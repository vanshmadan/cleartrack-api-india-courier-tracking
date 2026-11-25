"""Track every shipment in a CSV (header: carrier,awb) and flag the ones that need attention.

Writes results.csv in the current directory.
Usage: python bulk_track.py ../sample/awbs.csv
"""
import csv
import sys
import time

from cleartrack import ClearTrack, ClearTrackError


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python bulk_track.py <file.csv>")

    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        rows = [(r["carrier"].strip(), r["awb"].strip()) for r in csv.DictReader(f) if r.get("carrier") and r.get("awb")]

    ct = ClearTrack()
    fields = ["carrier", "awb", "status", "last_location", "requires_attention", "attention_reason", "error"]
    results = []

    for carrier, awb in rows:
        try:
            s = ct.track(carrier, awb)
            ins = s.get("insights") or {}
            flag = f"  <- {ins.get('attention_reason')}" if ins.get("requires_attention") else ""
            print(f"{carrier:<12} {awb:<16} {s['status']}{flag}")
            results.append({
                "carrier": carrier, "awb": awb, "status": s["status"],
                "last_location": s.get("last_known_location") or "",
                "requires_attention": str(ins.get("requires_attention", "")).lower(),
                "attention_reason": ins.get("attention_reason") or "", "error": "",
            })
        except ClearTrackError as e:
            print(f"{carrier:<12} {awb:<16} ERROR {e.code}")
            results.append({"carrier": carrier, "awb": awb, "error": e.code})
            # Out of lookups for the period / day: stop instead of failing every remaining row.
            if e.code in ("plan_quota_exceeded", "daily_quota_exceeded"):
                break
        time.sleep(0.25)  # stays under the 5 requests/second trial burst limit

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    print(f"\nWrote results.csv ({len(results)} rows). Each call uses 1 lookup from your plan.")


if __name__ == "__main__":
    main()

"""Track one shipment and print its status, insights and scan history.

Usage: python track.py <carrier> <awb>      e.g. python track.py indiapost EE123456789IN
"""
import sys

from cleartrack import ClearTrack, ClearTrackError


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python track.py <carrier> <awb>")
    carrier, awb = sys.argv[1], sys.argv[2]

    try:
        s = ClearTrack().track(carrier, awb)
    except (ClearTrackError, ValueError) as e:
        sys.exit(f"Error: {e}")

    print(f"{s['carrier']} {s['awb']}: {s['status']} ({s['status_text']})")
    print(f"Last location : {s.get('last_known_location') or 'unknown'}")
    print(f"Est. delivery : {s.get('estimated_delivery_at') or 'not given'}")
    print(f"Delivered at  : {s.get('delivered_at') or '-'}")
    insights = s.get("insights") or {}
    if insights.get("requires_attention"):
        print(f"Needs attention: {insights.get('attention_reason')}")
    if s.get("stale"):
        print("(carrier unreachable right now: showing last known data)")

    print("\nScans (newest first):")
    for e in s.get("events", []):
        print(f"  {e['timestamp']}  {e['status']:<16}  {e.get('description') or ''}  @ {e.get('location') or '-'}")


if __name__ == "__main__":
    main()

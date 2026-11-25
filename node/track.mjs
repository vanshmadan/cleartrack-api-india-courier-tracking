// Track one shipment and print its status, insights and scan history.
// Usage: node track.mjs <carrier> <awb>      e.g. node track.mjs indiapost EE123456789IN
import { ClearTrack } from "./cleartrack.mjs";

const [carrier, awb] = process.argv.slice(2);
if (!carrier || !awb) {
  console.error("Usage: node track.mjs <carrier> <awb>");
  process.exit(1);
}

try {
  const ct = new ClearTrack();
  const s = await ct.track(carrier, awb);

  console.log(`${s.carrier} ${s.awb}: ${s.status} (${s.status_text})`);
  console.log(`Last location : ${s.last_known_location ?? "unknown"}`);
  console.log(`Est. delivery : ${s.estimated_delivery_at ?? "not given"}`);
  console.log(`Delivered at  : ${s.delivered_at ?? "-"}`);
  if (s.insights?.requires_attention) {
    console.log(`Needs attention: ${s.insights.attention_reason}`);
  }
  if (s.stale) console.log("(carrier unreachable right now: showing last known data)");

  console.log("\nScans (newest first):");
  for (const e of s.events ?? []) {
    console.log(`  ${e.timestamp}  ${e.status.padEnd(16)}  ${e.description ?? ""}  @ ${e.location ?? "-"}`);
  }
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}

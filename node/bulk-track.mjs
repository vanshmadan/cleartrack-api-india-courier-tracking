// Track every shipment in a CSV (header: carrier,awb) and flag the ones that need attention.
// Writes results.csv next to where you run it.
// Usage: node bulk-track.mjs ../sample/awbs.csv
import { readFile, writeFile } from "node:fs/promises";
import { ClearTrack, ClearTrackError } from "./cleartrack.mjs";

const file = process.argv[2];
if (!file) {
  console.error("Usage: node bulk-track.mjs <file.csv>");
  process.exit(1);
}

const rows = (await readFile(file, "utf8"))
  .split(/\r?\n/)
  .slice(1)
  .map((line) => line.split(",").map((v) => v.trim()))
  .filter(([carrier, awb]) => carrier && awb);

const ct = new ClearTrack();
const out = [["carrier", "awb", "status", "last_location", "requires_attention", "attention_reason", "error"]];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

for (const [carrier, awb] of rows) {
  try {
    const s = await ct.track(carrier, awb);
    const flag = s.insights?.requires_attention ? `  <- ${s.insights.attention_reason}` : "";
    console.log(`${carrier.padEnd(12)} ${awb.padEnd(16)} ${s.status}${flag}`);
    out.push([carrier, awb, s.status, s.last_known_location ?? "", s.insights?.requires_attention ?? "", s.insights?.attention_reason ?? "", ""]);
  } catch (err) {
    const code = err instanceof ClearTrackError ? err.code : err.message;
    console.log(`${carrier.padEnd(12)} ${awb.padEnd(16)} ERROR ${code}`);
    out.push([carrier, awb, "", "", "", "", code]);
    // Out of lookups for the period / day: stop instead of failing every remaining row.
    if (code === "plan_quota_exceeded" || code === "daily_quota_exceeded") break;
  }
  await sleep(250); // stays under the 5 requests/second trial burst limit
}

const csv = out.map((r) => r.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(",")).join("\n");
await writeFile("results.csv", csv + "\n");
console.log(`\nWrote results.csv (${out.length - 1} rows). Each call uses 1 lookup from your plan.`);

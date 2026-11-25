// Show your plan and how many lookups are left.
// Usage: node usage.mjs
import { ClearTrack } from "./cleartrack.mjs";

const u = await new ClearTrack().usage();
console.log(`Plan   : ${u.plan} (${u.status})`);
console.log(`Period : ${u.period_lookups_used} / ${u.period_lookups_limit} lookups, ends ${u.period_end ?? "-"}`);
console.log(`Today  : ${u.daily_used} / ${u.daily_limit}`);

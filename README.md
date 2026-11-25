# ClearTrack API: India courier tracking examples (Node.js & Python)

Node.js and Python examples for the [ClearTrack Tracking API](https://api.cleartrackpromise.in/docs): one REST API that tracks shipments across Indian couriers and returns the same normalised JSON for all of them.

- One response shape for India Post / Speed Post, Delhivery, Blue Dart, Ekart, Xpressbees, Shadowfax, Shree Maruti, Trackon, The Professional Couriers and Shiprocket.
- Normalised status (`in_transit`, `out_for_delivery`, `delivered`, `returned`...), scan history, milestones and failed delivery attempts with reason codes.
- Computed insights: stuck shipments (no scan for 72h+), late against the carrier's ETA, RTO, and `requires_attention` with a reason.
- Receiver names, phone numbers and OTPs are stripped from every response.

## Quick start

1. Get a free 14-day trial key (100 lookups) at **https://api.cleartrackpromise.in/trial**.
2. Set it in your shell:

```bash
export CLEARTRACK_API_KEY=ct_live_your_key_here
```

3. Try it with curl:

```bash
curl -H "X-API-Key: $CLEARTRACK_API_KEY" https://api.cleartrackpromise.in/v1/track/indiapost/EE123456789IN
```

Replace `EE123456789IN` with a real tracking number.

## Examples

| | Node.js (18+, no dependencies) | Python (3.8+, standard library) |
|---|---|---|
| Track one shipment | [`node/track.mjs`](node/track.mjs) | [`python/track.py`](python/track.py) |
| Track a CSV of shipments, flag problems | [`node/bulk-track.mjs`](node/bulk-track.mjs) | [`python/bulk_track.py`](python/bulk_track.py) |
| Check plan and remaining lookups | [`node/usage.mjs`](node/usage.mjs) | [`python/usage.py`](python/usage.py) |
| Small client to copy into your project | [`node/cleartrack.mjs`](node/cleartrack.mjs) | [`python/cleartrack.py`](python/cleartrack.py) |

```bash
cd node && node track.mjs bluedart 78036172546
```

```bash
cd python && python track.py bluedart 78036172546
```

## API at a glance

| Endpoint | What it returns |
|---|---|
| `GET /v1/track/{carrier}/{awb}` | Normalised tracking for one shipment |
| `GET /v1/usage` | Plan, period and daily lookup usage |

Base URL: `https://api.cleartrackpromise.in/v1`. Auth: `X-API-Key` header.

**Carrier slugs:** `indiapost`, `speedpost`, `delhivery`, `bluedart`, `ekart`, `xpressbees`, `shadowfax`, `shreemaruti`, `trackon`, `professional` (alias `tpc`), `shiprocket`. DTDC is not supported.

**Short response example:**

```json
{
  "awb": "EE123456789IN",
  "carrier": "indiapost",
  "status": "delivered",
  "status_text": "Item Delivery Confirmed",
  "is_delivered": true,
  "last_known_location": "Mumbai GPO",
  "estimated_delivery_at": "2026-10-05T18:00:00.000Z",
  "delivered_at": "2026-10-05T14:32:00.000Z",
  "insights": {
    "is_stuck": false,
    "requires_attention": false,
    "attention_reason": null,
    "current_stage": "delivered"
  },
  "events": [
    { "timestamp": "2026-10-05T14:32:00.000Z", "status": "delivered", "description": "Item Delivery Confirmed", "location": "Mumbai GPO" }
  ]
}
```

See the [full API docs](https://api.cleartrackpromise.in/docs) for every field, status and error code.

## Errors and limits

Errors come back as `{"error": {"code": "...", "message": "..."}}`. The ones you'll handle most:

| HTTP | `code` | What to do |
|---|---|---|
| 400 | `unsupported_carrier` / `invalid_awb` | Fix the carrier slug or tracking number |
| 401 | `missing_api_key` / `invalid_api_key` | Check the `X-API-Key` header |
| 404 | `shipment_not_found` | The carrier has no scans for this number yet |
| 429 | `rate_limit_exceeded` | Too many requests per second: wait `Retry-After` seconds (the example clients retry this) |
| 429 | `daily_quota_exceeded` / `plan_quota_exceeded` | Out of lookups for the day or plan period |

Every call counts as one lookup, including cached answers. Active shipments are cached for 30 minutes, so polling the same number more often than that just uses up lookups.

## Plans

All prices in INR. Paid plans are prepaid for 30 days. Renewing an active plan adds the new 30 days to the days you have left.

| Plan | Price | Valid for | Lookups included | Daily cap | Burst limit |
|---|---|---|---|---|---|
| Free Trial | Free | 14 days | 100 | 100 / day | 5 req/sec |
| Starter | ₹399 | 30 days | 1,500 | 300 / day | 5 req/sec |
| Growth | ₹999 | 30 days | 4,000 | 800 / day | 10 req/sec |
| Business | ₹3,000 | 30 days | 12,000 | 2,400 / day | 20 req/sec |

- Usage is counted in **lookups, not shipments**: every API call is one lookup, including cached answers and repeat checks of the same number.
- Growth and Business also include the Shipment Analyzer (sign in with your ClearTrack account). Business gets priority email support; the other paid plans get standard email support.
- Check what you have left at any time with `GET /v1/usage` (or [`node/usage.mjs`](node/usage.mjs) / [`python/usage.py`](python/usage.py)).

Start the trial at https://api.cleartrackpromise.in/trial. See current pricing at https://api.cleartrackpromise.in/pricing.

## Security

Call the API from your backend only. Don't put your API key in browser JavaScript or a mobile app. Keep it in an environment variable (see [`.env.example`](.env.example)).

## License

MIT. See [LICENSE](LICENSE).

# Node.js examples

Needs Node 18 or newer. No `npm install`: the examples only use the built-in `fetch`.

```bash
export CLEARTRACK_API_KEY=ct_live_your_key_here
```

```bash
node track.mjs indiapost EE123456789IN
```

```bash
node usage.mjs
```

```bash
node bulk-track.mjs ../sample/awbs.csv
```

Use [`cleartrack.mjs`](cleartrack.mjs) in your own code:

```js
import { ClearTrack } from "./cleartrack.mjs";

const ct = new ClearTrack(); // reads CLEARTRACK_API_KEY
const shipment = await ct.track("bluedart", "78036172546");
console.log(shipment.status, shipment.insights.requires_attention);
```

Call the API from your server only. Never put your API key in browser or mobile app code.

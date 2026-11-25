# Python examples

Needs Python 3.8 or newer. Nothing to install: the examples only use the standard library.

```bash
export CLEARTRACK_API_KEY=ct_live_your_key_here
```

```bash
python track.py indiapost EE123456789IN
```

```bash
python usage.py
```

```bash
python bulk_track.py ../sample/awbs.csv
```

Use [`cleartrack.py`](cleartrack.py) in your own code:

```python
from cleartrack import ClearTrack

ct = ClearTrack()  # reads CLEARTRACK_API_KEY
shipment = ct.track("bluedart", "78036172546")
print(shipment["status"], shipment["insights"]["requires_attention"])
```

Call the API from your server only. Never put your API key in browser or mobile app code.

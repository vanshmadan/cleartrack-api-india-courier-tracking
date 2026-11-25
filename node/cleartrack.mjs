// Minimal ClearTrack API client. No dependencies: uses the fetch built into Node 18+.
// Docs: https://api.cleartrackpromise.in/docs

const DEFAULT_BASE_URL = "https://api.cleartrackpromise.in/v1";

export class ClearTrackError extends Error {
  constructor(status, code, message, retryAfter = null) {
    super(`${status} ${code}: ${message}`);
    this.status = status;
    this.code = code;
    this.retryAfter = retryAfter;
  }
}

export class ClearTrack {
  constructor({ apiKey = process.env.CLEARTRACK_API_KEY, baseUrl = process.env.CLEARTRACK_BASE_URL || DEFAULT_BASE_URL, maxRetries = 2 } = {}) {
    if (!apiKey) throw new Error("Set CLEARTRACK_API_KEY (get a trial key at https://api.cleartrackpromise.in/trial)");
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.maxRetries = maxRetries;
  }

  /** Normalised tracking for one shipment. carrier: e.g. "indiapost", "bluedart", "delhivery". */
  track(carrier, awb) {
    return this.#get(`/track/${encodeURIComponent(carrier)}/${encodeURIComponent(awb)}`);
  }

  /** Plan, period and daily quota for this API key. */
  usage() {
    return this.#get("/usage");
  }

  async #get(path) {
    for (let attempt = 0; ; attempt++) {
      const res = await fetch(this.baseUrl + path, {
        headers: { "X-API-Key": this.apiKey, Accept: "application/json" },
      });
      const body = await res.json().catch(() => ({}));
      if (res.ok) return body;

      const code = body?.error?.code ?? "unknown_error";
      const message = body?.error?.message ?? res.statusText;
      const retryAfter = Number(res.headers.get("retry-after")) || null;

      // Retry only the short per-second burst limit. Period / daily quota errors won't clear by waiting a few seconds.
      if (res.status === 429 && code === "rate_limit_exceeded" && attempt < this.maxRetries) {
        await new Promise((r) => setTimeout(r, (retryAfter ?? 1) * 1000));
        continue;
      }
      throw new ClearTrackError(res.status, code, message, retryAfter);
    }
  }
}

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import feedparser
import asyncio
import httpx
import re
from scrapling.fetchers import Fetcher

app = FastAPI(title="Hybrid News Pipeline (RSS + URLs)")


# =====================
# MODELS
# =====================
class HybridRequest(BaseModel):
    rss_feeds: Optional[List[str]] = []
    urls: Optional[List[HttpUrl]] = []
    callback_url: HttpUrl


# =====================
# CLEANER
# =====================
JUNK_PATTERNS = re.compile(
    r"cookie|subscribe|newsletter|privacy policy|accept all",
    flags=re.IGNORECASE,
)

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<script.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)          # strip remaining tags
    text = re.sub(r"\s+", " ", text)
    text = JUNK_PATTERNS.sub("", text)
    return text.strip()


# =====================
# RSS → URL EXPANSION
# =====================
def _extract_urls_from_rss_sync(feed_url: str) -> List[str]:
    try:
        feed = feedparser.parse(feed_url)
        return [e.link for e in feed.entries if hasattr(e, "link")]
    except Exception as e:
        print(f"RSS ERROR [{feed_url}]: {e}")
        return []


async def extract_urls_from_rss(feed_url: str) -> List[str]:
    # feedparser.parse is blocking I/O — run it off the event loop
    return await asyncio.to_thread(_extract_urls_from_rss_sync, feed_url)


# =====================
# SCRAPER
# =====================
def extract_article_sync(url: str) -> Optional[str]:
    try:
        fetcher = Fetcher(
            respect_robots=False,
            timeout=20,
            retries=2,
        )
        r = fetcher.get(url)

        # Use Scrapling's native text extraction (no BS4)
        text = clean_text(r.get_all_text(ignore_tags=("script", "style", "noscript")))

        return text if len(text) >= 250 else None

    except Exception as e:
        print(f"SCRAPE ERROR [{url}]: {e}")
        return None


async def extract_article(url: str) -> Optional[str]:
    return await asyncio.to_thread(extract_article_sync, url)


# =====================
# CALLBACK
# =====================
async def send_callback(client: httpx.AsyncClient, url: str, text: str) -> None:
    try:
        response = await client.post(url, json={"raw_input": text}, timeout=15)
        print(f"CALLBACK STATUS: {response.status_code}")
        if response.status_code != 200:
            print(f"CALLBACK BODY: {response.text}")
    except Exception as e:
        print(f"CALLBACK EXCEPTION: {repr(e)}")


# =====================
# SHARED URL COLLECTOR
# =====================
async def collect_urls(req: HybridRequest) -> List[str]:
    rss_results = await asyncio.gather(
        *[extract_urls_from_rss(feed) for feed in (req.rss_feeds or [])]
    )
    all_urls = [url for urls in rss_results for url in urls]
    all_urls += [str(u) for u in (req.urls or [])]
    return list(set(all_urls))  # dedup


# =====================
# ENDPOINTS
# =====================
@app.post("/hybrid_batch")
async def hybrid_batch(req: HybridRequest):
    all_urls = await collect_urls(req)

    results = await asyncio.gather(*[extract_article(u) for u in all_urls])

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[
            send_callback(client, str(req.callback_url), r)
            for r in results if r
        ])

    return {
        "status": "completed",
        "processed": sum(1 for r in results if r),
        "total_urls": len(all_urls),
    }


@app.post("/stream")
async def stream(req: HybridRequest):
    all_urls = await collect_urls(req)
    print(f"TOTAL URLS: {len(all_urls)}")

    processed = 0
    async with httpx.AsyncClient() as client:
        for url in all_urls:
            print(f"➡️  Processing: {url}")
            text = await extract_article(url)

            if not text:
                print(f"❌ NO TEXT: {url}")
                continue

            print(f"✅ TEXT OK: {url}  len={len(text)}")
            await send_callback(client, str(req.callback_url), text)
            processed += 1

    return {"status": "stream_completed", "processed": processed}


# =====================
# MAIN
# =====================
def main():
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8070, reload=True)


if __name__ == "__main__":
    main()
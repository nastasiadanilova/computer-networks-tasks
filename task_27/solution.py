import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
import sys

def _fetch(url: str, retries: int, timeout: int) -> dict:
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                body = resp.read()
                return {"url": url, "status": resp.status,
                        "bytes": len(body), "attempts": attempt, "error": None}
        except urllib.error.HTTPError as e:
            return {"url": url, "status": e.code,
                    "bytes": 0, "attempts": attempt, "error": str(e.reason)}
        except Exception as e:
            last_err = str(e)
    return {"url": url, "status": None, "bytes": 0,
            "attempts": retries, "error": last_err}

def download_all(urls: list, workers: int = 4,
                 retries: int = 3, timeout: int = 5) -> list:
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_fetch, u, retries, timeout) for u in urls]
        return [f.result() for f in futs]

if __name__ == "__main__":
    urls = sys.argv[1:] if len(sys.argv) > 1 else []
    if not urls:
        print("Usage: python3 solution.py <url1> [url2 ...]")
        sys.exit(0)
    for r in download_all(urls):
        print(r)

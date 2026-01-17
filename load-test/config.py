BASE_URL = "https://www.n11.com"

SEARCH_PATH = "/arama"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

MIN_WAIT_TIME = 1
MAX_WAIT_TIME = 3

INVALID_SEARCH_TERMS = [
    "xyzqwerty123",
    "nonexistingproduct",
    "   ",
    "a",
    "sdfkdsfjhdsjfhks" * 50,
]

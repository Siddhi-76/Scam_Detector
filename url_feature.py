import math
import re
from urllib.parse import urlparse

BRANDS = ["paytm", "google", "amazon", "flipkart", "phonepe", "gpay", "hdfc", "sbi", "icici"]


def parse_url(url):
    """Break a URL into scheme, domain, path, query. e.g. https://paytm-kyc.xyz/login -> scheme=https, netloc=paytm-kyc.xyz"""
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
    }


def uses_https(url):
    """Returns 1 if safe (https), 0 if not. No HTTPS = data sent in plain text = easy to intercept."""
    return 1 if url.startswith("https://") else 0


def url_length(url):
    """Long URLs hide the real domain in noise. Legitimate sites rarely exceed 50-60 chars."""
    return len(url)


def shannon_entropy(text):
    """Measures randomness. Formula: H = -sum(p * log2(p)) for each char. Real brands (paytm, google) score ~2.5-3.0. Auto-generated scam domains (asdkj82h) score 3.8+."""
    if not text:
        return 0.0
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    length = len(text)
    return round(-sum((c / length) * math.log2(c / length) for c in freq.values()), 3)


def levenshtein_distance(a, b):
    if len(a) < len(b):
        return levenshtein_distance(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for ca in a:
        curr = [prev[0] + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[-1] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


def extract_features(url):
    """Run all checks on a URL. Returns a dict of features. This dict becomes one row in your ML training dataset."""
    netloc = urlparse(url).netloc
    domain = netloc.replace("www.", "").split(".")[0].replace("-", "")
    dists = {b: levenshtein_distance(domain[: len(b) + 2], b) for b in BRANDS}
    best = min(dists, key=dists.get)
    is_lk = 1 if (0 < dists[best] <= 2 and domain != best) else 0
    return {
        "uses_https": 1 if url.startswith("https://") else 0,
        "url_length": len(url),
        "subdomain_count": max(0, len(netloc.split(".")) - 2),
        "has_ip": 1 if re.match(r"^\d+\.\d+\.\d+\.\d+$", netloc.split(":")[0]) else 0,
        "has_at": 1 if "@" in url else 0,
        "hyphen_count": netloc.count("-"),
        "suspicious_tld": 1
        if any(netloc.endswith(t) for t in [".xyz", ".top", ".click", ".loan", ".online", ".site"])
        else 0,
        "domain_entropy": shannon_entropy(domain),
        "is_brand_lookalike": is_lk,
        "closest_brand": best,
        "brand_distance": dists[best],
        "url": url,
    }


if __name__ == "__main__":
    url = "https://paytm-kyc.xyz/login"
    print(extract_features(url))

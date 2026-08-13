import math
import re
from urllib.parse import urlparse

BRANDS = [
    "paytm",
    "phonepe",
    "googlepay",
    "sbi",
    "hdfc",
    "icici",
    "amazon",
    "flipkart",
    "whatsapp",
    "rbi",
    "upi",
]

URL_SHORTENERS = {
    "bit.ly",
    "t.co",
    "tinyurl.com",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "rebrand.ly",
    "cutt.ly",
    "rb.gy",
    "lnkd.in",
    "amzn.to",
    "fb.me",
    "youtu.be",
    "tiny.cc",
    "shorturl.at",
}


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


def is_url_shortener(url):
    """Returns 1 if the URL uses a known shortener (bit.ly, t.co, etc.), else 0."""
    url_for_parse = url if (url.startswith("http://") or url.startswith("https://")) else ("http://" + url)
    host = urlparse(url_for_parse).netloc.lower().replace("www.", "").split(":")[0]
    return 1 if host in URL_SHORTENERS else 0


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
    url_for_parse = url if (url.startswith("http://") or url.startswith("https://")) else ("http://" + url)
    netloc = urlparse(url_for_parse).netloc
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
        "is_url_shortener": is_url_shortener(url),
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


def rule_based_score(features):
    score, reasons = 0, []
    if not features["uses_https"]:
        score += 15
        reasons.append("No HTTPS — traffic not encrypted")
    if features["url_length"] > 75:
        score += 10
        reasons.append(f"Long URL ({features['url_length']} chars)")
    if features["subdomain_count"] >= 2:
        score += 15
        reasons.append("Multiple subdomains hiding real domain")
    if features["has_ip"]:
        score += 25
        reasons.append("Uses raw IP instead of domain name")
    if features["has_at"]:
        score += 30
        reasons.append("@ symbol — classic URL redirect trick")
    if features["hyphen_count"] >= 2:
        score += 10
        reasons.append("Multiple hyphens — fake domain pattern")
    if features["suspicious_tld"]:
        score += 15
        reasons.append("High-risk TLD (.xyz/.top/.click etc)")
    if features["domain_entropy"] > 3.8:
        score += 10
        reasons.append(f"High randomness in domain (entropy={features['domain_entropy']})")
    if features["is_brand_lookalike"]:
        score += 35
        reasons.append(f"Looks like '{features['closest_brand']}' — brand impersonation")
    score = min(score, 100)
    verdict = "DANGEROUS" if score >= 60 else "SUSPICIOUS" if score >= 30 else "LIKELY SAFE"
    return {"score": score, "verdict": verdict, "reasons": reasons}


if __name__ == "__main__":
    url = "https://paytm-kyc.xyz/login"
    features = extract_features(url)
    print(features)
    print(rule_based_score(features))

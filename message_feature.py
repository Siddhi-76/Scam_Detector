import re

URGENCY_WORDS = [
    "urgent",
    "immediately",
    "expire",
    "expires",
    "expiry",
    "last chance",
    "blocked",
    "suspended",
    "action required",
    "verify now",
    "final warning",
    "limited time",
]
REWARD_WORDS = [
    "you have won",
    "winner",
    "prize",
    "lottery",
    "selected",
    "claim now",
    "congratulations",
    "reward",
    "bonus",
    "gift",
]
KYC_WORDS = [
    "kyc",
    "otp",
    "verify your account",
    "account suspended",
    "rbi",
    "sebi",
    "bank alert",
    "aadhar",
    "pan card",
    "aadhaar",
]
HINGLISH_SCAM = [
    "turant",
    "abhi",
    "inam",
    "paisa milega",
    "khata band",
    "bank se call",
    "lucky draw",
    "jaldi karo",
    "time khatam",
]


def detect_urgency(text):
    t = text.lower()
    matched = [w for w in URGENCY_WORDS if w in t]
    return {"count": len(matched), "matched": matched}


def detect_reward(text):
    t = text.lower()
    matched = [w for w in REWARD_WORDS if w in t]
    return {"count": len(matched), "matched": matched}


def detect_kyc_otp(text):
    t = text.lower()
    matched = [w for w in KYC_WORDS if w in t]
    return {"count": len(matched), "matched": matched}


def detect_caps_abuse(text):
    words = text.split()
    if not words:
        return 0.0
    caps_ratio = sum(1 for w in words if w.isupper() and len(w) > 2) / len(words)
    return round(caps_ratio, 3)


def detect_hinglish(text):
    t = text.lower()
    matched = [w for w in HINGLISH_SCAM if w in t]
    return {"count": len(matched), "matched": matched}


def has_phone_number(text):
    # Indian mobile: 10 digits starting with 6, 7, 8, or 9
    return 1 if re.search(r"\b[6-9]\d{9}\b", text) else 0


def has_embedded_url(text):
    shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly", "short.url"]
    return 1 if any(s in text.lower() for s in shorteners) else 0


def extract_message_features(text):
    urg = detect_urgency(text)
    rew = detect_reward(text)
    kyc = detect_kyc_otp(text)
    hin = detect_hinglish(text)
    return {
        "urgency_count": urg["count"],
        "urgency_words": urg["matched"],
        "reward_count": rew["count"],
        "reward_words": rew["matched"],
        "kyc_count": kyc["count"],
        "kyc_words": kyc["matched"],
        "caps_ratio": detect_caps_abuse(text),
        "hinglish_count": hin["count"],
        "hinglish_words": hin["matched"],
        "exclamations": text.count("!"),
        "has_phone": has_phone_number(text),
        "has_short_url": has_embedded_url(text),
    }


def message_risk_score(features):
    score, reasons = 0, []
    if features["urgency_count"] >= 2:
        score += 25
        reasons.append(f"Urgency language: {features['urgency_words']}")
    if features["reward_count"] >= 1:
        score += 30
        reasons.append(f"Fake reward claim: {features['reward_words']}")
    if features["kyc_count"] >= 1:
        score += 25
        reasons.append(f"KYC/OTP scam pattern: {features['kyc_words']}")
    if features["caps_ratio"] > 0.3:
        score += 10
        reasons.append(f"Excessive CAPS abuse ({features['caps_ratio'] * 100:.0f}% caps)")
    if features["hinglish_count"] >= 1:
        score += 20
        reasons.append(f"Hinglish scam phrases: {features['hinglish_words']}")
    if features["exclamations"] >= 3:
        score += 10
        reasons.append(f"{features['exclamations']} exclamation marks")
    if features["has_phone"]:
        score += 15
        reasons.append("Embedded Indian phone number")
    if features["has_short_url"]:
        score += 20
        reasons.append("Shortened/hidden URL in message")
    score = min(score, 100)
    verdict = "DANGEROUS" if score >= 60 else "SUSPICIOUS" if score >= 30 else "LIKELY SAFE"
    return {"score": score, "verdict": verdict, "reasons": reasons}


if __name__ == "__main__":
    sample = "URGENT! Your KYC is expired. Call 9876543210 now or account BLOCKED!!! Claim reward at bit.ly/scam"
    features = extract_message_features(sample)
    print(features)
    print(message_risk_score(features))

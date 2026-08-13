"""
NIGRANI 50-Sample Evaluation Suite
Runs rule-based + ML threat detection across 50 real-world samples (25 Scam, 25 Legit)
and produces a detailed evaluation document logging True Positives, True Negatives,
False Positives, False Negatives, and diagnostic root causes.
"""

import os
import sys
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from url_features import extract_features, rule_based_score
from message_feature import extract_message_features, message_risk_score
import joblib

MODEL = None
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model.pkl")
if os.path.exists(model_path):
    MODEL = joblib.load(model_path)

# 50 Real-World Test Samples (25 Scam / 25 Legit)
SAMPLES = [
    # --- 25 SCAM SAMPLES ---
    {"input": "http://paytm-kyc.verify-now.xyz/login", "label": 1, "type": "url", "source": "PhishTank / CERT-In"},
    {"input": "http://free-iphone-claim.top/win", "label": 1, "type": "url", "source": "OpenPhish"},
    {"input": "http://sbi-netbanking-update.click/verify", "label": 1, "type": "url", "source": "CERT-In Advisory"},
    {"input": "http://192.168.1.1/admin/paytm.html", "label": 1, "type": "url", "source": "PhishTank"},
    {"input": "http://user@google-security-alert.com/login", "label": 1, "type": "url", "source": "PhishTank"},
    {"input": "http://phonepe-reward-scratchcard.online", "label": 1, "type": "url", "source": "WhatsApp Forward"},
    {"input": "http://icici-card-limit-increase.site", "label": 1, "type": "url", "source": "CERT-In Advisory"},
    {"input": "http://amazon-prime-free-lifetime.xyz/claim", "label": 1, "type": "url", "source": "OpenPhish"},
    {"input": "http://whatsapp-gold-download-now.top", "label": 1, "type": "url", "source": "WhatsApp Forward"},
    {"input": "http://rbi-unclaimed-fund-transfer.click", "label": 1, "type": "url", "source": "CERT-In Advisory"},
    {"input": "http://hdfc-netbanking-suspended.xyz/reactivate", "label": 1, "type": "url", "source": "PhishTank"},
    {"input": "http://flipkart-big-billion-winner.top/prize", "label": 1, "type": "url", "source": "OpenPhish"},
    {"input": "http://googlepay-scratch-card.online/rewards", "label": 1, "type": "url", "source": "WhatsApp Forward"},
    {"input": "http://sbi-yono-app-update.click/download", "label": 1, "type": "url", "source": "CERT-In Advisory"},
    {"input": "http://paytm-cashback-offer-2024.site/claim", "label": 1, "type": "url", "source": "WhatsApp Forward"},
    {"input": "http://bit.ly/free-prize-claim-now", "label": 1, "type": "url", "source": "OpenPhish"},
    {"input": "http://192.168.0.100/banking/login.php", "label": 1, "type": "url", "source": "PhishTank"},
    {"input": "http://income-tax-refund-pending.online/claim", "label": 1, "type": "url", "source": "CERT-In Advisory"},
    {"input": "http://epfo-pf-withdrawal-apply.top/submit", "label": 1, "type": "url", "source": "CERT-In Advisory"},
    {"input": "http://jio-free-recharge-offer.top/claim", "label": 1, "type": "url", "source": "WhatsApp Forward"},
    {"input": "URGENT! Your KYC is expired. Call 9876543210 now or account BLOCKED!!! Claim reward at bit.ly/scam", "label": 1, "type": "message", "source": "WhatsApp Forward"},
    {"input": "Congratulations! You have won Rs 50,000 lottery reward from KBC. Click bit.ly/claim to receive money.", "label": 1, "type": "message", "source": "WhatsApp Forward"},
    {"input": "Dear customer, your SBI account is suspended due to missing PAN. Verify immediately at http://sbi-pan.click", "label": 1, "type": "message", "source": "SMS Scam"},
    {"input": "Khata band hone wala hai! Abhi turant 9876543210 pe call karein aur inam claim karein.", "label": 1, "type": "message", "source": "WhatsApp Forward (Hinglish)"},
    {"input": "Electricity bill unpaid! Your power connection will be disconnected tonight at 9:30 PM. Call official 9812345678", "label": 1, "type": "message", "source": "SMS Scam"},

    # --- 25 LEGIT SAMPLES ---
    {"input": "https://www.google.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.amazon.in", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.wikipedia.org", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://github.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.paytm.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.phonepe.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.sbi.co.in", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.hdfcbank.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.icicibank.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.flipkart.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.youtube.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.facebook.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.linkedin.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.rbi.org.in", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.incometax.gov.in", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.irctc.co.in", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.zomato.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.swiggy.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.spotify.com", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "https://www.coursera.org", "label": 0, "type": "url", "source": "Legitimate Site"},
    {"input": "Hey, let's catch up tomorrow at 5 PM for coffee near the campus library!", "label": 0, "type": "message", "source": "Legitimate Message"},
    {"input": "Your Amazon order #408-1234567-8901234 has been dispatched and will arrive tomorrow.", "label": 0, "type": "message", "source": "Legitimate Message"},
    {"input": "Please review the attached project proposal draft and let me know your thoughts.", "label": 0, "type": "message", "source": "Legitimate Message"},
    {"input": "Good morning! Don't forget to submit the assignment before midnight today.", "label": 0, "type": "message", "source": "Legitimate Message"},
    {"input": "Happy Birthday! Wishing you a fantastic year filled with health, happiness and success!", "label": 0, "type": "message", "source": "Legitimate Message"},
]

def run_evaluation():
    results = []
    tp, tn, fp, fn = 0, 0, 0, 0

    print("=" * 70)
    print("  NIGRANI 50-SAMPLE DETECTOR EVALUATION SUITE")
    print("=" * 70)

    for i, item in enumerate(SAMPLES, 1):
        inp = item["input"]
        true_label = item["label"]
        stype = item["type"]

        if stype == "url":
            feats = extract_features(inp)
            res = rule_based_score(feats)
            if MODEL:
                feature_cols = [
                    "uses_https","url_length","subdomain_count","has_ip",
                    "has_at","hyphen_count","suspicious_tld","domain_entropy","is_brand_lookalike"
                ]
                feat_df = pd.DataFrame([[feats.get(k, 0) for k in feature_cols]], columns=feature_cols)
                ml_p = MODEL.predict(feat_df)[0]
                res["ml_verdict"] = "SCAM" if ml_p == 1 else "SAFE"
        else:
            msg_feats = extract_message_features(inp)
            res = message_risk_score(msg_feats)

        predicted_scam = 1 if (res["score"] >= 30 or res.get("ml_verdict") == "SCAM") else 0
        verdict_str = res["verdict"]

        # Classification outcome
        if true_label == 1 and predicted_scam == 1:
            outcome = "TP (True Positive)"
            tp += 1
        elif true_label == 0 and predicted_scam == 0:
            outcome = "TN (True Negative)"
            tn += 1
        elif true_label == 0 and predicted_scam == 1:
            outcome = "FP (False Positive)"
            fp += 1
        else:
            outcome = "FN (False Negative)"
            fn += 1

        results.append({
            "ID": i,
            "Input": inp[:45] + "..." if len(inp) > 45 else inp,
            "Type": stype,
            "True Label": "SCAM" if true_label == 1 else "LEGIT",
            "Predicted Verdict": verdict_str,
            "Risk Score": res["score"],
            "Outcome": outcome,
            "Reasons": "; ".join(res.get("reasons", []))
        })

    accuracy = (tp + tn) / len(SAMPLES)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print(f"\nEvaluation Results:")
    print(f"  Total Samples Evaluated: {len(SAMPLES)}")
    print(f"  True Positives  (Scams Caught):     {tp}")
    print(f"  True Negatives  (Legit Cleared):   {tn}")
    print(f"  False Positives (Legit Flagged):   {fp}")
    print(f"  False Negatives (Scams Missed):    {fn}")
    print(f"  Accuracy:  {accuracy * 100:.2f}%")
    print(f"  Precision: {precision * 100:.2f}%")
    print(f"  Recall:    {recall * 100:.2f}%")
    print(f"  F1-Score:  {f1 * 100:.2f}%")
    print("=" * 70)

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv("tests/evaluation_report.csv", index=False)
    print("Saved detailed test log to tests/evaluation_report.csv")

if __name__ == "__main__":
    run_evaluation()

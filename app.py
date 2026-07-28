import os

import joblib
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from message_feature import extract_message_features, message_risk_score
from url_features import extract_features, rule_based_score

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")

# Load ML model if it exists
MODEL = None
if os.path.exists("model.pkl"):
    MODEL = joblib.load("model.pkl")



@app.route("/")
def index():
    """Serve the main HTML page. Flask looks for index.html inside the templates/ folder automatically."""
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    """Main detection endpoint.

    Receives JSON: {"input": "http://paytm-kyc.xyz"}
    Returns JSON: {"score": 85, "verdict": "DANGEROUS", "reasons": [...]}
    """
    data = request.get_json()
    user_input = data.get("input", "").strip()
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Decide: URL or message?
    is_url = user_input.startswith("http") or user_input.startswith("www.")
    if is_url:
        features = extract_features(user_input)
        result = rule_based_score(features)
        result["type"] = "url"
    else:
        msg_features = extract_message_features(user_input)
        result = message_risk_score(msg_features)
        result["type"] = "message"

    # Add ML model prediction if available (Week 3)
    if MODEL and is_url:
        feat_vec = [
            [
                features.get(k, 0)
                for k in [
                    "uses_https",
                    "url_length",
                    "subdomain_count",
                    "has_ip",
                    "has_at",
                    "hyphen_count",
                    "suspicious_tld",
                    "domain_entropy",
                    "is_brand_lookalike",
                ]
            ]
        ]
        ml_pred = MODEL.predict(feat_vec)[0]
        result["ml_verdict"] = "SCAM" if ml_pred == 1 else "SAFE"

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

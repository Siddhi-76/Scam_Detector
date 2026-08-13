import io
import os
import pandas as pd

import joblib
import pickle
import numpy as np
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_file

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

from message_feature import extract_message_features, message_risk_score
from report_generator import generate_report
from url_features import extract_features, rule_based_score

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")

# Load ML models if they exist
MODEL = None
if os.path.exists("model.pkl"):
    MODEL = joblib.load("model.pkl")

DL_MODEL = None
TOKENIZER = None
if TF_AVAILABLE and os.path.exists("message_dl_model.keras") and os.path.exists("tokenizer.pkl"):
    try:
        DL_MODEL = load_model("message_dl_model.keras")
        with open("tokenizer.pkl", "rb") as f:
            TOKENIZER = pickle.load(f)
    except Exception as e:
        print("Error loading DL model:", e)


@app.route("/")
def index():
    """Serve the main HTML page."""
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
    features = None
    if is_url:
        features = extract_features(user_input)
        result = rule_based_score(features)
        result["type"] = "url"
        result["features"] = features
    else:
        msg_features = extract_message_features(user_input)
        result = message_risk_score(msg_features)
        result["type"] = "message"

    # Add ML model prediction if available
    if is_url and MODEL and features:
        feature_cols = [
            "uses_https", "url_length", "subdomain_count", "has_ip", "has_at",
            "hyphen_count", "suspicious_tld", "domain_entropy", "is_brand_lookalike"
        ]
        feat_df = pd.DataFrame([[features.get(k, 0) for k in feature_cols]], columns=feature_cols)
        ml_pred = MODEL.predict(feat_df)[0]
        result["ml_verdict"] = "SCAM" if ml_pred == 1 else "SAFE"
    elif not is_url and DL_MODEL and TOKENIZER:
        # Deep Learning Message Analysis
        seq = TOKENIZER.texts_to_sequences([user_input])
        pad = pad_sequences(seq, maxlen=50, padding='post', truncating='post')
        pred_prob = DL_MODEL.predict(pad, verbose=0)[0][0]
        
        result["dl_confidence"] = f"{pred_prob * 100:.1f}%"
        result["dl_verdict"] = "SCAM" if pred_prob > 0.5 else "SAFE"
        
        # Override or enhance rule-based verdict if DL is very confident
        if pred_prob > 0.85:
            result["verdict"] = "DANGEROUS"
            result["reasons"].append(f"AI Deep Learning model flagged with {result['dl_confidence']} confidence.")
        elif pred_prob < 0.15 and result["score"] < 50:
            result["verdict"] = "LIKELY SAFE"

    return jsonify(result)


@app.route("/report", methods=["POST"])
def report():
    """Generate and return a PDF threat analysis report.

    Receives JSON: {"input": "...", "result": {...}, "features": {...}}
    Returns: PDF file download
    """
    data = request.get_json()
    user_input = data.get("input", "")
    analysis_result = data.get("result", {})
    features = data.get("features", None)

    pdf_bytes = generate_report(user_input, analysis_result, features)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"NIGRANI_Report_{analysis_result.get('verdict', 'scan')}.pdf",
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("=" * 60)
    print(f" 🛡️ NIGRANI Scam Detector active")
    print(f" 🚀 Localhost URL: http://localhost:{port}")
    print(f" 🌐 Loopback URL:  http://127.0.0.1:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)






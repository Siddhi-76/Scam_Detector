"""
NIGRANI — PDF Report Generator
Generates detailed threat analysis reports in PDF format.
"""

from datetime import datetime
from fpdf import FPDF

def sanitize_text(text):
    """Ensure text only contains characters supported by FPDF core fonts (latin-1)."""
    if text is None:
        return ""
    return str(text).encode('latin-1', 'replace').decode('latin-1')


class NigraniReport(FPDF):
    """Custom PDF class with NIGRANI branding."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        # Brand bar
        self.set_fill_color(108, 99, 255)
        self.rect(0, 0, 210, 8, "F")
        # Logo text
        self.set_y(12)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(108, 99, 255)
        self.cell(100, 8, "NIGRANI", align="L")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, "AI-Powered Threat Analysis Report", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        # Divider
        self.set_draw_color(108, 99, 255)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"NIGRANI Report | Page {self.page_no()}/{{nb}}", align="C")

    def add_section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(40, 40, 60)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(108, 99, 255)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def add_key_value(self, key, value, bold_value=False):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(100, 100, 100)
        self.cell(50, 7, key + ":", align="L")
        style = "B" if bold_value else ""
        self.set_font("Helvetica", style, 10)
        self.set_text_color(40, 40, 60)
        self.cell(0, 7, str(value), new_x="LMARGIN", new_y="NEXT")

    def add_verdict_badge(self, verdict, score):
        if score >= 60:
            r, g, b = 220, 38, 38
            label = "HIGH RISK"
        elif score >= 30:
            r, g, b = 217, 119, 6
            label = "MEDIUM RISK"
        else:
            r, g, b = 5, 150, 105
            label = "LOW RISK"

        # Badge background
        self.set_fill_color(r, g, b)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        badge_text = f"  {verdict}  -  {label}  "
        self.cell(0, 12, badge_text, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        # Score bar
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 60)
        self.cell(0, 8, f"Risk Score: {score} / 100", new_x="LMARGIN", new_y="NEXT")

        # Draw score bar
        bar_x = 10
        bar_y = self.get_y()
        bar_w = 190
        bar_h = 6

        # Background
        self.set_fill_color(230, 230, 235)
        self.rect(bar_x, bar_y, bar_w, bar_h, "F")

        # Fill
        self.set_fill_color(r, g, b)
        fill_w = max(2, (score / 100) * bar_w)
        self.rect(bar_x, bar_y, fill_w, bar_h, "F")
        self.ln(10)

    def add_reason(self, index, reason):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(180, 50, 50)
        self.cell(8, 7, str(index) + ".")
        self.set_text_color(60, 60, 80)
        self.multi_cell(0, 7, reason)
        self.ln(1)

    def add_safe_note(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(5, 150, 105)
        self.cell(8, 7, "+")
        self.set_text_color(60, 60, 80)
        self.multi_cell(0, 7, text)
        self.ln(1)


def generate_report(user_input, analysis_result, features=None):
    """
    Generate a PDF threat analysis report.
    """
    pdf = NigraniReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    # ── Report Meta ────────────────────────────────────────
    pdf.add_section_title("Report Details")
    pdf.add_key_value("Report ID", f"NGR-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    pdf.add_key_value("Generated At", datetime.now().strftime("%d %B %Y, %I:%M %p IST"))
    pdf.add_key_value("Analysis Type", (analysis_result.get("type", "url")).upper())
    pdf.ln(4)

    # ── Input Analysed ─────────────────────────────────────
    pdf.add_section_title("Input Analysed")
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(40, 40, 60)
    pdf.set_fill_color(245, 245, 250)
    pdf.multi_cell(0, 6, sanitize_text(user_input), border=1, fill=True)
    pdf.ln(6)

    # ── Verdict ────────────────────────────────────────────
    pdf.add_section_title("Verdict & Risk Score")
    score = analysis_result.get("score", 0)
    verdict = analysis_result.get("verdict", "UNKNOWN")
    pdf.add_verdict_badge(verdict, score)

    # ── AI Machine Learning Analysis ───────────────────────
    ml_confidence = analysis_result.get("dl_confidence") or analysis_result.get("ml_verdict")
    if ml_confidence:
        pdf.add_section_title("AI Machine Learning Analysis")
        pdf.set_font("Courier", "B", 10)
        pdf.set_text_color(255, 255, 255)
        
        is_scam = "SCAM" in str(ml_confidence).upper() or float(str(ml_confidence).replace("%","").split("(")[-1].replace(")","")) > 50 if "(" in str(ml_confidence) else ("%" in str(ml_confidence) and float(str(ml_confidence).replace("%","")) > 50)
        
        if is_scam:
            pdf.set_fill_color(220, 38, 38)  # Red
        else:
            pdf.set_fill_color(5, 150, 105)  # Green
            
        pdf.cell(0, 10, f"  Neural Network / ML Confidence: {sanitize_text(str(ml_confidence))}  ", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

    # ── Threat Indicators ──────────────────────────────────
    reasons = analysis_result.get("reasons", [])
    pdf.add_section_title("Threat Indicators")
    if reasons:
        for i, reason in enumerate(reasons, 1):
            pdf.add_reason(i, sanitize_text(reason))
    else:
        pdf.add_safe_note("No threat indicators detected. This input appears safe.")
    pdf.ln(4)

    # ── Feature Breakdown (for URLs) ───────────────────────
    if features:
        pdf.add_section_title("Detailed Feature Breakdown")

        feature_descriptions = {
            "uses_https": "HTTPS Encryption (1 = Encrypted, 0 = Plain Text)",
            "url_length": "URL Length (total characters)",
            "subdomain_count": "Subdomain Count (nested domain levels)",
            "has_ip": "Uses IP Address (1 = Raw IP, 0 = Named domain)",
            "has_at": "Contains @ Symbol (1 = Redirect trick present)",
            "hyphen_count": "Hyphen Count (fake domain indicator)",
            "suspicious_tld": "Suspicious TLD (1 = High-risk top-level domain)",
            "domain_entropy": "Domain Entropy (randomness score)",
            "is_brand_lookalike": "Brand Impersonation (1 = Brand lookalike)",
            "is_url_shortener": "URL Shortener (1 = Shortened URL)",
            "closest_brand": "Closest Brand Match",
            "brand_distance": "Brand Levenshtein Distance",
        }

        for key, value in features.items():
            if key in ("url",):
                continue
            desc = feature_descriptions.get(key, key)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(60, 60, 80)
            pdf.cell(50, 6, key)
            pdf.set_font("Courier", "B", 9)
            pdf.set_text_color(108, 99, 255)
            pdf.cell(20, 6, sanitize_text(value))
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(120, 120, 140)
            pdf.cell(0, 6, desc, new_x="LMARGIN", new_y="NEXT")

        pdf.ln(4)

    # ── Safety Recommendations ─────────────────────────────
    pdf.add_page()
    pdf.add_section_title("Safety Recommendations")

    recommendations = []
    if score >= 60:
        recommendations = [
            "DO NOT click this link or share any personal information.",
            "DO NOT enter any passwords, OTPs, or financial details.",
            "Report this URL to cybercrime.gov.in or call 1930.",
            "Block the sender and warn others about this scam.",
            "If you already clicked, change your passwords immediately.",
            "Enable two-factor authentication on all your accounts.",
        ]
    elif score >= 30:
        recommendations = [
            "Exercise caution - this link shows some suspicious patterns.",
            "Verify the sender's identity through a separate, trusted channel.",
            "Check the URL carefully for misspellings or unusual domains.",
            "Do not enter sensitive information until you verify the site.",
            "When in doubt, navigate to the official website directly.",
        ]
    else:
        recommendations = [
            "This input appears safe based on our analysis.",
            "Always remain vigilant - new scam patterns emerge daily.",
            "Keep your software and browsers updated for security patches.",
            "Enable two-factor authentication wherever possible.",
        ]

    for rec in recommendations:
        if score < 30:
            pdf.add_safe_note(rec)
        else:
            pdf.add_reason("!", rec)
    pdf.ln(4)

    # ── About NIGRANI ──────────────────────────────────────
    pdf.add_section_title("About NIGRANI")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    about_text = (
        "NIGRANI (meaning 'Vigilance' in Hindi) is an AI-powered cybersecurity tool that detects "
        "phishing URLs and scam messages using feature engineering, rule-based heuristics, and "
        "machine learning classification. It analyses 15+ threat signals including HTTPS status, "
        "domain entropy, brand impersonation, suspicious TLDs, and more to provide explainable "
        "risk assessments.\n\n"
        "Built with Python, Flask, Scikit-learn, and modern web technologies."
    )
    pdf.multi_cell(0, 5, about_text)
    pdf.ln(6)

    # ── Disclaimer ─────────────────────────────────────────
    pdf.set_fill_color(255, 250, 240)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 120, 60)
    disclaimer = (
        "Disclaimer: This report is generated by an automated AI system for informational purposes only. "
        "It does not constitute legal or professional cybersecurity advice. Always consult official sources "
        "and authorities for confirmed threat assessments."
    )
    pdf.multi_cell(0, 5, disclaimer, fill=True, border=1)

    return bytes(pdf.output())


if __name__ == "__main__":
    test_result = {
        "score": 75,
        "verdict": "DANGEROUS",
        "reasons": [
            "No HTTPS - traffic not encrypted",
            "High-risk TLD (.xyz/.top/.click etc)",
            "Looks like 'paytm' - brand impersonation",
        ],
        "type": "url",
        "ml_verdict": "SCAM",
    }
    test_features = {
        "uses_https": 0,
        "url_length": 42,
        "subdomain_count": 1,
        "has_ip": 0,
        "has_at": 0,
        "hyphen_count": 2,
        "suspicious_tld": 1,
        "domain_entropy": 3.2,
        "is_brand_lookalike": 1,
        "closest_brand": "paytm",
        "brand_distance": 1,
    }
    pdf_bytes = generate_report("http://paytm-kyc.verify-now.xyz/login", test_result, test_features)
    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)
    print(f"Test report successfully saved to test_report.pdf ({len(pdf_bytes)} bytes)")

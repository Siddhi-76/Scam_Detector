import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# --- Load data ---
df = pd.read_csv("data/feature_matrix.csv")
FEATURE_COLS = [
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
X = df[FEATURE_COLS].fillna(0)
y = df["label"]

# --- Split: 80% train, 20% test ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Train both models and compare ---
for name, model in [
    ("Decision Tree", DecisionTreeClassifier(max_depth=6, random_state=42)),
    ("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42)),
]:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n=== {name} ===")
    print(classification_report(y_test, y_pred, target_names=["Legit", "Scam"]))

# --- Save the best model (Random Forest usually wins) ---
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
joblib.dump(rf, "model.pkl")
print("\nModel saved as model.pkl")

# --- Feature importance plot ---
plt.figure(figsize=(8, 5))
plt.barh(FEATURE_COLS, rf.feature_importances_)
plt.title("Which features matter most?")
plt.tight_layout()
plt.savefig("feature_importance.png")
print("Saved feature_importance.png")

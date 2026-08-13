import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
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

print(f"Dataset: {len(df)} samples ({y.sum()} scam, {len(y) - y.sum()} legit)")
print("=" * 60)

# --- Split: 80% train, 20% test ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Train multiple models and compare ---
models = [
    ("Decision Tree", DecisionTreeClassifier(max_depth=6, random_state=42)),
    ("Random Forest", RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)),
    ("Gradient Boosting", GradientBoostingClassifier(n_estimators=150, max_depth=5, random_state=42)),
]

best_model = None
best_accuracy = 0
best_name = ""

for name, model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")

    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    print(f"  Test Accuracy: {acc:.4f}")
    print(f"  Cross-Val Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(classification_report(y_test, y_pred, target_names=["Legit", "Scam"]))

    if cv_scores.mean() > best_accuracy:
        best_accuracy = cv_scores.mean()
        best_model = model
        best_name = name

# --- Save the best model ---
print(f"\n{'*' * 60}")
print(f"  Best Model: {best_name} (CV Accuracy: {best_accuracy:.4f})")
print(f"{'*' * 60}")

# Retrain best model on full training data
best_model.fit(X_train, y_train)
joblib.dump(best_model, "model.pkl")
print(f"\nModel saved as model.pkl")

# --- Feature importance plot ---
if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
    indices = np.argsort(importances)

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(indices)), importances[indices], color='#6c63ff', edgecolor='#4a44b3')
    plt.yticks(range(len(indices)), [FEATURE_COLS[i] for i in indices], fontsize=11)
    plt.xlabel("Feature Importance", fontsize=12)
    plt.title(f"NIGRANI — Feature Importance ({best_name})", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("feature_importance.png", dpi=150)
    print("Saved feature_importance.png")

# --- Confusion Matrix ---
y_pred_final = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred_final)
print(f"\nConfusion Matrix:\n{cm}")
print(f"  True Negatives (Legit correctly identified): {cm[0][0]}")
print(f"  False Positives (Legit flagged as Scam):     {cm[0][1]}")
print(f"  False Negatives (Scam missed):               {cm[1][0]}")
print(f"  True Positives (Scam correctly caught):      {cm[1][1]}")

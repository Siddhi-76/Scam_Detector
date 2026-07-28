import pandas as pd
from url_features import extract_features

# Load raw URL lists
scam = pd.read_csv("data/scam_urls.csv")
legit = pd.read_csv("data/legit_urls.csv")

scam["label"] = 1  # 1 = scam
legit["label"] = 0  # 0 = legit

all_urls = pd.concat([scam, legit], ignore_index=True)

# Run feature extraction on every URL
features_list = []
for url in all_urls["url"]:
    try:
        f = extract_features(str(url))
        features_list.append(f)
    except:
        features_list.append({})

feature_df = pd.DataFrame(features_list)
feature_df["label"] = all_urls["label"].values

feature_df.to_csv("data/feature_matrix.csv", index=False)
print(f"Saved {len(feature_df)} rows to feature_matrix.csv")

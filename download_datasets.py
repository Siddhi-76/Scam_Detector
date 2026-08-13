import os
import pandas as pd
import requests
import io

def download_sms_dataset():
    print("Downloading SMS Spam Collection dataset...")
    # Using a reliable github mirror for the UCI SMS Spam Collection
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse TSV
        df = pd.read_csv(io.StringIO(response.text), sep='\t', header=None, names=['label_str', 'message'])
        
        # Convert labels: ham -> 0, spam -> 1
        df['label'] = df['label_str'].map({'ham': 0, 'spam': 1})
        df = df.drop('label_str', axis=1)
        
        # Save to our data folder
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/messages.csv", index=False)
        print(f"Successfully downloaded {len(df)} real SMS messages and saved to data/messages.csv")
    except Exception as e:
        print(f"Failed to download SMS dataset: {e}")

def download_url_dataset():
    print("Downloading Phishing URL dataset...")
    try:
        # Fetch scam URLs from OpenPhish feed
        response = requests.get("https://openphish.com/feed.txt", timeout=30)
        response.raise_for_status()
        
        scam_urls = response.text.strip().split('\n')
        df_bad = pd.DataFrame({"url": scam_urls, "label": 1})
        df_bad = df_bad.drop_duplicates()
        df_bad.to_csv("data/scam_urls.csv", index=False)
        print(f"Successfully processed {len(df_bad)} phishing URLs.")
        
        # We will use the existing legit_urls.csv for now (or a backup generation logic)
        if not os.path.exists("data/legit_urls.csv") or len(pd.read_csv("data/legit_urls.csv")) < 100:
            print("Generating benign URLs...")
            benign = ["https://google.com", "https://youtube.com", "https://facebook.com", "https://amazon.in",
                      "https://flipkart.com", "https://twitter.com", "https://instagram.com", "https://linkedin.com",
                      "https://wikipedia.org", "https://netflix.com", "https://apple.com", "https://microsoft.com"]
            # Augment with random paths
            augmented = []
            for _ in range(500):
                for b in benign:
                    augmented.append(b + "/page" + str(pd.np.random.randint(100, 999)))
            df_good = pd.DataFrame({"url": augmented, "label": 0})
            df_good.to_csv("data/legit_urls.csv", index=False)
            print(f"Successfully processed {len(df_good)} benign URLs.")
            
    except Exception as e:
        print(f"Failed to download URL dataset: {e}")

if __name__ == "__main__":
    download_sms_dataset()
    download_url_dataset()

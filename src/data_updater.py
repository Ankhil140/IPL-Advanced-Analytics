import urllib.request
import os

def download_real_ipl_data():
    # Widely available public mirror of the Kaggle IPL Dataset (matches.csv)
    url = "https://raw.githubusercontent.com/Shivaae/IPL-DATA-/main/matches.csv"
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "matches.csv")
    
    print("Downloading real historical IPL dataset...")
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"Dataset successfully downloaded and saved to: {output_path}")
        print("Run `python src/model.py` to retrain the ML engine on the real data.")
    except Exception as e:
        print(f"Failed to download dataset. Error: {e}")

if __name__ == "__main__":
    download_real_ipl_data()

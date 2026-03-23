import urllib.request
import os

def download_real_ipl_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    matches_url = "https://raw.githubusercontent.com/Shivaae/IPL-DATA-/main/matches.csv"
    deliveries_url = "https://raw.githubusercontent.com/Shivaae/IPL-DATA-/main/deliveries.csv"
    
    matches_path = os.path.join(base_dir, "data", "matches.csv")
    deliveries_path = os.path.join(base_dir, "data", "deliveries.csv")
    
    print("Downloading authentic historical IPL datasets. This may take a minute...")
    try:
        urllib.request.urlretrieve(matches_url, matches_path)
        print(f"matches.csv successfully saved to: {matches_path}")
        
        urllib.request.urlretrieve(deliveries_url, deliveries_path)
        print(f"deliveries.csv successfully saved to: {deliveries_path}")
        
        print("\nSUCCESS!")
        print("Run `python src/model.py` to retrain the ML engine.")
        print("Run `python src/player_stats_compiler.py` to serialize player data.")
    except Exception as e:
        print(f"Failed to download dataset. Error: {e}")

if __name__ == "__main__":
    download_real_ipl_data()

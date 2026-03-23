import requests
from bs4 import BeautifulSoup

def get_live_matches():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    try:
        # User agent is necessary so they don't block the request immediately
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'lxml')
        
        matches = []
        
        # Current live score cards usually reside in these containers
        match_divs = soup.find_all('div', class_='cb-mtch-lst')
        
        for div in match_divs:
            title = div.find('h3', class_='cb-lv-scr-mtch-hdr')
            score = div.find('div', class_='cb-lv-scrs-col') 
            status = div.find('div', class_='cb-text-complete') or div.find('div', class_='cb-text-live')
            
            if title:
                matches.append({
                    'title': title.text.strip(),
                    'score': score.text.strip() if score else "Score details unavailable",
                    'status': status.text.strip() if status else 'Match in Progress'
                })
                
        # If the classes have changed or there are no matches in that specific div
        if not matches:
            headers = soup.find_all('a', class_='text-hvr-underline')
            for h in headers[:5]:
                if "vs" in h.text.lower():
                    matches.append({
                        'title': h.text.strip(), 
                        'score': 'Live stats on Cricbuzz', 
                        'status': 'Check live updates'
                    })
                
        return matches
    except Exception as e:
        print(f"Error scraping live matches: {e}")
        return []

if __name__ == "__main__":
    print(get_live_matches())

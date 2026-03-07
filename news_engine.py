import requests
from bs4 import BeautifulSoup
import ollama

# --- CONFIGURATION ---
GROUPME_BOT_ID = ""
MODEL_NAME = "llama3"

def scrape_cyber_news():
    #Scrapes top headlines from common cyber news sites
    headlines = []
    sources = [
        "https://thehackernews.com/",
        "https://www.bleepingcomputer.com/",
        "https://www.cisa.gov/news-events/cybersecurity-advisories",
        "https://www.darkreading.com/",
        "https://krebsonsecurity.com/"
    ]
    
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            if "hacker" in url:
                # The Hacker News titles
                tags = soup.find_all('h2', class_='home-title')[:3]
            else:
                # BleepingComputer titles
                tags = soup.find_all('h4')[:3]
                
            for tag in tags:
                headlines.append(tag.text.strip())
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            
    return headlines

def generate_brief(headlines):
    #Uses Llama 3 to turn raw headlines into a student brief
    prompt = (
        f"You are a cybersecurity expert. Summarize these headlines into a short, "
        f"bulleted 'Morning Cyber Brief' for students. Explain the 'why it matters' "
        f"for each. Headlines: {headlines}"
    )
    
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

def send_to_groupme(text):
    """Sends the final brief to GroupMe."""
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": GROUPME_BOT_ID,
        "text": text
    }
    response = requests.post(url, json=data)
    return response.status_code

if __name__ == "__main__":
    print("Scraping news...")
    raw_news = scrape_cyber_news()
    
    print("Asking Llama to summarize...")
    final_brief = generate_brief(raw_news)
    
    print("Sending to GroupMe...")
    status = send_to_groupme(final_brief)
    
    if status == 202:
        print("Success! Message sent.")
    else:
        print(f"Failed to send. Status: {status}")
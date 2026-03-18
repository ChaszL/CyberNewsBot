import requests
from bs4 import BeautifulSoup
import ollama

# GroupMe bot ID and Llama model
GROUPME_BOT_ID = ""
MODEL_NAME = "llama3"

# Scapes news headlines from cybersecurity news sites and returns those headlines as a list
def scrape_cyber_news():
    # Headlines list and Source URLs dictionary with CSS headline selectors
    headlines = []
    sources = {
        "https://thehackernews.com/": "h2.home-title",
        "https://www.bleepingcomputer.com/": "h4",
    }
    
    # Scapes the top headline from each source and adds it to the headlines list
    for url, tag_selector in sources.items():
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            tags = soup.select(tag_selector)[:3]
                
            # for every headline found, it will be added to the headline list
            for tag in tags:
                headlines.append(tag.text.strip())

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Print obtained headlines and return the list
    print(f"Scraped headlines: {headlines}")
    return headlines

# Uses Llama 3 to turn raw headlines into a student brief
def generate_brief(headlines):
    prompt = (
        f"You are a cybersecurity expert. Summarize these headlines into a short, "
        f"bulleted 'Morning Cyber Brief' for students. Explain the 'why it matters' "
        f"for each. Headlines: {headlines} and this is for students on a groupme chat."
        f"Please make sure the brief is below 800 characters and shows the most important information with headings being all caps"
    )
    
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

# Sends the final brief to GroupMe.
def send_to_groupme(text):
    # GroupMe API endpoint and payload
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": GROUPME_BOT_ID,
        "text": text
    }
    response = requests.post(url, json=data)
    return response.status_code

# Main execution
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

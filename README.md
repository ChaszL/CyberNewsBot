CyberNews-GroupMe-Bot 🤖🛡️
A Python-based automation tool that scrapes the latest cybersecurity headlines, summarizes them using Ollama (Llama 3), and broadcasts a "Morning Cyber Brief" to a GroupMe student chat.

🚀 Features
Multi-Source Scraping: Pulls headlines from The Hacker News, BleepingComputer, and CISA.

AI Summarization: Uses a local Llama 3 instance to contextualize "why it matters" for students.

GroupMe Integration: Automatically posts the brief via the GroupMe Bot API.

Error Handling: Built-in try-except blocks to handle connection timeouts or site changes.

🛠️ Tech Stack
Language: Python 3.x

Web Scraping: BeautifulSoup4, requests

AI/LLM: ollama (Llama 3)

API: GroupMe Bot API

📋 Prerequisites
Ollama: You must have Ollama installed and the Llama 3 model downloaded:

Bash
ollama pull llama3
GroupMe Bot ID: Create a bot at the GroupMe Developers portal and save your Bot ID.

🔧 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/your-username/cybernews-groupme-bot.git
cd cybernews-groupme-bot
Install dependencies:

Bash
pip install requests beautifulsoup4 ollama
Configure the Script:
Open bot.py and replace the GROUPME_BOT_ID variable with your actual ID:

Python
GROUPME_BOT_ID = "your_actual_bot_id_here"
🖥️ Usage
Run the script manually or schedule it (via Cron or Task Scheduler) to send daily updates:

Bash
python bot.py
How it Works (Logic Flow)
scrape_cyber_news(): Sends HTTP GET requests to news sites. It parses the HTML using CSS selectors and stores the top 3 headlines per site into a list.

generate_brief(): Passes the list of headlines to the Llama 3 model with a custom system prompt designed for students.

send_to_groupme(): Sends the AI-generated string to the GroupMe API endpoint.

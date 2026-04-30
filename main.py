import requests
from bs4 import BeautifulSoup
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "8463282045:AAGmCnljPnbU1MEtH4g-Emfap_2qgnBUm_U"
CHAT_ID = "8586986001"
last_project_url = ""

def check_kafeel():
    global last_project_url
    url = "https://kafeel.me/projects?category=1" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        project_h3 = soup.find('h3')
        project_link_tag = project_h3.find('a') if project_h3 else None
        
        if project_link_tag:
            project_title = project_link_tag.text.strip()
            project_url = "https://kafeel.me" + project_link_tag['href']

            if project_url != last_project_url:
                message = f"New Project Found!\n\nTitle: {project_title}\nLink: {project_url}"
                telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
                requests.get(telegram_url)
                
                last_project_url = project_url
                print(f"Sent: {project_title}")
        else:
            print("Watching...")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        check_kafeel()
        time.sleep(60)

import requests
import os
from dotenv import load_dotenv

# .env dosyasındaki API anahtarı ve veritabanı ID'sini yükle
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")   

# Notion API sabitleri
NOTION_VERSION = "2022-06-28"
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

# Notion'dan verileri çek
def get_notion_data():
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        for page in results:
            props = page["properties"]
            print("-----")
            for key, value in props.items():
                value_type = value.get("type")
                if value_type == "title":
                    print(f"{key}: {value['title'][0]['plain_text'] if value['title'] else ''}")
                elif value_type == "rich_text":
                    print(f"{key}: {value['rich_text'][0]['plain_text'] if value['rich_text'] else ''}")
                elif value_type == "checkbox":
                    print(f"{key}: {'✅' if value['checkbox'] else '❌'}")
                elif value_type == "date":
                    print(f"{key}: {value['date']['start'] if value['date'] else ''}")
    else:
        print("Hata oluştu:", response.status_code, response.text)

# Çalıştır
if __name__ == "__main__":
    get_notion_data()
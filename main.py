from flask import Flask, render_template_string
import requests
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"

app = Flask(__name__)

@app.route("/")
def index():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    items = []
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        for page in results:
            props = page["properties"]
            name = props.get("Name", {}).get("title", [])
            title = name[0]["plain_text"] if name else ""
            date = props.get("Date", {}).get("date", {})
            start = date.get("start", "")
            end = date.get("end", "")
            items.append({
                "title": title,
                "start": start,
                "end": end
            })
    else:
        return f"Error: {response.status_code} - {response.text}"

    # HTML şablonu
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Notion Verileri</title>
    </head>
    <body>
        <h1>Notion Verileri</h1>
        <ul>
        {% for item in items %}
            <li>
                <strong>{{ item.title or 'Başlıksız' }}</strong><br>
                Başlangıç: {{ item.start or '-' }}<br>
                Bitiş: {{ item.end or '-' }}
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

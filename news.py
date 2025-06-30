from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_google_finance_news_rss(query="金融"):
    url = f"https://news.google.com/rss/search?q={query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item")[:10]  # 顯示 10 則新聞
    news_list = []
    for item in items:
        title = item.title.text
        link = item.link.text
        news_list.append({"title": title, "link": link})
    return news_list

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "金融")
    news = fetch_google_finance_news_rss(query)
    return render_template("index.html", news=news, query=query)

if __name__ == "__main__":
    app.run(debug=True)
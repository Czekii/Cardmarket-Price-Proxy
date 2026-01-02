from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/price")
def price():
    url = request.args.get("url")
    if not url:
        return "Missing url", 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return f"Request error: {e}", 500

    if r.status_code != 200:
        return f"Error {r.status_code}", 500

    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    dds = soup.select("#tabContent-info dl dd")
    if len(dds) < 20:
        return "Not found", 404

    raw_price = dds[19].get_text(strip=True)
    return raw_price

app.run(host="0.0.0.0", port=8080)

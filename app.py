from flask import Flask, render_template
from threading import Thread
import requests
import time

app = Flask(__name__)
txs = []

@app.route("/")
def home():
    return render_template("home.html", txs=txs.reverse())

def run():
    app.run(host="0.0.0.0", port=8080)

t = Thread(target=run)
t.start()

def claim_faucet():
    try:
        response = requests.post("https://faucet.testnet.humanity.org/api/claim", json={"address": "0x01fdc84aa8074f74794E095AE9347b6538817050"})
        if response.status_code == 200:
            response2 = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Kolkata")
            if response2.status_code == 200:
                global txs
                txs.append({'date': response2.json()["date"], 'time': response2.json()["time"], 'txhash': response.json()["msg"]})
    except Exception as e:
        print(f"Error occurred: {e}")

while True:
    claim_faucet()
    time.sleep(60)

from flask import Flask, render_template
from threading import Thread
import requests
import time

app = Flask(__name__)
txs = []

@app.route("/")
def home():
    reversed_txs = list(reversed(txs))
    return render_template("home.html", txs=reversed_txs)

def run():
    app.run(host="0.0.0.0", port=8080)

t = Thread(target=run)
t.start()

def claim_faucet():
    global txs
    time = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Kolkata")
    attempts = 0
    while attempts < 100:
        try:
            attempts += 1
            response = requests.post("https://faucet.testnet.humanity.org/api/claim", json={"address": "0x01fdc84aa8074f74794E095AE9347b6538817050"})
            if response.status_code == 200:
                txs.append({'date': time.json()["date"], 'time': time.json()["time"], 'txhash': response.json()["msg"], 'wallet': '0x01fdc84aa8074f74794E095AE9347b6538817050'})
                break
        except Exception as e:
            print(f"Error occurred: {e}")
    attempts = 0
    while attempts < 100:
        try:
            attempts += 1
            response = requests.post("https://faucet.testnet.humanity.org/api/claim", json={"address": "0x673fcF2440FDe7A154150bAb04853A4583bE9d69"})
            if response.status_code == 200:
                txs.append({'date': time.json()["date"], 'time': time.json()["time"], 'txhash': response.json()["msg"], 'wallet': '0x673fcF2440FDe7A154150bAb04853A4583bE9d69'})
                break
        except Exception as e:
            print(f"Error occurred: {e}")

while True:
    claim_faucet()
    time.sleep(60)

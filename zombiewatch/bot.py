import os
import json
import httpx
from ape import Contract
from silverback import SilverbackBot

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
CONTRACT_ADDRESS = os.environ.get("CONTRACT_ADDRESS", "0x5FbDB2315678afecb367f032d93F642f64180aa3")

ARTIFACT_PATH = os.path.join(
    os.path.dirname(__file__),
    "../artifacts/contracts/zombieownership.sol/ZombieOwnership.json"
)
with open(ARTIFACT_PATH) as f:
    abi = json.load(f)["abi"]

bot = SilverbackBot()

contract = Contract(CONTRACT_ADDRESS, abi=abi)


def send_telegram(msg: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    httpx.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})


@bot.on_startup()
def handle_startup(state):
    send_telegram(f"🧟 zombieWatch is live — watching {CONTRACT_ADDRESS}")
    print(f"Watching contract: {CONTRACT_ADDRESS}")


@bot.on_(contract.NewZombie)
def handle_new_zombie(log):
    msg = (
        f"🧟 New Zombie Created!\n"
        f"ID: {log.zombieId}\n"
        f"Name: {log.name}\n"
        f"DNA: {log.dna}"
    )
    send_telegram(msg)
    print(msg)


@bot.on_shutdown()
def handle_shutdown():
    send_telegram("🔴 zombieWatch stopped.")

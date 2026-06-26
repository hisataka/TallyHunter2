import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")


def get_port():
    return int(os.getenv("PORT", 10000))

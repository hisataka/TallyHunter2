from flask import Flask

from .config import get_port

app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"


def run_web_server():
    app.run(host='0.0.0.0', port=get_port())

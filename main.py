from threading import Thread

from app.bot import bot
from app.config import TOKEN
from app.web import run_web_server


def main():
    Thread(target=run_web_server, daemon=True).start()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()

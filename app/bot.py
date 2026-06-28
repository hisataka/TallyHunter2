import datetime

import time

import discord
from discord.ext import commands, tasks

from .extreme.commands import register as register_extreme
from .extreme.views import ExtremeTrialView
from .hunt.commands import register as register_hunt
from .hunt.views import HuntView, ResultView
from .utils import get_data_field
from .help.commands import register as register_help
from .artifact.commands import register as register_artifact
from .artifact.views import ArtifactView

class HuntBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self):
        self.add_view(HuntView())
        self.add_view(ResultView())  # デフォルト引数で初期化可能に
        self.add_view(ExtremeTrialView())
        self.add_view(ArtifactView())
        self.auto_end.start()
        await self.tree.sync()

#    @tasks.loop(seconds=30)
#    async def auto_end(self):
#        for guild in self.guilds:
#            for channel in guild.text_channels:
#                async for msg in channel.history(limit=50):
#                    if msg.author == self.user and msg.embeds and "_data" in [f.name for f in msg.embeds[0].fields]:
#                        data = get_data_field(msg).split('|')
#                        if time.time() > int(data[1]) and "\U0001F3C6" in msg.embeds[0].title:
#                            await HuntView().end_hunt_logic(msg)
    @tasks.loop(seconds=30)
    async def auto_end(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                try:
                    # limit=50 → 200 に拡大。さらに「直近24時間以内」だけスキャン
                    after = discord.utils.utcnow() - datetime.timedelta(days=1)
                    async for msg in channel.history(limit=200, after=after):
                        if (msg.author == self.user
                                and msg.embeds
                                and "_data" in [f.name for f in msg.embeds[0].fields]):
                            data = get_data_field(msg).split('|')
                            if time.time() > int(data[1]) and "\U0001F3C6" in msg.embeds[0].title:
                                await HuntView().end_hunt_logic(msg)
                except (discord.Forbidden, discord.HTTPException):
                    # 権限不足チャンネル等は黙ってスキップ（ループ自体は止めない）
                    continue

def create_bot():
    new_bot = HuntBot()
    register_hunt(new_bot)
    register_extreme(new_bot)
    register_help(new_bot)
    register_artifact(new_bot)
    return new_bot


bot = create_bot()

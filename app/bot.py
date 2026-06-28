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

    @tasks.loop(seconds=15)
    async def auto_end(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                try:
                    after = discord.utils.utcnow() - datetime.timedelta(days=1)

                    async for msg in channel.history(limit=200, after=after):
                        # Bot投稿以外はスキップ
                        if msg.author != self.user:
                            continue

                        # embedなし
                        if not msg.embeds:
                            continue

                        embed = msg.embeds[0]

                        # _dataフィールドなし
                        if "_data" not in [f.name for f in embed.fields]:
                            continue

                        title = embed.title or ""

                        # 狩猟大会以外は無視
                        if not title.startswith("🏆 狩猟大会中:"):
                            continue

                        data = get_data_field(msg).split('|')

                        # Hunt format:
                        # score|end_time|host_id|is_host_mode|counts
                        if len(data) < 5:
                            continue

                        try:
                            end_time = int(data[1])
                        except ValueError:
                            continue

                        if time.time() > end_time:
                            await HuntView().end_hunt_logic(msg)

                except (discord.Forbidden, discord.HTTPException):
                    continue

def create_bot():
    new_bot = HuntBot()
    register_hunt(new_bot)
    register_extreme(new_bot)
    register_help(new_bot)
    register_artifact(new_bot)
    return new_bot


bot = create_bot()

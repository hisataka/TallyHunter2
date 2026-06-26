import asyncio

import time

import discord

from ..constants import POINTS
from .views import HuntView


def register(bot):
    @bot.tree.command(name="start-hunt", description="狩猟大会を開始")
    async def start(interaction: discord.Interaction, team_name: str, minutes: int = 15, is_host_mode: bool = False):
        end_t = int(time.time()) + (minutes * 60)
        counts = {k: 0 for k in POINTS.keys()}
        view = HuntView()
        await interaction.response.send_message(
            embed=view.get_embed(team_name, 0, counts, end_t, interaction.user.id, is_host_mode),
            view=view,
        )
        message = await interaction.original_response()
        asyncio.create_task(view.schedule_auto_end(message, end_t)

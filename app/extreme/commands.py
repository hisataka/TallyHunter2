import discord

from .embeds import build_extreme_embed
from .views import ExtremeTrialView


def register(bot):
    """極限編成トライアル関連のスラッシュコマンドを bot に登録する。"""

    @bot.tree.command(name="extreme-trial", description="極限編成トライアルを開始")
    async def extreme_trial(
        interaction: discord.Interaction,
        team_name: str,
        time_limit: int = 180,
        is_host_mode: bool = False,
    ):
        view = ExtremeTrialView()

        initial_data = (
            f"150.0,0,0,0,0,0,0,0,60,"
            f"{time_limit},"
            f"{interaction.user.id},"
            f"{int(is_host_mode)}"
        )

        embed = build_extreme_embed(team_name, initial_data)

        await interaction.response.send_message(
            embed=embed,
            view=view,
        )

import discord

from .embeds import build_artifact_embed
from .views import ArtifactView


def register(bot):
    @bot.tree.command(
        name="artifact-score",
        description="聖遺物スコアを計算",
    )
    async def artifact_score(
        interaction: discord.Interaction,
        character_name: str,
        is_host_mode: bool = False,
    ):
        data_str = (
            "0,0,0,0,0"
            f"|{interaction.user.id}"
            f"|{int(is_host_mode)}"
        )

        embed = build_artifact_embed(
            character_name,
            data_str,
        )

        await interaction.response.send_message(
            embed=embed,
            view=ArtifactView(),
        )
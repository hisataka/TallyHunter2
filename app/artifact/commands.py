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

        score_str = "0,0,0,0,0"
        raw_input_str = ";".join(["0,0,0"] * 5)

        data_str = (
            score_str
            + "|"
            + raw_input_str
            + f"|{interaction.user.id}"
            + f"|{int(is_host_mode)}"
        )

        embed = build_artifact_embed(
            character_name,
            data_str,
        )

        await interaction.response.send_message(
            embed=embed,
            view=ArtifactView(),
        )
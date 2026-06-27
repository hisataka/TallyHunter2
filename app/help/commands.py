import discord
from .embeds import build_help_embed


def register(bot):
    @bot.tree.command(name="help", description="ヘルプを表示")
    async def help_command(interaction: discord.Interaction):
        embed = build_help_embed()
        await interaction.response.send_message(embed=embed)
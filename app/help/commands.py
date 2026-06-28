from .embeds import build_help_top_embed
from .views import HelpView


def register(bot):
    @bot.tree.command(name="help", description="ヘルプを表示")
    async def help_command(interaction):
        await interaction.response.send_message(
            embed=build_help_top_embed(),
            view=HelpView(),
        )
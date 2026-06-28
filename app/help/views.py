import discord
from .embeds import *


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def show_top(self, interaction):
        await interaction.response.edit_message(
            embed=build_help_top_embed(),
            view=self
        )

    @discord.ui.button(label="狩猟大会", emoji="🏹", style=discord.ButtonStyle.danger)
    async def hunt(self, interaction, button):
        await interaction.response.edit_message(
            embed=build_hunt_help_embed(),
            view=HelpBackView(),
        )

    @discord.ui.button(label="極限編成", emoji="⚔️", style=discord.ButtonStyle.primary)
    async def extreme(self, interaction, button):
        await interaction.response.edit_message(
            embed=build_extreme_help_embed(),
            view=HelpBackView(),
        )

    @discord.ui.button(label="聖遺物", emoji="⭐", style=discord.ButtonStyle.success)
    async def artifact(self, interaction, button):
        await interaction.response.edit_message(
            embed=build_artifact_help_embed(),
            view=HelpBackView(),
        )


class HelpBackView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="戻る", emoji="⬅️", style=discord.ButtonStyle.secondary)
    async def back(self, interaction, button):
        await interaction.response.edit_message(
            embed=build_help_top_embed(),
            view=HelpView(),
        )
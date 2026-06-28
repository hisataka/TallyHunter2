import discord

from .embeds import (
    build_help_top_embed,
    build_hunt_help_embed,
    build_extreme_help_embed,
    build_artifact_help_embed,
)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        self.back.disabled = True

    @discord.ui.button(
        label="狩猟大会",
        emoji="🏹",
        style=discord.ButtonStyle.danger,
        row=0,
    )
    async def hunt(self, interaction, button):
        self.back.disabled = False
        await interaction.response.edit_message(
            embed=build_hunt_help_embed(),
            view=self,
        )

    @discord.ui.button(
        label="極限編成",
        emoji="⚔️",
        style=discord.ButtonStyle.primary,
        row=0,
    )
    async def extreme(self, interaction, button):
        self.back.disabled = False
        await interaction.response.edit_message(
            embed=build_extreme_help_embed(),
            view=self,
        )

    @discord.ui.button(
        label="聖遺物",
        emoji="⭐",
        style=discord.ButtonStyle.success,
        row=0,
    )
    async def artifact(self, interaction, button):
        self.back.disabled = False
        await interaction.response.edit_message(
            embed=build_artifact_help_embed(),
            view=self,
        )

    @discord.ui.button(
        label="戻る",
        emoji="⬅️",
        style=discord.ButtonStyle.secondary,
        row=1,
    )
    async def back(self, interaction, button):
        self.back.disabled = True
        await interaction.response.edit_message(
            embed=build_help_top_embed(),
            view=self,
        )
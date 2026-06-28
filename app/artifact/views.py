import discord

from ..utils import (
    NUMBER_REQUIRED_MESSAGE,
    PERMISSION_DENIED_MESSAGE,
    get_data_field,
    is_authorized,
)
from .embeds import (
    ARTIFACT_TITLE_PREFIX,
    PARTS,
    build_artifact_embed,
)
from .scoring import calculate_artifact_score


def get_artifact_meta(message):
    data = get_data_field(message).split("|")

    scores = data[0].split(",")
    host_id = int(data[1])
    is_host_mode = bool(int(data[2]))

    return scores, host_id, is_host_mode


def _character_name_from_message(message):
    return message.embeds[0].title.replace(
        ARTIFACT_TITLE_PREFIX,
        "",
    )


class ArtifactModal(discord.ui.Modal):
    def __init__(self, message, index):
        super().__init__(title=f"{PARTS[index]} 入力")

        self.message = message
        self.index = index

        self.cd = discord.ui.TextInput(
            label="会心ダメージ",
            placeholder="例: 21.8",
            required=True,
        )

        self.atk = discord.ui.TextInput(
            label="攻撃力%",
            placeholder="例: 11.1",
            required=True,
        )

        self.cr = discord.ui.TextInput(
            label="会心率",
            placeholder="例: 7.8",
            required=True,
        )

        self.add_item(self.cd)
        self.add_item(self.atk)
        self.add_item(self.cr)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            cd = float(self.cd.value)
            atk = float(self.atk.value)
            cr = float(self.cr.value)
        except ValueError:
            return await interaction.response.send_message(
                NUMBER_REQUIRED_MESSAGE,
                ephemeral=True,
            )

        score = calculate_artifact_score(cd, atk, cr)

        scores, host_id, is_host_mode = get_artifact_meta(
            self.message
        )

        scores[self.index] = str(score)

        new_data = (
            ",".join(scores)
            + f"|{host_id}|{int(is_host_mode)}"
        )

        character_name = _character_name_from_message(
            interaction.message
        )

        embed = build_artifact_embed(
            character_name,
            new_data,
        )

        await interaction.response.edit_message(
            embed=embed,
            view=ArtifactView(),
        )


class ArtifactView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def _open_modal(self, interaction, idx):
        _, host_id, is_host_mode = get_artifact_meta(
            interaction.message
        )

        if not is_authorized(
            interaction,
            host_id,
            is_host_mode,
        ):
            return await interaction.response.send_message(
                PERMISSION_DENIED_MESSAGE,
                ephemeral=True,
            )

        await interaction.response.send_modal(
            ArtifactModal(interaction.message, idx)
        )

    @discord.ui.button(
        label="花",
        style=discord.ButtonStyle.secondary,
        custom_id="artifact_0",
    )
    async def flower(self, interaction, button):
        await self._open_modal(interaction, 0)

    @discord.ui.button(
        label="羽",
        style=discord.ButtonStyle.secondary,
        custom_id="artifact_1",
    )
    async def feather(self, interaction, button):
        await self._open_modal(interaction, 1)

    @discord.ui.button(
        label="時計",
        style=discord.ButtonStyle.primary,
        custom_id="artifact_2",
    )
    async def sands(self, interaction, button):
        await self._open_modal(interaction, 2)

    @discord.ui.button(
        label="杯",
        style=discord.ButtonStyle.primary,
        custom_id="artifact_3",
    )
    async def goblet(self, interaction, button):
        await self._open_modal(interaction, 3)

    @discord.ui.button(
        label="冠",
        style=discord.ButtonStyle.success,
        custom_id="artifact_4",
    )
    async def circlet(self, interaction, button):
        await self._open_modal(interaction, 4)
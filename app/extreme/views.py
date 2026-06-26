import discord

from ..utils import PERMISSION_DENIED_MESSAGE, get_data_field, is_authorized
from .embeds import build_extreme_embed
from .scoring import calculate_extreme_score

EXTREME_TITLE_PREFIX = "極限編成トライアル: "

TRIAL_INPUT_LABELS = [
    ["①聖遺物スコア", "②☆5キャラ人数", "③最大凸数", "④その他凸合計"],
    ["⑤☆5武器数", "⑥☆3武器数", "⑦最多凸武器精錬", "⑧その他武器精錬合計", "⑨討伐タイム(秒)"],
]


def get_trial_meta(message):
    data = get_data_field(message).split(',')
    host_id = int(data[10])
    is_host_mode = bool(int(data[11]))
    return host_id, is_host_mode


def _team_name_from_message(message):
    return message.embeds[0].title.replace(EXTREME_TITLE_PREFIX, "")


class TrialEditModal(discord.ui.Modal):
    def __init__(self, message, part):
        title = "極限トライアル入力1" if part == 1 else "極限トライアル入力2"
        super().__init__(title=title)

        self.message = message
        self.part = part

        data = get_data_field(message).split(',')
        self.d = data
        self.inputs = []

        labels = TRIAL_INPUT_LABELS

        for label in labels[part - 1]:
            idx = labels[0].index(label) if part == 1 else labels[1].index(label) + 4
            ti = discord.ui.TextInput(
                label=label,
                default=str(self.d[idx]),
                style=discord.TextStyle.short,
            )
            self.add_item(ti)
            self.inputs.append(ti)

    async def on_submit(self, i):
        new_d = self.d[:]

        for idx, ti in enumerate(self.inputs):
            target_idx = idx if self.part == 1 else idx + 4
            new_d[target_idx] = ti.value

        data_str = ",".join(new_d)
        team_name = _team_name_from_message(i.message)
        embed = build_extreme_embed(team_name, data_str)
        await i.response.edit_message(embed=embed)


class ExtremeTrialView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def _open_input_modal(self, i, part):
        host_id, is_host_mode = get_trial_meta(i.message)
        if not is_authorized(i, host_id, is_host_mode):
            return await i.response.send_message(PERMISSION_DENIED_MESSAGE, ephemeral=True)
        await i.response.send_modal(TrialEditModal(i.message, part))

    @discord.ui.button(label="入力1", style=discord.ButtonStyle.primary, custom_id="tr_1")
    async def b1(self, i, b):
        await self._open_input_modal(i, 1)

    @discord.ui.button(label="入力2", style=discord.ButtonStyle.primary, custom_id="tr_2")
    async def b2(self, i, b):
        await self._open_input_modal(i, 2)

    @discord.ui.button(label="計算実行", style=discord.ButtonStyle.success, custom_id="tr_calc")
    async def b3(self, i, b):
        host_id, is_host_mode = get_trial_meta(i.message)

        if not is_authorized(i, host_id, is_host_mode):
            return await i.response.send_message(PERMISSION_DENIED_MESSAGE, ephemeral=True)

        data_str = get_data_field(i.message)
        d_list = data_str.split(',')

        d = {
            'artifact_score': float(d_list[0]),
            'char_count': int(d_list[1]),
            'max_c_const': int(d_list[2]),
            'sum_c_const': int(d_list[3]),
            'w5_count': int(d_list[4]),
            'w3_count': int(d_list[5]),
            'max_w_refine': int(d_list[6]),
            'sum_w_refine': int(d_list[7]),
            'time': int(d_list[8]),
            'time_limit': int(d_list[9]),
        }

        score, a, c, w = calculate_extreme_score(d)

        team_name = _team_name_from_message(i.message)

        embed = build_extreme_embed(team_name, data_str, (score, a, c, w))

        await i.response.edit_message(embed=embed)

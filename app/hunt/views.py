import asyncio

import time

import discord

from ..constants import BOSS_MAPPING, POINTS
from ..utils import (
    HUNT_ENDED_MESSAGE,
    NUMBER_REQUIRED_MESSAGE,
    PERMISSION_DENIED_MESSAGE,
    get_data_field,
    is_authorized,
)

# 修正モーダルが対象とするカテゴリ
HUNT_TARGETS = ["SS", "S", "A", "B", "C"]
HILLY_TARGETS = ["変ヒル"]
COLLECT_TARGETS = ["釣り", "豪華", "貴重", "普通&精巧", "原型"]


def _team_name_from_message(message):
    """埋め込みタイトルからチーム名部分を取り出す。"""
    return message.embeds[0].title.split(': ')[-1]


class EditModal(discord.ui.Modal):
    def __init__(self, message, end_time, host_id, is_host_mode, counts, targets, title):
        super().__init__(title=title)
        self.message, self.end_time = message, end_time
        self.host_id, self.is_host_mode = host_id, is_host_mode
        self.inputs = {}
        for k in targets:
            ti = discord.ui.TextInput(label=k, default=str(counts[k]), placeholder='0', required=True)
            self.add_item(ti)
            self.inputs[k] = ti

    async def on_submit(self, i: discord.Interaction):
        if not is_authorized(i, self.host_id, self.is_host_mode):
            return await i.response.send_message(PERMISSION_DENIED_MESSAGE, ephemeral=True)
        counts = ResultView.get_counts_static(self.message)
        try:
            for k, ti in self.inputs.items():
                counts[k] = int(ti.value)
        except ValueError:
            return await i.response.send_message(NUMBER_REQUIRED_MESSAGE, ephemeral=True)
        new_score = sum(counts[k] * POINTS[k] for k in POINTS.keys())
        new_embed = HuntView().get_embed(
            _team_name_from_message(self.message),
            new_score,
            counts,
            self.end_time,
            self.host_id,
            self.is_host_mode,
            True,
        )
        await i.response.edit_message(
            embed=new_embed,
            view=ResultView(self.message, self.end_time, self.host_id, self.is_host_mode),
        )


class HuntView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def get_embed(self, team_name, score, counts, end_time, host_id, is_host_mode, final=False):
        counts_str = ",".join([str(counts.get(k, 0)) for k in POINTS.keys()])
        data_value = f"{score}|{end_time}|{host_id}|{int(is_host_mode)}|{counts_str}"
        if final:
            lines = ["```diff", "+ 狩猟結果詳細", "--------------------------"]
            for k, v in POINTS.items():
                if counts.get(k, 0) > 0:
                    lines.append(f"{k:2}: {counts[k]:2}回 \u00d7 {v:3}pt = {counts[k]*v:4}pt")
            lines.append("--------------------------")
            lines.append(f"最終合計: {score} pt```")
            embed = discord.Embed(
                title=f"\U0001F3C1 終了: {team_name}",
                description="\n".join(lines),
                color=discord.Color.gold(),
            )
            embed.add_field(name="_data", value=data_value, inline=False)
            return embed

        info_text = "```css\n[ 討伐対象リスト ]\n"
        for r, d in BOSS_MAPPING.items():
            info_text += f"{r:2} : {d}\n"
        info_text += "\n[ ポイント表 ]\n"
        for k, v in POINTS.items():
            info_text += f"{k:2}: {v}pt\n"
        info_text += "--------------------------\n"
        info_text += f"現在スコア: {score} pt\n```"
        embed = discord.Embed(
            title=f"\U0001F3C6 狩猟大会中: {team_name}",
            description=info_text,
            color=discord.Color.blue(),
        )
        embed.add_field(name="終了時間", value=f"終了予定: <t:{end_time}:F>\n(残り: <t:{end_time}:R>)", inline=False)
        embed.add_field(name="_data", value=data_value, inline=False)
        return embed

    async def _handle_update(self, i, key):
        data = get_data_field(i.message).split('|')
        host_id, is_host_mode = int(data[2]), bool(int(data[3]))
        if not is_authorized(i, host_id, is_host_mode):
            return await i.response.send_message(PERMISSION_DENIED_MESSAGE, ephemeral=True)

        counts = ResultView.get_counts_static(i.message)
        if time.time() > int(data[1]):
            await self.end_hunt_logic(i.message)
            return await i.response.send_message(HUNT_ENDED_MESSAGE, ephemeral=True)
        counts[key] += 1
        new_score = sum(counts[k] * POINTS[k] for k in POINTS.keys())
        await i.response.edit_message(
            embed=self.get_embed(
                _team_name_from_message(i.message),
                new_score,
                counts,
                int(data[1]),
                host_id,
                is_host_mode,
            ),
            view=self,
        )

    async def end_hunt_logic(self, message):
        counts = ResultView.get_counts_static(message)
        data = get_data_field(message).split('|')
        await message.edit(
            embed=self.get_embed(
                _team_name_from_message(message),
                int(data[0]),
                counts,
                int(data[1]),
                int(data[2]),
                bool(int(data[3])),
                True,
            ),
            view=ResultView(message, int(data[1]), int(data[2]), bool(int(data[3]))),
        )

    async def schedule_auto_end(self, message, end_time):
        """end_time を過ぎたら自動で結果画面へ遷移するタスクを予約する。"""
        delay = end_time - time.time()
        if delay > 0:
            await asyncio.sleep(delay)
        # 既に終了済み（タイトルが🏁）ならスキップ
        try:
            fresh = await message.channel.fetch_message(message.id)
            if "\U0001F3C6" in fresh.embeds[0].title:  # 🏆 が残っているなら未終了
                await self.end_hunt_logic(fresh)
        except (discord.NotFound, discord.Forbidden, IndexError):
            return

    @discord.ui.button(label="SS", style=discord.ButtonStyle.danger, custom_id="h1")
    async def b1(self, i, b):
        await self._handle_update(i, "SS")

    @discord.ui.button(label="S", style=discord.ButtonStyle.danger, custom_id="h2")
    async def b2(self, i, b):
        await self._handle_update(i, "S")

    @discord.ui.button(label="A", style=discord.ButtonStyle.danger, custom_id="h3")
    async def b3(self, i, b):
        await self._handle_update(i, "A")

    @discord.ui.button(label="B", style=discord.ButtonStyle.danger, custom_id="h4")
    async def b4(self, i, b):
        await self._handle_update(i, "B")

    @discord.ui.button(label="C", style=discord.ButtonStyle.danger, custom_id="h5")
    async def b5(self, i, b):
        await self._handle_update(i, "C")

    @discord.ui.button(label="変ヒル", style=discord.ButtonStyle.primary, custom_id="h6")
    async def b6(self, i, b):
        await self._handle_update(i, "変ヒル")

    @discord.ui.button(label="釣り", style=discord.ButtonStyle.success, custom_id="h7")
    async def b7(self, i, b):
        await self._handle_update(i, "釣り")

    @discord.ui.button(label="豪華", style=discord.ButtonStyle.success, custom_id="h8")
    async def c1(self, i, b):
        await self._handle_update(i, "豪華")

    @discord.ui.button(label="貴重", style=discord.ButtonStyle.success, custom_id="h9")
    async def c2(self, i, b):
        await self._handle_update(i, "貴重")

    @discord.ui.button(label="普通&精巧", style=discord.ButtonStyle.success, custom_id="h10")
    async def c3(self, i, b):
        await self._handle_update(i, "普通&精巧")

    @discord.ui.button(label="原型", style=discord.ButtonStyle.success, custom_id="h12")
    async def c4(self, i, b):
        await self._handle_update(i, "原型")

    @discord.ui.button(label="強制終了", style=discord.ButtonStyle.secondary, custom_id="h11")
    async def end_btn(self, i, b):
        data = get_data_field(i.message).split('|')
        if not is_authorized(i, int(data[2]), bool(int(data[3]))):
            return await i.response.send_message(PERMISSION_DENIED_MESSAGE, ephemeral=True)
        await self.end_hunt_logic(i.message)


class ResultView(discord.ui.View):
    def __init__(self, message=None, end_time=None, host_id=None, is_host_mode=None):
        super().__init__(timeout=None)
        self.message, self.end_time = message, end_time
        self.host_id, self.is_host_mode = host_id, is_host_mode

    @staticmethod
    def get_counts_static(message):
        data = get_data_field(message).split('|')
        return {k: int(data[4].split(',')[idx]) for idx, k in enumerate(POINTS.keys())}

    async def _open_edit_modal(self, i, targets, title):
        if not is_authorized(i, self.host_id, self.is_host_mode):
            return await i.response.send_message(PERMISSION_DENIED_MESSAGE, ephemeral=True)
        await i.response.send_modal(EditModal(
            i.message,
            self.end_time,
            self.host_id,
            self.is_host_mode,
            self.get_counts_static(i.message),
            targets,
            title,
        ))

    @discord.ui.button(label="討伐修正", style=discord.ButtonStyle.danger, custom_id="res_fix_hunt")
    async def fix_hunt(self, i, b):
        await self._open_edit_modal(i, HUNT_TARGETS, "討伐修正")

    @discord.ui.button(label="変ヒル修正", style=discord.ButtonStyle.primary, custom_id="res_fix_hilly")
    async def fix_hilly(self, i, b):
        await self._open_edit_modal(i, HILLY_TARGETS, "変ヒル修正")

    @discord.ui.button(label="採集修正", style=discord.ButtonStyle.success, custom_id="res_fix_collect")
    async def fix_collect(self, i, b):
        await self._open_edit_modal(i, COLLECT_TARGETS, "採集修正")

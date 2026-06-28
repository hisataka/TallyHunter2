import discord


def build_help_top_embed():
    embed = discord.Embed(
        title="📘 TallyHunter Help",
        description="見たい機能を選択してください",
        color=discord.Color.blurple(),
    )
    return embed


def build_hunt_help_embed():
    embed = discord.Embed(
        title="🏹 狩猟大会 Help",
        color=discord.Color.red(),
    )

    embed.add_field(
        name="コマンド",
        value="`/start-hunt`",
        inline=False,
    )

    embed.add_field(
        name="引数",
        value=(
            "• `team_name` (必須)\n"
            "• `minutes` (default=15)\n"
            "• `is_host_mode`"
        ),
        inline=False,
    )

    embed.add_field(
        name="使い方",
        value=(
            "1. コマンド実行\n"
            "2. ボタンで討伐数を加算\n"
            "3. 制限時間終了で自動集計"
        ),
        inline=False,
    )

    return embed


def build_extreme_help_embed():
    embed = discord.Embed(
        title="⚔️ 極限編成トライアル Help",
        color=discord.Color.gold(),
    )

    embed.add_field(
        name="コマンド",
        value="`/extreme-trial`",
        inline=False,
    )

    embed.add_field(
        name="引数",
        value=(
            "• `team_name`\n"
            "• `time_limit`\n"
            "• `is_host_mode`"
        ),
        inline=False,
    )

    embed.add_field(
        name="説明",
        value=(
            "聖遺物・キャラ凸・武器凸・討伐タイムから\n"
            "極限スコアを算出します"
        ),
        inline=False,
    )

    return embed


def build_artifact_help_embed():
    embed = discord.Embed(
        title="⭐ 聖遺物スコア Help",
        color=discord.Color.green(),
    )

    embed.add_field(
        name="コマンド",
        value="`/artifact-score`",
        inline=False,
    )

    embed.add_field(
        name="計算式",
        value="`会心ダメージ + メインステータス + 会心率 × 2`",
        inline=False,
    )

    embed.add_field(
        name="ランク",
        value=(
            "SS: 220+\n"
            "S : 200+\n"
            "A : 180+\n"
            "B : 160+\n"
            "C : 140+\n"
            "D : <140"
        ),
        inline=False,
    )

    embed.add_field(
        name="補足",
        value=(
            "• 花 / 羽 は赤ボタン\n"
            "• 時計 / 杯 は青ボタン\n"
            "• 冠 は緑ボタン"
        ),
        inline=False,
    )

    return embed
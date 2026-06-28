import discord


def build_help_top_embed():
    embed = discord.Embed(
        title="📘 TallyHunter Help",
        description="見たい機能を選択してください",
        color=discord.Color.blurple(),
    )
    embed.set_footer(text="Help Top")
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
            "2. ボタンで討伐加算\n"
            "3. 時間終了で自動集計"
        ),
        inline=False,
    )

    embed.add_field(
        name="例",
        value="`/start-hunt team_name:炎PT minutes:20`",
        inline=False,
    )

    embed.set_footer(text="Hunt Help")
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
        name="Tips",
        value=(
            "• 聖遺物スコアを入力\n"
            "• キャラ凸・武器凸も加点対象"
        ),
        inline=False,
    )

    embed.set_footer(text="Extreme Help")
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
        value="`会心ダメ + メインステ + 会心率×2`",
        inline=False,
    )

    embed.add_field(
        name="ランク",
        value=(
            "SS 220+\n"
            "S 200+\n"
            "A 180+\n"
            "B 160+\n"
            "C 140+\n"
            "D <140"
        ),
        inline=False,
    )

    embed.add_field(
        name="Tips",
        value=(
            "• 花羽はメインステ入力あり\n"
            "• 再度ボタン押下で再編集可能"
        ),
        inline=False,
    )

    embed.set_footer(text="Artifact Help")
    return embed
import discord


def build_help_embed():
    embed = discord.Embed(
        title="📖 TallyHunter2 Help",
        description="利用可能なコマンド一覧",
    )

    embed.add_field(
        name="/start-hunt",
        value=(
            "狩猟大会を開始します\n\n"
            "引数:\n"
            "• team_name (必須): チーム名\n"
            "• minutes (任意): 制限時間（分、default=15）\n"
            "• is_host_mode (任意): 主催者モード\n\n"
            "例:\n"
            "`/start-hunt team_name:炎PT minutes:20`"
        ),
        inline=False,
    )

    embed.add_field(
        name="/extreme-trial",
        value=(
            "極限編成トライアルを開始します\n\n"
            "引数:\n"
            "• team_name (必須): チーム名\n"
            "• time_limit (任意): 制限秒（default=180）\n"
            "• is_host_mode (任意): 主催者モード\n\n"
            "例:\n"
            "`/extreme-trial team_name:星4縛り time_limit:180`"
        ),
        inline=False,
    )

    return embed
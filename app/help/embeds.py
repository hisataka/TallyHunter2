import discord


def build_help_embed():
    embed = discord.Embed(
        title="📖 TallyHunter Help",
        description="利用可能なコマンド一覧",
    )

    embed.add_field(
        name="/start-hunt",
        value=(
            "狩猟大会を開始します\n\n"
            "引数:\n"
            "• team_name (必須): チーム名\n"
            "• minutes (任意): 制限時間（分、default=15）\n"
            "• is_host_mode (任意): 主催者モード（ボタンを主催者のみが押下可能です。）\n\n"
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
            "• is_host_mode (任意): 主催者モード（ボタンを主催者のみが押下可能です。）\n\n"
            "例:\n"
            "`/extreme-trial team_name:星4縛り time_limit:180`"
        ),
        inline=False,
    )

    embed.add_field(
        name="/artifact-score",
        value=(
            "聖遺物スコアを計算します\n\n"
            "計算式:\n"
            "• 会心ダメージ + メインステータス + 会心率 × 2\n\n"
            "引数:\n"
            "• character_name (必須): キャラ名\n"
            "• is_host_mode (任意): ホストのみ編集可能\n\n"
            "使い方:\n"
            "1. コマンド実行\n"
            "2. 花 / 羽 / 時計 / 杯 / 冠 ボタンを押す\n"
            "3. 各聖遺物の値を入力\n"
            "4. 合計スコアが表示される\n\n"
            "※ メインステータスには元素ダメージ%、攻撃%、"
            "チャージ効率%などを入力\n\n"
            "例:\n"
            "`/artifact-score character_name:フリーナ`"
        ),
        inline=False,
    )

    return embed
import discord

EXTREME_DISPLAY_LABELS = [
    "①聖遺物スコア",
    "②☆5キャラ人数",
    "③最大キャラ凸数",
    "④その他キャラ凸合計",
    "⑤☆5武器数",
    "⑥☆3武器数",
    "⑦最多凸武器精錬",
    "⑧その他武器精錬合計",
    "⑨討伐タイム(秒)",
    "制限時間(秒)",
]


def build_extreme_embed(team_name, data_str, result=None):
    d = data_str.split(',')

    labels = [
        (EXTREME_DISPLAY_LABELS[0], d[0]),
        (EXTREME_DISPLAY_LABELS[1], d[1]),
        (EXTREME_DISPLAY_LABELS[2], d[2]),
        (EXTREME_DISPLAY_LABELS[3], d[3]),
        (EXTREME_DISPLAY_LABELS[4], d[4]),
        (EXTREME_DISPLAY_LABELS[5], d[5]),
        (EXTREME_DISPLAY_LABELS[6], d[6]),
        (EXTREME_DISPLAY_LABELS[7], d[7]),
        (EXTREME_DISPLAY_LABELS[8], d[8]),
        (EXTREME_DISPLAY_LABELS[9], d[9]),
    ]

    desc = "```yaml\n"
    for k, v in labels:
        desc += f"{k}: {v}\n"
    desc += "```"

    embed = discord.Embed(
        title=f"極限編成トライアル: {team_name}",
        description=desc,
        color=discord.Color.purple(),
    )

    if result:
        score, a, c, w = result
        embed.add_field(
            name="計算結果",
            value=(
                "```diff\n"
                f"+ 総合スコア : {score:.2f}\n"
                f"聖遺物係数   : {a:.2f}\n"
                f"キャラ係数   : {c:.2f}\n"
                f"武器係数     : {w:.2f}\n"
                "```"
            ),
            inline=False,
        )

    embed.add_field(name="_data", value=data_str, inline=False)
    return embed

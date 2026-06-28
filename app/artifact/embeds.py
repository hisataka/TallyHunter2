import discord

ARTIFACT_TITLE_PREFIX = "聖遺物スコア: "
PARTS = ["花", "羽", "時計", "杯", "冠"]


def build_artifact_embed(character_name, data_str):
    data = data_str.split("|")
    scores = [float(x) for x in data[0].split(",")]
    total = sum(scores)

    lines = []

    for idx, part in enumerate(PARTS):
        score = scores[idx]
        if score == 0:
            lines.append(f"{part}: 未入力")
        else:
            lines.append(f"{part}: {score:.1f}")

    lines.append("----------------")
    lines.append(f"Total Score: {total:.1f}")

    embed = discord.Embed(
        title=f"{ARTIFACT_TITLE_PREFIX}{character_name}",
        description="```yaml\n" + "\n".join(lines) + "\n```",
        color=discord.Color.green(),
    )

    embed.add_field(
        name="_data",
        value=data_str,
        inline=False,
    )

    return embed
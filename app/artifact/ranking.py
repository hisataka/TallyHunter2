PART_THRESHOLDS = {
    "flower_feather": [
        ("SS", 50),
        ("S", 45),
        ("A", 40),
        ("B", 35),
        ("C", 30),
        ("D", 0),
    ],
    "sands_goblet": [
        ("SS", 45),
        ("S", 40),
        ("A", 35),
        ("B", 30),
        ("C", 25),
        ("D", 0),
    ],
    "circlet": [
        ("SS", 40),
        ("S", 35),
        ("A", 30),
        ("B", 25),
        ("C", 20),
        ("D", 0),
    ],
}

TOTAL_THRESHOLDS = [
    ("SS", 220),
    ("S", 200),
    ("A", 180),
    ("B", 160),
    ("C", 140),
    ("D", 0),
]


def get_part_rank(part_index, score):
    """
    部位別ランク
    0 花
    1 羽
    2 時計
    3 杯
    4 冠
    """
    if part_index in (0, 1):
        table = PART_THRESHOLDS["flower_feather"]
    elif part_index in (2, 3):
        table = PART_THRESHOLDS["sands_goblet"]
    else:
        table = PART_THRESHOLDS["circlet"]

    for rank, threshold in table:
        if score >= threshold:
            return rank

    return "D"


def get_total_rank(total_score):
    for rank, threshold in TOTAL_THRESHOLDS:
        if total_score >= threshold:
            return rank
    return "D"
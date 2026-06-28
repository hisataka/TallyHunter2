def calculate_artifact_score(cd, atk, cr):
    """
    聖遺物スコア計算

    score = 会心ダメ + 攻撃% + 会心率*2
    """
    return cd + atk + cr * 2
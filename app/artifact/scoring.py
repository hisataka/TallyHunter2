def calculate_artifact_score(cd, main_stat, cr):
    """
    聖遺物スコア

    score = 会心ダメ + メインステータス + 会心率*2
    """
    return cd + main_stat + cr * 2
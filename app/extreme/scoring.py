"""極限編成トライアルのスコア計算ロジック。"""


def _get_artifact_coeff(s):
    if s >= 200:
        return 0.25
    if s >= 180:
        return 0.5
    if s >= 170:
        return 0.75
    if s >= 160:
        return 1.0
    if s >= 140:
        return 1.75
    if s >= 120:
        return 2.5
    if s >= 100:
        return 3.5
    return 6.0


def calculate_extreme_score(d):
    base_char = {4: 0.25, 3: 0.5, 2: 1.0, 1: 1.75, 0: 3.0}
    c_coeff = base_char.get(d['char_count'], 0.25)
    c_penalty = (d['max_c_const'] * 0.15) + (d['sum_c_const'] / 10)
    c_coeff = c_coeff - c_penalty

    w_coeff = 2.25 - (d['w5_count'] * 0.5) + (d['w3_count'] * 0.5)
    w_penalty = (d['max_w_refine'] * 0.2) + (d['sum_w_refine'] / 15)
    w_coeff = w_coeff - w_penalty

    a_coeff = _get_artifact_coeff(d['artifact_score'])

    limit = d['time_limit']
    time_score = limit - (d['time'] ** 2 / limit) if d['time'] <= limit else 0

    score = (a_coeff + c_coeff + w_coeff) * max(0, time_score)

    return score, a_coeff, c_coeff, w_coeff

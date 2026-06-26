# HuntBot

Discord bot providing two slash commands:

- `/start-hunt` — 狩猟大会を開始
- `/extreme-trial` — 極限編成トライアルを開始

## Project layout

```
huntbot/
├── main.py              # entrypoint
├── requirements.txt
├── .env.example
└── app/
    ├── config.py        # 環境変数 (.env) の読み込み
    ├── web.py           # Flask 常駐サーバ (health check)
    ├── constants.py     # ポイント表、討伐対象マッピング
    ├── utils.py         # 権限チェック、_data 取得ヘルパ
    ├── bot.py           # HuntBot 本体、auto_end ループ
    ├── hunt/            # 狩猟大会 (start-hunt) 機能
    │   ├── views.py     # HuntView / ResultView / EditModal
    │   └── commands.py  # /start-hunt 登録
    └── extreme/         # 極限編成トライアル (extreme-trial) 機能
        ├── scoring.py   # 計算ロジック
        ├── embeds.py    # 埋め込み生成
        ├── views.py     # ExtremeTrialView / TrialEditModal
        └── commands.py  # /extreme-trial 登録
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # then edit DISCORD_BOT_TOKEN
python main.py
```

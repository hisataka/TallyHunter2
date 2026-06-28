"""共通ユーティリティ。"""

PERMISSION_DENIED_MESSAGE = "ホストのみ操作可能です。"
NUMBER_REQUIRED_MESSAGE = "数字で入力してください。"
HUNT_ENDED_MESSAGE = "大会は終了しました."


def is_authorized(interaction, host_id, is_host_mode):
    """ホストモード時にホスト以外のユーザーをブロックする。"""
    if is_host_mode and interaction.user.id != host_id:
        return False
    return True


def get_data_field(message):
    """埋め込みの '_data' フィールドの値を返す。"""
    for field in message.embeds[0].fields:
        if field.name == "_data":
            return field.value
    raise ValueError("_data field not found")
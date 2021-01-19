import subprocess

# get_helptext
# ヘルプテキスト作成
async def get_helptext(prefix, name, txt):
    return f'テキストチャンネル（以下TC）に入力された文字列をボイスチャンネル（以下VC）へ音声で出力するBotです。\n' \
        + f'読み上げ対象はjoinコマンドを入力されたTC→Botの居るVCです。\n' \
        + f'Bot以外のVC参加者が居なくなった場合は自動的に切断されます。\n' \
        + f'{prefix}set_prefix arg1 : prefixをarg1に変更します。\n' \
        + f'{prefix}cv arg1 arg2（省略可能） : コマンド入力した人の読み上げ音声をarg1、読み上げ速度をarg2（標準は1.0）で登録します。\n' \
        + f'{prefix}ad arg1 arg2 : arg1の読みをarg2で辞書登録します。\n' \
        + f'{prefix}cvlist : 登録済み読み上げ音声の一覧を表示します。左がcvのarg1で使用可能な情報、右が音声ファイル名です。\n' \
        + f'{prefix}join : コマンド入力した人が居るVCへ接続し、読み上げを開始します。\n' \
        + f'{prefix}ch_entry_info : 接続VC内の入退室情報読み上げ状態を変更します。現在は{txt}です。\n' \
        + f'{prefix}bye : VCから退室します。\n' \
        + f'※現在の{name}のprefixは{prefix}です。'

# get_cptext
# prefix変更時テキスト作成
async def get_cptext(before_prefix, prefix):
    return f'prefixが {before_prefix} から {prefix} に変更されました。'

# get_cvetext
# 声変更コマンド例外時テキスト作成
async def get_cvetext(arg1, DEV):
    return f'{arg1}はcvlistに存在しませんでしたので、f001で登録を行います。\n' \
        + f'現在使用できる声の種類はcvlistコマンドで確認して下さい。\n' \
        + f'欲しい声の種類が無い場合は{DEV}まで。'

# get_cvtext
# 声変更コマンド終了時テキスト作成
async def get_cvtext(name, arg1, arg2):
    return f'{name}の読み上げを以下の通り変更しました。\n' \
        + f'cv:{arg1},読み上げ速度:{arg2}'

# get_exittext
# 退出時読み上げ用メッセージ作成
async def get_exittext(name):
    return f'{name}さんが退出しました'

# get_entrytext
# 入室時読み上げ用メッセージ作成
async def get_entrytext(name):
    return f'{name}さんが接続しました'

# get_adtext
# 辞書登録時メッセージ作成
async def get_adtext(arg1, arg2):
    return f'`{arg1}` を `{arg2}` として登録しました'

# get_acttext
# ステータス表示情報作成
async def get_acttext():
    return 'Bot宛メンションでhelp'
import os
import asyncio
import time
import discord
import aiofiles
import json
from voice_generator import creat_WAV

# chk_config
# コンフィグファイルが存在しない場合作成する。
async def chk_config(sid, DCTB):
    # サーバーIDディレクトリチェック
    siddir = f'{DCTB}guild/{sid}'

    # ディレクトリがない場合、作成する
    if not os.path.exists(siddir):
        print('サーバー情報を作成します')
        os.makedirs(siddir)
        path = f'{siddir}/config.json'
        dic = {}
        await set_json(path, dic)

# common_disconnect
# 切断時共通処理
async def common_disconnect(sid, filepath):
    data = await get_json(filepath)
    delete = data.pop(sid)  # sidを削除
    print(f'{delete}から退出')
    await set_json(filepath, data)

# get_json
# json形式ファイル取得処理
async def get_json(filepath):
    async with aiofiles.open(filepath) as f:
        contents = await f.read()
        data = json.loads(contents)  # json形式として読み込む
    return data

# set_json
# json形式ファイル更新処理
async def set_json(filepath, data):
    async with aiofiles.open(filepath,'w') as f:
        await f.write(json.dumps(data))  # 変更済みの辞書をjson形式でファイル出力

def del_file(filepath):
    if os.path.exists(f'{filepath}input.txt'):
        os.remove(f'{filepath}input.txt')
    if os.path.exists(f'{filepath}output.wav'):
        os.remove(f'{filepath}output.wav')
import subprocess
import re
import os
import json
import aiofiles
import settings

DSCT = settings.DSCT
OPJT = settings.OPJT
DCTB = os.path.dirname(__file__) + '/'

# remove_custom_emoji
# 絵文字IDは読み上げない
def remove_custom_emoji(text):
    pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'    # カスタム絵文字のパターン
    return re.sub(pattern,'',text)   # 置換処理

# urlAbb
# URLなら省略
def urlAbb(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern,'URL省略',text)   # 置換処理

# remove_picture
# 画像ファイルなら読み上げない
def remove_picture(text):
    pattern = r'.*(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
    return re.sub(pattern,'',text)   # 置換処理

# user_custam
# ユーザ登録した文字を読み替える
def user_custam(text,sid):

    filepath = f'{DCTB}guild/{sid}/dic.txt'
    if os.path.isfile(filepath):
        f = open(filepath, 'r')
        line = f.readline()

        while line:
            pattern = line.strip().split(',')
            if pattern[0] in text and len(pattern) >= 2:
                text = text.replace(pattern[0], pattern[1])
                break
            else:
                line = f.readline()

        f.close()
    else:
        pass

    return text

# creat_WAV
# message.contentをテキストファイルに書き込み
def creat_WAV(inputText, sid, cv, r, t):

    inputText = remove_custom_emoji(inputText)   # 絵文字IDは読み上げない
    inputText = urlAbb(inputText)   # URLなら省略
    inputText = remove_picture(inputText)   # 画像なら読み上げない
    inputText = user_custam(inputText, sid)   # ユーザ登録した文字を読み替える
    text_check = re.sub(r"[ 　\n]", "", inputText)

    if len(text_check) != 0:
        input_file = f'{DCTB}guild/{sid}/{t}input.txt'
        print(input_file)

        with open(input_file,'w',encoding='shift_jis') as file:
            file.write(inputText.replace( '\n' , '　' ))

        #辞書のPath
        x = f'{OPJT}dic/'

        #ボイスファイルのPath
        m = f'{OPJT}{cv}.htsvoice'

        #出力ファイル名 and Path
        ow = f'{DCTB}guild/{sid}/{t}output.wav'

        #r is voice speed
        args = {'x':x, 'm':m, 'r':r, 'ow':ow, 'input_file':input_file}

        command = f'{OPJT}open_jtalk -x {x} -m {m} -r {r} -ow {ow} {input_file}'

        cmd = command.format(**args)

        subprocess.run(cmd)
        return True
    else:
        return False

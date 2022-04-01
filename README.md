# DiscordTalkBot  
Discord readout bot using open_jtalk-1.11  
Because the developer is an idiot, this README is only available in Japanese.  

# 仕様の変更に伴い動かなくなったため現在調整中  

## Discord内のテキストチャンネルに入力された内容をボイスチャンネルで音声出力するBot  
有名なPublicの読み上げBotに負荷が掛かり過ぎ、使用出来ない事が増えてきたため  
Pythonの理解と実益を兼ねて自作した、Open_JTalkを利用したDiscord用の読み上げBotです。  
ボイスチャンネルに参加しているユーザがこのBotのみとなった場合自動的に切断します。  
また、ボイスチャンネルへの入退室情報読み上げ機能を積んでいます。  

## 機能
Botへのメンションでhelpを送信します。  
Defaultのprefixは"."となっています。  

- .join           コマンドを入力したユーザーが居るボイスチャンネルへ接続し、
                  全ユーザーが居なくなるか、byeコマンドでBotが切断されるまでの間、  
                  コマンドが入力されたテキストチャンネルの読み上げを行います。  
- .bye            接続中のボイスチャンネルから切断します。  
- .ch_entry_info  接続中のボイスチャンネル内の入退室情報読み上げのOn/Offを切り替えます。  

他の機能はhelpを参照して下さい。  

## 必要要件

- Windows10 Pro 64bit版でのみ動作確認を行っています。  
- open_jtalk（shift_jis版）が導入されていること。  
- UNIX等の環境で動かす場合、UTF-8へ変更するべきだと思います。  
- 自分の確認環境ではshift_jisでないと正常に動作しませんでした。  
- Python 3.9.1  
- Discord.py 1.6.0  
- python-dotenv 0.15.0  
- その他必要に応じたライブラリ
aiofiles
ffmpeg
PyNaCl
python-dotenv

## 使い方

1. BotをDISCORD DEVELOPER PORTALへ登録する。  
2. .envファイルを作成する。  
3. 初期音声ファイル設定をあなたの環境に合わせ、conf/cvlist.jsonを変更する。  
4. read_bot.pyを実行  

## その他

不慣れなため拙い部分が多いと思います。  
不明点が有りましたら連絡頂ければ可能な範囲で対応します。  
要望など有れば作者TwitterへDM下さい。※極力日本語でお願いします。  
改修していただけた場合は、よろしければ内容を連絡頂ければ励みになります。  

## 作者

[@marumusi_mc](https://twitter.com/marumusi_mc)

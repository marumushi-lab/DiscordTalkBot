import discord
import json
import aiofiles
import time
import asyncio
import os
import subprocess
import ffmpeg
import wave
import re
from discord.ext import commands
from voice_generator import creat_WAV
import settings
import longtext as lt
import sub_module as sb
from collections import deque

DSCT = settings.DSCT
OPJT = settings.OPJT
DCTB = os.path.dirname(__file__)+'/'
BID = settings.BID
DEV = settings.DEV

channel_path = f'{DCTB}conf/channel.json'
guild_path = f'{DCTB}conf/guild.json'
prefix_path = f'{DCTB}conf/prefix.json'
cvlist_path = f'{DCTB}conf/cvlist.json'

oplist = {} # queueの登録に使用

intents = discord.Intents.default()
intents.members = True
voice_client = None

def LengthMusic(wavefile):
    wf = wave.open("{0}".format(wavefile) , "r" )
    times = int(int(wf.getnframes()) / wf.getframerate())
    return times + 1

async def cre_oplist(sid):
    global oplist
    oplist[sid] = deque() # queue作成

async def get_oplist(sid):
    q = oplist.get(sid,deque())
    return q[0] # queue情報取得

async def add_oplist(sid,t):
    global oplist
    q = oplist.get(sid,deque())
    q.append(t)
    oplist[sid] = q # queue更新

async def pop_oplist(sid):
    global oplist
    q = oplist.get(sid,deque())
    q.popleft()
    oplist[sid] = q # queue更新

async def del_oplist(sid):
    global oplist
    oplist.pop(sid) # queueを削除

# chk_play
# 音声出力終了待ち処理
async def chk_play(vc, sid, t, f='cre'):
    while True:
        if not vc.is_playing():
            nq = await get_oplist(sid)
            if nq == t:
                if f != 'del':
                    break
                else:
                    await pop_oplist(sid)
                    sb.del_file(f'{DCTB}guild/{sid}/{t}')
                    break
            else:
                pass
        else:
            pass
        time.sleep(1)
    return

# iocheck
# 入退室チェック処理
async def iocheck(sid, vc, msg):
    data = await sb.get_json(guild_path)
    iolog = data.get(sid,'t')
    if iolog == 't':
        t = str(time.perf_counter()).replace('.', '')
        await add_oplist(sid, t)
        if creat_WAV(msg, sid, 'f001', '1.0', t):
            source = discord.FFmpegPCMAudio(f'{DCTB}guild/{sid}/{t}output.wav')
            await chk_play(vc, sid, t)
            vc.play(source)
            await chk_play(vc, sid, t, 'del')

# disconnect
# 切断処理
async def disconnect(vc,sid):
    await vc.disconnect()
    await sb.common_disconnect(sid, channel_path)
    await del_oplist(sid)

# prefix_from_json
# prefix変更用処理
async def prefix_from_json(bot,message):

    data = await sb.get_json(prefix_path)

    return data.get(str(message.guild.id),'.')

client = commands.Bot(command_prefix=prefix_from_json, help_command=None, intents=intents) # 定義した関数を渡しています
client.remove_command("help")

# 起動時処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(await lt.get_acttext()))

# prefix登録処理
@client.command()
async def set_prefix(ctx,prefix):

    sid = str(ctx.guild.id)
    data = await sb.get_json(prefix_path)
    before_prefix = data.get(sid,'.')
    data[sid] = prefix  # 辞書内で prefix を変更しておく

    await sb.set_json(prefix_path, data)

    await ctx.send(await lt.get_cptext(before_prefix, prefix))

# VC接続処理
@client.command()
async def join(ctx):
    vc = ctx.author.voice.channel
    sid = str(ctx.guild.id)
    cid = str(ctx.channel.id)
    print(f'{ctx.guild.name}で使用開始')

    data = await sb.get_json(channel_path)
    data[sid] = cid  # 辞書内で channel を登録しておく

    await sb.set_json(channel_path, data)

    await cre_oplist(sid)

    await sb.chk_config(sid, DCTB)
    await vc.connect()

# VC退出処理
@client.command()
async def bye(ctx):
    print('#切断')
    sid = str(ctx.guild.id)
    vc = ctx.voice_client
    await disconnect(vc, sid)

@client.command()
async def help(ctx):
    print(ctx)
    data = await sb.get_json(prefix_path)
    prefix = data.get(str(ctx.guild.id),'.')
    data = await sb.get_json(guild_path)
    info = data.get(str(ctx.guild.id),'t')
    if info == 't':
        txt = 'On'
    else:
        txt = 'Off'

    await ctx.author.send(await lt.get_helptext(prefix, ctx.guild.name, txt))

@client.command()
async def cvlist(ctx):
    data = await sb.get_json(cvlist_path)
    
    txt = None
    for jsn_key in data:
        jsn_val = data.get(jsn_key)
        if txt is None:
            txt = f'{jsn_key}:{jsn_val}'
        else:
            txt = txt + f'\n{jsn_key}:{jsn_val}'

    await ctx.channel.send(txt)

@client.command()
async def ad(ctx, arg1, arg2):

    sid = str(ctx.guild.id)
    filepath = f'{DCTB}guild/{sid}/dic.txt'
    with open(filepath, mode='a') as f:
        f.write(f'\n{arg1},{arg2}')
    ctx.send(await lt.get_adtext(arg1, arg2))

@client.command()
async def ch_entry_info(ctx):

    data = await sb.get_json(guild_path)
    old_info = data.get(str(ctx.guild.id),'t')
    if old_info =='t':
        info = 'f'
        txt = 'Off'
    else:
        info = 't'
        txt = 'On'
    data[str(ctx.guild.id)] = info  # 辞書内で prefix を変更しておく

    await sb.set_json(guild_path, data)

    await ctx.send(f'入退室の読み上げを{txt}に変更しました。')

@client.command()
async def cv(ctx, arg1='f001', arg2='1.0'):

    sid = str(ctx.guild.id)

    data = await sb.get_json(cvlist_path)
    cvck = data.get(arg1,None)
    if cvck is None:
        await ctx.channel.send(await lt.get_cvetext(arg1, DEV))
        arg1 = 'f001'
    cvconf = {'cv':arg1,'x':arg2}

    filepath = f'{DCTB}guild/{sid}/config.json'
    data = await sb.get_json(filepath)
    data[str(ctx.author.id)] = cvconf  # 辞書更新

    await sb.set_json(filepath, data)

    await ctx.channel.send(await lt.get_cvtext(ctx.author.name, arg1, arg2))

@client.event
async def on_voice_state_update(member, before, after):

    if member.guild.voice_client is not None:
        vc = member.guild.voice_client
        sid = str(member.guild.id)
        name = member.display_name
        if vc.is_connected():
            if before.channel is not None:
                if vc.channel.id == before.channel.id:
                    if len(before.channel.voice_states) == 1:

                        print('#切断')
                        data = await sb.get_json(channel_path)
                        cid = data.get(sid, None)
                        if cid != None:
                            channel = client.get_channel(int(cid))
                            await channel.send('ご利用ありがとうございました。')
                        await vc.disconnect()
                        await sb.common_disconnect(sid, channel_path)
                        await del_oplist(sid)

                    else:
                        if before.channel.id != after.channel.id:
                            msg = await lt.get_exittext(name)
                            await iocheck(sid, vc, msg)

                else:
                    if after.channel is not None:
                        if vc.channel.id == after.channel.id:
                            msg = await lt.get_entrytext(name)
                            await iocheck(sid, vc, msg)
            else:
                if after.channel is not None:
                    if vc.channel.id == after.channel.id:
                        msg = await lt.get_entrytext(name)
                        await iocheck(sid, vc, msg)

@client.event
async def on_message(message):

    if message.author.bot:
        return
    sid = str(message.guild.id)
    ncid = str(message.channel.id)
    data = await sb.get_json(prefix_path)
    prefix = data.get(sid,'.')
    await sb.chk_config(sid, DCTB)

    if message.content.startswith(f'<@!{BID}>'):
        message.content = f'{prefix}help'
    if message.content.startswith(prefix):
        await client.process_commands(message)
    else:
        if message.guild.voice_client:
            data = await sb.get_json(channel_path)
            cid = data.get(sid,ncid)
            if ncid == cid:
                dc = {'cv':'f001','x':'1.0'}
                data = await sb.get_json(f'{DCTB}guild/{sid}/config.json')
                conf = data.get(str(message.author.id),dc)
                cv = conf.get('cv')
                x = conf.get('x')
                msg = message.content
                userids = re.findall('<@!(.*)>', msg)
                roleids = re.findall('<@&(.*)>', msg)
                if userids:
                    for userid in userids:
                        user = message.guild.get_member(int(userid))
                        msg = re.sub(f'<@!{userid}>',user.display_name,msg)
                if roleids:
                    for roleid in roleids:
                        role = message.guild.get_role(int(roleid)).name
                        msg = re.sub(f'<@&{roleid}>',role,msg)
                t = str(time.perf_counter()).replace('.', '')
                await add_oplist(sid, t)
                if creat_WAV(msg, sid, cv, x, t):
                    times = LengthMusic(f'{DCTB}guild/{sid}/{t}output.wav')
                    source = discord.FFmpegPCMAudio(f'{DCTB}guild/{sid}/{t}output.wav')
                    await chk_play(message.guild.voice_client, sid, t)
                    message.guild.voice_client.play(source)
                    time.sleep(times)
                    await chk_play(message.guild.voice_client, sid, t, 'del')

client.run(DSCT)
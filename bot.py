"""This is a main program"""
from asyncio import sleep
import configparser
import datetime
import json
import re
import discord
import time_checker


CLIENT = discord.Client()
INIFILE = configparser.SafeConfigParser()
INIFILE.read('config.ini', 'UTF-8')
BOT_TOKEN = INIFILE.get('Discord', 'BOT_TOKEN')
CHANNEL_ID = INIFILE.get('Discord', 'CHANNEL')
CHANNEL = discord.Object(id=CHANNEL_ID)
COMAND_PREFIX = INIFILE.get('Discord', 'COMAND_PREFIX')
DEL_TIME = int(INIFILE.get('Discord', 'DEL_TIME'))
POPTIME_JSON = open('poptime.json', 'r', encoding="utf-8_sig")
JSON_DATA = json.load(POPTIME_JSON)
CT = time_checker.CheckTime(JSON_DATA)

@CLIENT.event
async def regular_processing():
    """
    指定の時間にボスのpopを通知する
    """
    while True:
        now = datetime.datetime.now()
        time_key, weekday = CT.check_nextpop(now)
        nowplay = CT.change_presence(time_key, weekday)
        try:
            await CLIENT.change_presence(game=discord.Game(name=nowplay))
        except AttributeError:
            pass

        res = CT.check_before30(now, time_key, weekday)
        if res is None:
            print("...")

        else:
            try:
                msg = await CLIENT.send_message(CHANNEL, res)
                CLIENT.loop.create_task(del_notification(msg))
            except AttributeError:
                pass

        await sleep(60)


@CLIENT.event
async def on_ready():
    """
    起動確認
    """
    print('Black Desert Online infomation bot')
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)


@CLIENT.event
async def on_message(message):
    """
    テキストチャットに反応する
    """
    if CLIENT.user != message.author \
    and message.content.startswith(COMAND_PREFIX):

        if re.search("info", message.content):
            now = datetime.datetime.now()
            _, weekday = CT.check_nextpop(now)
            title, description = CT.info(weekday)
            res = discord.Embed(title=title,\
            description=description, colour=0x3498db)
            msg = await CLIENT.send_message(CHANNEL, embed=res)
            await CLIENT.add_reaction(msg, '◀')
            await CLIENT.add_reaction(msg, '▶')
            await sleep(1)
            CLIENT.loop.create_task(check_reaction(msg, weekday))
            await sleep(DEL_TIME)
            await CLIENT.delete_message(msg)
            await CLIENT.delete_message(message)

        elif re.search("help", message.content):
            res = discord.Embed(title="機能",\
            description="・ボスの湧き時間10分前、30分前に通知\
            \n・次のボスの名前と湧き時間をステータスに表示\
            \n・`{}info`で曜日ごとのボスポップ一覧を表示\
            \n　(◀で前の曜日、▶で次の曜日)\
            \n要望、バグ報告は https://github.com/4KaNE/BDOinfo に"\
            .format(COMAND_PREFIX), colour=0x3498db)
            msg = await CLIENT.send_message(CHANNEL, embed=res)
            await sleep(DEL_TIME)
            await CLIENT.delete_message(msg)
            await CLIENT.delete_message(message)


@CLIENT.event
async def check_reaction(target_msg, weekday):
    """
    指定のメッセージにつけられたリアクションを監視する
    """
    def weekday_normalize(value):
        """
        weekdayの数値を0～6の範囲に直す
        """
        if value < 0:
            value += 7

        elif value > 6:
            value -= 7

        else:
            pass

        return value

    endtime = datetime.datetime.now() + datetime.timedelta(seconds=DEL_TIME)
    while True:
        if datetime.datetime.now() >= endtime:
            break

        else:
            target_reaction = await CLIENT.wait_for_reaction(message=target_msg)
            if target_reaction.reaction.emoji == '◀':
                weekday -= 1

            elif target_reaction.reaction.emoji == '▶':
                weekday += 1

            else:
                weekday = None

            if weekday is None:
                pass

            else:
                weekday = weekday_normalize(weekday)
                title, description = CT.info(weekday)
                msg = discord.Embed(title=title,\
                description=description, colour=0x3498db)
                await CLIENT.edit_message(target_msg, embed=msg)
                await CLIENT.remove_reaction(target_msg, \
                target_reaction.reaction.emoji, target_reaction.user)

@CLIENT.event
async def del_notification(target_msg):
    """
    ボス時間の通知を20分後に削除する
    """
    await sleep(1200)
    count = 0
    while count < 5:
        count += 1
        try:
            await CLIENT.delete_message(target_msg)
        except AttributeError:
            print("通知の削除に失敗 {}回目".format(count))

        sleep(60)

CLIENT.loop.create_task(regular_processing())
CLIENT.run(BOT_TOKEN)

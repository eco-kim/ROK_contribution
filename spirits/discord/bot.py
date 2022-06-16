import discord, asyncio, os
from discord.ext import commands
import json
import pandas as pd
import psycopg2
import re

try:
    conn = psycopg2.connect(host='127.0.0.1', dbname="rok", user="eco", password="1227")
except:
    print("DB connect fail")

dir = 'C:/Users/ikho7/Desktop/projects/rok_contribution/spirits/discord/screenshots/'
namedf = pd.read_csv('C:/Users/ikho7/Desktop/projects/rok_contribution/spirits/namelist.csv')
dciddf = pd.read_csv('C:/Users/ikho7/Desktop/projects/rok_contribution/spirits/dcidlist.csv')
game = discord.Game("스크린샷 수집")
client = commands.Bot(command_prefix='!', status=discord.Status.online, 
    activity=discord.Game('test'))

@client.event
async def on_ready(): 
    print("스크린샷 수집 중")
    print('---------------')
    await client.change_presence(status=discord.Status.online, 
    activity=game)

@client.command()
async def uid(ctx, uid):
    global namedf, dciddf
    uid = int(re.findall('\d+',uid)[0])
#    kdid = ctx.guild.id   #어느 디스코드 서버인지 체크
    dcid = ctx.author   #디스코드 아이디 체크
    temp = namedf['nickname'][namedf['uid']==uid].values
    if not temp:
        await ctx.send("uid를 다시 확인 해 주세요 (서버원 명단에 존재하지 않음)")
    else:
        nickname = temp[0]
        with open('C:/Users/ikho7/Desktop/projects/rok_contribution/spirits/dcidlist.csv','a',encoding='UTF-8') as f:
            f.write(f'{dcid},{uid},{nickname}\n')
        dciddf = dciddf.append({'dcid':dcid,'uid':uid,'nickname':nickname},ignore_index=True)
        await ctx.send(f"{nickname} {uid} : uid 등록완료")

@client.command(aliases=['제출','본캐','본계정'])
async def spirit(ctx, *args):
    global namedf, dciddf
    dcid = ctx.author
    if len(args)==0:
        temp = dciddf['uid'][dciddf['dcid']==dcid].values
        if len(temp)==0:
            await ctx.send("uid를 먼저 등록하시거나(!uid 11111111) !제출 11111111 형식으로 적어주세요")
            uid = 99999999
        else:
            uid = temp[-1]
    else:
        uid = int(re.findall('\d+',args[0])[0])
    attachment = ctx.message.attachments
#    kdid = ctx.guild.id   #어느 디스코드 서버인지 체크 / 나중에 다른서버에도 서비스한다면 필요한부분. 
    dcid = ctx.author   #디스코드 아이디 체크    
    temp = namedf['nickname'][namedf['uid']==uid].values
    if not temp:
        await ctx.send("uid를 다시 확인 해 주세요 (서버원 명단에 존재하지 않음)")
    else:
        nickname = temp[0]
        if len(attachment)==0:
            await ctx.send("스크린샷을 첨부해 주세요 (첨부파일과 uid를 동시에 전송해야합니다)")
        else:
            for attach in attachment:
                fname = str(attach).split('/')[-1]
                exten = fname.split('.')[-1]
                await attach.save(fp=dir+str(uid)+'.'+exten)
            await ctx.send(f"{nickname} {uid} : 영령전 제출완료")

@client.command(aliases=['부캐','부계정'])
async def sub(ctx, uid):
    global namedf, dciddf
    uid = int(re.findall('\d+',uid)[0])
    attachment = ctx.message.attachments
    dcid = ctx.author   #디스코드 아이디 체크
    temp = dciddf['nickname'][dciddf['dcid']==dcid].values
    if len(temp)==0:
        await ctx.send("부계정 영령전을 제출하시려면 본계정의 uid를 먼저 등록해주세요 (!uid xxxxxxxx)")
    else:
        mainnick = temp[-1]
        if len(attachment)==0:
            await ctx.send("스크린샷을 첨부해 주세요 (첨부파일과 uid를 동시에 전송해야합니다)")
        else:
            for attach in attachment:
                fname = str(attach).split('/')[-1]
                exten = fname.split('.')[-1]
                mainid = dciddf['uid'][dciddf['dcid']==dcid].values[-1]
                await attach.save(fp=dir+f'sub{mainid}_{uid}.{exten}')
            nickname = namedf['nickname'][namedf['uid']==uid].values
            if nickname:
                await ctx.send(f"{mainnick}님 부계정 {nickname} {uid} : 영령전 제출완료")
            else:
                await ctx.send(f"{mainnick}님 부계정 {uid} : 영령전 제출완료 (500위 외 닉네임 확인 불가)")

with open('./bot_info.json','r') as f:
    bot_info = json.load(f)
token = bot_info["TOKEN"]

client.run(token)

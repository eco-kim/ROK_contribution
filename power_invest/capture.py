import pyperclip as clip
import pyautogui as auto
import numpy as np
import time
import datetime
import os
import pandas as pd
import positioninfo
import pygetwindow as gw
from . import config

def range_click(posinfo):
    position, range = posinfo
    x, y = position
    if type(range)==int:
        dx, dy = range//2, range//2
    elif type(range)==list:
        dx, dy = range
        dx, dy = dx//2, dy//2
    x1 = x+np.random.randint(-dx,dx+1)
    y1 = y+np.random.randint(-dx,dy+1)
    auto.click(x+dx, y+dy, button='left')

def bias_sleep(low, range):
    dt = np.random.rand()*range
    time.sleep(low + dt)

def check(left,top,right,bottom):
    x, y = auto.position()
    if not ((left<x<right)&(top<y<bottom)):
        print('interrupred')
        return False
    else:
        return True
    
def invest(rank):
    global res, savedir
    if not check(x1,y1,x2,y2):
        return False
    if rank>=5:
        r = 5
    else:
        r = rank
    range_click(posdict['r{}'.format(r)])
    bias_sleep(0.7,0.5)
    temp = auto.locateOnScreen(dir+'ref_icon/nickname_1600.png',confidence=0.8)
    if temp is None:
        return -1
    else:
        left, top, dx, dy = temp
    if not check(x1,y1,x2,y2):
        return False
    range_click([[left+dx//2,top+dy//2],[dx//2,dy//2]])
    bias_sleep(0.3,0.3)
    nickname = clip.paste()
    auto.screenshot(f'{savedir}/{rank:0>4}_uid.png', region=scsdict['uid'])
    auto.screenshot(f'{savedir}/{rank:0>4}_power.png',region=scsdict['power'])
    if not check(x1,y1,x2,y2):
        return False
    range_click(posdict['moreinfo'])
    bias_sleep(0.5,0.5)
    auto.screenshot(f'{savedir}/{rank:0>4}_death.png',region=scsdict['death'])
    if not check(x1,y1,x2,y2):
        return False
    range_click(posdict['kills'])
    bias_sleep(0.3,0.3)
    auto.screenshot(f'{savedir}/{rank:0>4}_t4kill.png',region=scsdict['t4kill'])
    auto.screenshot(f'{savedir}/{rank:0>4}_t5kill.png',region=scsdict['t5kill'])
    if not check(x1,y1,x2,y2):
        return False
    range_click(posdict['infoX'])
    bias_sleep(0.5,0.5)
    if not check(x1,y1,x2,y2):
        return False
    range_click(posdict['profX'])
    bias_sleep(0.5,0.5)
    return nickname

win = gw.getWindowsWithTitle('NoxPlayer2')[0]
x1, y1, x2, y2 = win.left, win.top, win.right, win.bottom
if x1<0:
    print('Nox 창을 띄워주세요 (최소화 상태에선 작동하지 않음)')
else:
    print(x1,y1,x2,y2)

basedir = config.basedir
res = config.res
datadir = config.res
kdnum = config.kdnum
t0 = datetime.datetime.now()
t = datetime.datetime.today()
datestr = f'{t.year}{t.month:0>2}{t.day:0>2}'[2:]

try:
    os.mkdir(f'{datadir}kd{kdnum}')
except:
    print('왕국 폴더가 이미 있습니다')

try:
    os.mkdir(f'{datadir}kd{kdnum}/{datestr}')
except:
    print('날짜 폴더가 이미 있습니다')

savedir = f'{datadir}kd{kdnum}/{datestr}'

posdict, scsdict = positioninfo.returndict((1600,900))
x0, y0, _, _ = auto.locateOnScreen(basedir+f'ref_icon/power_{res}.png',confidence=0.9)
for p in posdict.keys():
    temp = posdict[p][0]
    x, y = temp[0]+x0, temp[1]+y0
    posdict[p][0] = [x,y]

for s in scsdict.keys():
    temp = scsdict[s]
    x, y = temp[0]+x0, temp[1]+y0
    scsdict[s] = (x,y,temp[2],temp[3])


nicks = pd.DataFrame(columns=['rank','name'])

range_click(posdict['botprofile'])
bias_sleep(0.3,0.3)
range_click(posdict['rank'])
bias_sleep(0.3,0.3)
range_click(posdict['powerrank'])
bias_sleep(1,0.5)

for rank in range(1,config.maxrank+1):
    if rank%10==1:
        print(f'rank {rank}')
    try:
        nick = invest(rank)
        nicks = nicks.append({'rank':rank,'name':nick},ignore_index=True)
    except:
        print(rank)
        #nicks = nicks.set_index('rank')
        nicks.to_csv(datadir+f'kd{kdnum}/namelist_stopped.csv',encoding="utf-8-sig")
    if not nick:
        break
    elif nick == -1:
        auto.drag(5, -100, 0.5)
        nicks = nicks.append({'rank':rank,'name':"**미접"},ignore_index=True)

nicks = nicks.set_index('rank')
nicks.to_csv(datadir+f'kd{kdnum}/namelist.csv',encoding="utf-8-sig")

t1 = datetime.datetime.now()
dt = t1-t0
dt = dt.seconds
print(f'total time -> {dt//3600}:{dt//60}:{dt%60}')
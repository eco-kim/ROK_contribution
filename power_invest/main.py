import os
import pyautogui as auto
import time
from . import config

basedir = config.basedir
res = config.res
noxdir = config.noxdir
os.startfile(noxdir+'Nox.exe')

def loading(minimum, interval, icon):
    global res
    time.sleep(minimum)
    while True:
        time.sleep(interval)
        try:
            left, top, dx, dy = auto.locateOnScreen(basedir+f'ref_icon/{icon}_{res}.png',confidence=0.8)
            break
        except:
            continue
    return left, top, dx, dy

left, top, dx, dy = loading(30,10,'rok')
auto.click(left+dx//2, top+dy//2, button='left')

left, top, dx, dy = loading(40,20,'power')

os.system('python capture.py')
os.system('python data_ext.py')
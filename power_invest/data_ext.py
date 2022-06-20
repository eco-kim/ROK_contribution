import pandas as pd
import pytesseract
import cv2
import re
import numpy as np
import datetime
from . import config

datadir = config.datadir
kdnum = config.kdnum
maxrank = config.maxrank

namelist = pd.read_csv(f'{datadir}kd{kdnum}/namelist.csv')
params = ['uid','power','t4kill','t5kill','death']

threshdict = {'uid':130, 'power':150, 'death':90, 't4kill':50, 't5kill':50}
langdict = {'uid':'rokuid','power':'eng','death':'rokdeath','t4kill':'rokkill','t5kill':'rokkill'}

df = pd.DataFrame(columns=['name','uid','power','t4kill','t5kill','death'])

t0 = datetime.datetime.now()
t = datetime.datetime.today()
datestr = f'{t.year}{t.month:0>2}{t.day:0>2}'[2:]

for j in range(1,maxrank+1):
    if j%30==1:
        print(j)
    data = {}
    data['name'] = list(namelist[namelist['rank']==j]['name'])[0]
    for p in params:
        im = cv2.imread(f'{datadir}kd{kdnum}/screenshots/{datestr}/{j:0>4}_{p}.png',cv2.IMREAD_GRAYSCALE)
        if im is None:
            check = -1
            break
        if (p=='t4kill')|(p=='t5kill'):
            im2 = np.zeros((34,130), dtype='uint8')
            im2[:,:8] = 229
            im2[:,8:] = im
            im = im2
            im = 255 - im
        _, im = cv2.threshold(im, 0, threshdict[p],cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) 
        text = pytesseract.image_to_string(im, lang=langdict[p],config='--psm 7')
        num = re.findall('\d',text)
        data[p] = ''.join(num)
    df = df.append(data, ignore_index=True)

df.to_csv(f'{datadir}kd{kdnum}/csv/{datestr}data.csv',encoding="utf-8-sig")
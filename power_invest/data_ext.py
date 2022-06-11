import pandas as pd
import pytesseract
import cv2
import re
import numpy as np
import pandas as pd

dir = 'C:/Users/ikho7/Desktop/projects/rok_contribution/power_invest/kd2038/'
date0 = '220511'
namelist = pd.read_csv(dir+'namelist.csv')
params = ['uid','power','t4kill','t5kill','death']

threshdict = {'uid':130, 'power':150, 'death':90, 't4kill':50, 't5kill':50}

#errdict = {'T':'7', 'A':'8','B':'8','$':'5','F':'7','L':'1','TF':'7'}

df = pd.DataFrame(columns=['uid','name','power','t4kill','t5kill','death'])
df2 = pd.DataFrame(columns=['rank','param','text'])
for j in range(1,301):
    if j%30==1:
        print(j)
    data = {}
    data['name'] = list(namelist[namelist['rank']==j]['name'])[0]
    for p in params:
        im = cv2.imread(dir+date0+f'/{j:0>4}_{p}.png',cv2.IMREAD_GRAYSCALE)
        if (p=='t4kill')|(p=='t5kill'):
            im2 = np.zeros((34,130), dtype='uint8')
            im2[:,:8] = 229
            im2[:,8:] = im
            im = im2
            im = 255 - im
        _, im = cv2.threshold(im, 0, threshdict[p],cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) 
        text = pytesseract.image_to_string(im, config='--psm 7')
        num = re.findall('\d',text)
        comma = re.findall(',',text)
        if len(num)+len(comma)+1!=len(text):
            df2 = df2.append({'rank':j,'param':p,'text':text}, ignore_index=True)
        data[p] = ''.join(num)
    df = df.append(data, ignore_index=True)

df.to_csv(dir+f'{date0}data.csv',encoding="utf-8-sig")
df2.to_csv(dir+f'{date0}data_qc.csv',encoding="utf-8-sig")
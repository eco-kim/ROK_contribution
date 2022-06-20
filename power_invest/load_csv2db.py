import pandas as pd
import sys
import glob
import sqlalchemy
from sqlalchemy import create_engine
from . import config

def nancheck(fname):
    df = pd.read_csv(fname).drop('Unnamed: 0', axis=1)
    if len(df[df.isnull()])!=0:
        df = df.dropna(axis=0)
        df = df.reset_index().drop('index', axis=1)
    return df

def float2int(df, clist):
    for column in clist:
        df[column] = df[column].astype('int32')
    return df

dbad = config.dbadress
try:
    engine = create_engine(f'postgresql://{dbad}')
except:
    print('db connection fail')
    sys.exit()

datadir = config.datadir
target = ['opening','closing']
kdnum = config.kdnum
flist = glob.glob(f'{datadir}kd{kdnum}/csv/*.csv')
ll = len(f'{datadir}kd{kdnum}/csv/')
schemaname = f'kd{kdnum}'
for fname in flist:
    df = nancheck(fname)
    df = float2int(df, ['uid','power','t4kill','t5kill','death'])
    df = df.set_index('uid')
    datestr = fname[ll:ll+6]
    tablename = f'ctrb{datestr}'
    engine.execute(f"DROP TABLE IF EXISTS {schemaname}.ctrb{tablename};")
    
    df.to_sql(name = tablename,
        con = engine,
        schema = schemaname,
        index = True,
        index_label = 'uid',
        dtype = {
                'uid': sqlalchemy.types.INTEGER(),
                'name': sqlalchemy.types.VARCHAR(20),
                'power': sqlalchemy.types.INTEGER(),
                't4kill': sqlalchemy.types.INTEGER(),
                't5kill': sqlalchemy.types.INTEGER(),
                'death': sqlalchemy.types.INTEGER(),
                }
            )
    engine.execute(f"ALTER TABLE {schemaname}.{tablename} ADD PRIMARY KEY (uid);")
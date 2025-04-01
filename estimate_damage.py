import os, sys, warnings
from distutils.util import strtobool
import math
import numpy as np
import pandas as pd
from scipy import stats

warnings.simplefilter('ignore')

def estimate_damage(popu_df, lamb, zeta):
    damage_df = popu_df.apply(lambda x: stats.norm.cdf((math.log(x)-lamb)/zeta))
    return damage_df

argvs = sys.argv  # command line argument

# Get input&output file from argment
cama_res = argvs[1] ; in_val = argvs[2] ; pick_num = argvs[3]
flood_path = argvs[4] ; calc_case = argvs[5] ; out_dir = argvs[6] ; out_range = argvs[7]

#cama_res = '1sec' ; in_val = 'household_average.csv' ; pick_num = 'T000876026'
#flood_path = './flood' ; calc_case = 'out' ; out_dir = './damage'
#out_range = '138,139,35,36'

cama_outv = -9999.0

if cama_res == '1sec':
    cell_size = 1/3600
elif cama_res == '3sec':
    cell_size = 1/1200
elif cama_res == '5sec':
    cell_size = 1/720
elif cama_res == '15sec':
    cell_size = 1/240
elif cama_res == '30sec':
    cell_size = 1/120
elif cama_res == '1min':
    cell_size = 1/60

west, east, south, north = [int(x.strip()) for x in out_range.split(',')]
nx_num = int((east-west)/cell_size) ; ny_num = int((north-south)/cell_size)

list_item = ['home_damage', 'house_damage', 'sum_damage']
list_head = 'The_amount_of'
list_unit = '(thousand yen)'
list_case = [str(x.strip()) for x in calc_case.split(',')]

df_cama = pd.DataFrame(np.arange(nx_num*ny_num), columns=['fid'])
df_val = pd.read_csv(in_val).rename(columns={pick_num: 'household'}).groupby('fid').agg({'household':np.sum})
df_cama = df_cama.merge(df_val, on='fid', how='left')

df_home = pd.DataFrame([], columns=list_case)
df_house = pd.DataFrame([], columns=list_case)
df_sum = pd.DataFrame([], columns=list_case)

df_cama['home'] = df_cama['household']*(9801+3441)
df_cama['house'] = df_cama['household']*(3957)
df_cama['sum'] = df_cama['home'] + df_cama['house']

if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

for calc in [x.strip() for x in calc_case.split(',')]:
    calc_name = 'flood_' + calc
    cama_file = os.path.join(flood_path, calc_name+'.bin')
    df_cama['fld_dph'] = np.fromfile(cama_file, dtype='float32')
    df_cama['fld_dph'].replace(0, np.nan, inplace=True)
    df_cama['fld_dph'].replace(cama_outv, np.nan, inplace=True)
    df_cama['home_rate'] = np.nan ; df_cama['house_rate'] = np.nan
    df_mask = df_cama['fld_dph'].loc[df_cama['fld_dph'].notna().tolist()]
    df_cama['home_rate'].where(df_cama['fld_dph'] == np.nan, estimate_damage(df_mask, 1.895, 3.374), inplace=True)
    df_cama['house_rate'].where(df_cama['fld_dph'] == np.nan, estimate_damage(df_mask, 0.188, 2.449), inplace=True)
    df_cama['home_damage'] = df_cama['home']*df_cama['home_rate']
    df_cama['house_damage'] = df_cama['house']*df_cama['house_rate']
    df_cama['sum_damage'] = df_cama['home_damage'] + df_cama['house_damage']

    df_home[calc] = df_cama['home_damage'].copy()
    df_house[calc] = df_cama['house_damage'].copy()
    df_sum[calc] = df_cama['sum_damage'].copy()

out_csv = os.path.join(out_dir, 'total')
df_home.sum(axis=0).to_csv(out_csv+'_home.csv')
df_house.sum(axis=0).to_csv(out_csv+'_house.csv')
df_sum.sum(axis=0).to_csv(out_csv+'_sum.csv')

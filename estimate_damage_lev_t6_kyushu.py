import os, sys, warnings
from distutils.util import strtobool
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy import stats
from shapely.geometry import Polygon
from shapely.ops import unary_union


warnings.simplefilter('ignore')

class BoundaryNorm(colors.Normalize):
    def __init__(self, boundaries):
        self.vmin = boundaries[0]
        self.vmax = boundaries[-1]
        self.boundaries = boundaries
        self.N = len(self.boundaries)

    def __call__(self, x, clip=False):
        x = np.asarray(x)
        ret = np.zeros(x.shape, dtype=np.int)
        for i, b in enumerate(self.boundaries):
            ret[np.greater_equal(x, b)] = i
        ret[np.less(x, self.vmin)] = -1
        ret = np.ma.asarray(ret / float(self.N-1))
        return ret

def estimate_damage(popu_df, lamb, zeta):

    def safe_log(x):
       if 30 > x > 0:
          return math.log(x)
       else:
          return np.nan  # or handle as needed, e.g., return 0 or np.nan

    damage_df = popu_df.apply(lambda x: stats.norm.cdf((safe_log(x)-lamb)/zeta))
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

df_val1 = pd.read_csv(in_val).rename(columns={pick_num: 'household'})

df_val2 = df_val1.groupby('fid').agg({
    'household': np.sum,
    'area': np.sum,
    'lon1': 'first',
    'lat1': 'first',
#    'geometry': lambda x: unary_union(x.tolist())
})

df_cama = df_cama.merge(df_val2, on='fid', how='left')
df_cama = df_cama.astype('float32')  # This will convert all columns to float16

df_home = pd.DataFrame([], columns=list_case)
df_house = pd.DataFrame([], columns=list_case)
df_homeori = pd.DataFrame([], columns=list_case)
df_houseori = pd.DataFrame([], columns=list_case)
#df_sum = pd.DataFrame([], columns=list_case)

if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

for calc in [x.strip() for x in calc_case.split(',')]:
    calc_name = 'flood_' + calc
    calc_nameori = 'flood_out4_' + calc
    cama_file = os.path.join(flood_path, calc_name+'.bin')
    cama_file1 = os.path.join(flood_path, 'flood_lev_c000_zero_kyushul5.bin')

    cama_fileori = os.path.join(flood_path, calc_nameori+'.bin')
    cama_fileori1 = os.path.join(flood_path, 'flood_out4_lev_c000_zero_kyushul5.bin')

    df_cama['fld_dph'] = np.fromfile(cama_file, dtype='float32')
    df_cama['fld_dph1'] = np.fromfile(cama_file1, dtype='float32')
    df_cama['fld_dph'].replace(0, np.nan, inplace=True)
    df_cama['fld_dph'].replace(cama_outv, np.nan, inplace=True)
    df_cama.loc[df_cama['fld_dph'] >= 100, 'fld_dph'] -= 100    
    df_cama.loc[df_cama['fld_dph'] < 0, 'fld_dph'] = np.nan    
    df_cama['home_rate'] = np.nan ; 
    df_mask = df_cama['fld_dph'].loc[df_cama['fld_dph'].notna().tolist()]
    df_cama['home_rate'].where(df_cama['fld_dph'] == np.nan, estimate_damage(df_mask, 1.826, 2.355), inplace=True)

    df_cama['fld_dphori'] = np.fromfile(cama_fileori, dtype='float32')
    df_cama['fld_dphori1'] = np.fromfile(cama_fileori1, dtype='float32')
    df_cama['fld_dphori'].replace(0, np.nan, inplace=True)
    df_cama['fld_dphori'].replace(cama_outv, np.nan, inplace=True)
    df_cama.loc[df_cama['fld_dphori'] >= 100, 'fld_dphori'] -= 100    
    df_cama.loc[df_cama['fld_dphori'] < 0, 'fld_dphori'] = np.nan    
    df_cama['home_rateori'] = np.nan ; 
    df_maskori = df_cama['fld_dphori'].loc[df_cama['fld_dphori'].notna().tolist()]
    df_cama['home_rateori'].where(df_cama['fld_dphori'] == np.nan, estimate_damage(df_maskori, 1.826, 2.355), inplace=True)

#    df_cama.loc[df_cama['fld_dph'] < 2.0, 'home_rate'] = 0.266   
    df_cama.loc[df_cama['fld_dph'] < 1.0, 'home_rate'] = 0.119  
    df_cama.loc[df_cama['fld_dph'] < 0.5, 'home_rate'] = 0.092    
    df_cama.loc[df_cama['fld_dph'] < 0.45, 'home_rate'] = 0.032  
    df_cama.loc[df_cama['fld_dph'] < 0.3, 'home_rate'] = 0  
    df_cama.loc[df_cama['fld_dph1'] > 0, 'home_rate'] = 0   

    df_cama.loc[df_cama['fld_dphori'] < 1.0, 'home_rateori'] = 0.119  
    df_cama.loc[df_cama['fld_dphori'] < 0.5, 'home_rateori'] = 0.092    
    df_cama.loc[df_cama['fld_dphori'] < 0.45, 'home_rateori'] = 0.032  
    df_cama.loc[df_cama['fld_dphori'] < 0.3, 'home_rateori'] = 0  
    df_cama.loc[df_cama['fld_dphori1'] > 0, 'home_rateori'] = 0  

    household_sum = df_cama['household'].sum(axis=0)
    with open(f'test19_{calc_name}_household.csv', 'w') as f:
        f.write(f"household_sum,{household_sum}")

    df_cama.loc[df_cama['household'] < 0.5, 'household'] = 0
    df_cama['floor'] = 1/np.ceil(df_cama['household']*500/df_cama['area'])
    
    df_cama['home_damage'] = df_cama['household']*df_cama['home_rate']*(9.801+3.441+3.957)*df_cama['floor']
    df_cama['house_damage'] = df_cama['household']*df_cama['home_rate']*df_cama['floor']

    df_cama['home_damageori'] = df_cama['household']*df_cama['home_rateori']*(9.801+3.441+3.957)*df_cama['floor']
    df_cama['house_damageori'] = df_cama['household']*df_cama['home_rateori']*df_cama['floor']

    home_sum = df_cama['home_damage'].sum(axis=0)
    with open(f'test19a_{calc_name}_home.csv', 'w') as f:
        f.write(f"home_damage_sum,{home_sum}")
    
    house_sum = df_cama['house_damage'].sum(axis=0)
    with open(f'test19a_{calc_name}_house.csv', 'w') as f:
        f.write(f"house_damage_sum,{house_sum}")

    home_sumori = df_cama['home_damageori'].sum(axis=0)
    with open(f'test19a_{calc_name}_homeori.csv', 'w') as f:
        f.write(f"home_damage_sumori,{home_sumori}")
    
    house_sumori = df_cama['house_damageori'].sum(axis=0)
    with open(f'test19a_{calc_name}_houseori.csv', 'w') as f:
        f.write(f"house_damage_sumori,{house_sumori}")
    
#    df_home[calc] = np.nan; df_house[calc] = np.nan
    df_home[calc] = np.nan; df_house[calc] = np.nan; df_homeori[calc] = np.nan; df_houseori[calc] = np.nan;

#    df_home[calc] = df_cama['home_damage'].copy()
#    df_house[calc] = df_cama['house_damage'].copy()

    df_home[calc] = df_cama['home_damage'].astype('float32').copy()
    df_house[calc] = df_cama['house_damage'].astype('float32').copy()

    df_homeori[calc] = df_cama['home_damageori'].astype('float32').copy()
    df_houseori[calc] = df_cama['house_damageori'].astype('float32').copy()
    
    df_cama[df_cama['fld_dphori'] > 0.1].to_csv('test18_'+calc_name+'.csv')
#    df_cama[df_cama['fld_dph'] > 0.1].to_csv('test19_'+calc_name+'.csv')
    #df_cama[df_cama['home_damage'] > 2.0].to_csv('test13_'+calc_name+'.csv')
#    df_cama.drop(['fld_dph1', 'home_rate', 'floor'], axis=1, inplace=True)
#    df_cama.to_csv('test14_'+calc_name+'.csv')

out_csv = os.path.join(out_dir, 'total_kyushu5f10')
df_home.sum(axis=0).to_csv(out_csv+'_home.csv')
df_house.sum(axis=0).to_csv(out_csv+'_house.csv')
df_homeori.sum(axis=0).to_csv(out_csv+'_homeori.csv')
df_houseori.sum(axis=0).to_csv(out_csv+'_houseori.csv')

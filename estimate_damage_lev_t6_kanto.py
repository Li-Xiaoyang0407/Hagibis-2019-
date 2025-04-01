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

def parse_polygon(polygon_str):
    coords = polygon_str.replace('POLYGON ((', '').replace('))', '').split(', ')
    coords = [tuple(map(float, coord.split())) for coord in coords]
    return Polygon(coords)

def plot_household_distribution(df, cell_size, west, east, south, north, pick_num):
    # Create a grid for the plot
    lon_bins = np.arange(west, east, cell_size)
    lat_bins = np.arange(south, north, cell_size)
    
    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon1, df.lat1))
    
    # Plot the household distribution
    fig, ax = plt.subplots(figsize=(12, 8))
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.boundary.plot(ax=ax, linewidth=1)

    interval=(0.0, 10, 20, 30, 40, 50, 60, 70, 80, 90)
#    interval=(0.0, 1, 2, 3, 4, 5, 6, 7, 8, 9)    
#    interval=(-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5)
    norml=colors.BoundaryNorm(interval,256)    
    # Plot the points
    gdf.plot(ax=ax, column=pick_num, cmap='OrRd', norm=norml, markersize=5)
    #gdf.plot(ax=ax, column=pick_num, cmap='seismic', norm=norml, markersize=0.1)
    #gdf.plot(ax=ax, column=pick_num, cmap='OrRd', norm=norml, markersize=5)
#    im2=plt.imshow(dphw040,cmap=cm.YlGnBu,norm=norml,extent=(west,east,south,north))
    # Manually add colorbar 

    #sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=gdf[pick_num].min(), vmax=gdf[pick_num].max()))
    #sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=gdf[pick_num].min(), vmax=10))
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=norml)
    #sm = plt.cm.ScalarMappable(cmap='seismic', norm=plt.Normalize(vmin=-5, vmax=5))
    sm._A = []
    cbar = plt.colorbar(sm, ax=ax)
    #cbar.set_label("flood water depth (m)")
    #cbar.set_label("Difference in depth (m)")
    #cbar.set_label("Difference in damage (million yen)")   
    cbar.set_label("Flood damage (million yen)")
    plt.title("Flood damage distribution (without lev)")
    #plt.title("flood depth Distribution (without lev)")
    #plt.title("dph_ori - dph_lev")    
#    plt.title("damage_ori - damage_lev") 
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Set the x and y limits to the specified range
    plt.xlim(west, east)
    plt.ylim(south, north)
    plt.grid(True)
    
#    plt.savefig("./fig/flddph_hokkaido.jpg")
#    plt.savefig("./flddph_t3_dif_dph.png")
#    plt.savefig("./flddph_t3_dif_damage.png")
    plt.savefig("./flddph_t3_ori_damage.png")
#    plt.savefig("./flddph_t3_ori_dph.png")
#    plt.show()

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

#df_cama1 = pd.DataFrame(np.arange(nx_num*ny_num), columns=['fid', 'lon1', 'lat1'])

##df_val = pd.read_csv(in_val).rename(columns={pick_num: 'household'}).groupby('fid').agg({'household':np.sum, 'area': np.sum})
##df_val.to_csv('test3a.csv')
df_val1 = pd.read_csv(in_val).rename(columns={pick_num: 'household'})
###df_val1.to_csv('test0.csv')

####df_val1['geometry'] = df_val1['geometry'].apply(parse_polygon)
#df['geometry'] = df['geometry'].apply(parse_polygon)
###df_val1.to_csv('test0a.csv')

df_val2 = df_val1.groupby('fid').agg({
    'household': np.sum,
    'area': np.sum,
    'lon1': 'first',
    'lat1': 'first',
#    'geometry': lambda x: unary_union(x.tolist())
})
###df_val2.to_csv('test0c.csv')
#gdf = gpd.GeoDataFrame(df_val2, crs='EPSG:4326', geometry='geometry')

df_cama = df_cama.merge(df_val2, on='fid', how='left')
df_cama = df_cama.astype('float32')  # This will convert all columns to float16
#df_cama.to_csv('test1.csv')

##df_cama1 = df_cama.merge(df_val1[['fid', 'lon1', 'lat1', 'geometry', 'area']], on='fid', how='left')
#df_cama1.to_csv('test2.csv')

##df_cama2 = df_cama1.drop_duplicates(subset=['fid', 'lon1', 'lat1'])
#df_cama2.to_csv('test2a.csv')

df_home = pd.DataFrame([], columns=list_case)
df_house = pd.DataFrame([], columns=list_case)
#df_homeori = pd.DataFrame([], columns=list_case)
#df_houseori = pd.DataFrame([], columns=list_case)
#df_sum = pd.DataFrame([], columns=list_case)

#df_cama['home'] = df_cama['household']*(9801+3441)/1000
#df_cama['house'] = df_cama['household']*(3957)/1000
#df_cama['sum'] = df_cama['home'] + df_cama['house']

#df_cama['home1'] = df_cama['home']
#df_cama['house1'] = df_cama['house']
#df_cama3 = df_cama.merge(df_cama2[['fid', 'lon1', 'lat1']], on='fid', how='left')
#df_cama3.to_csv('test1b.csv')

if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

for calc in [x.strip() for x in calc_case.split(',')]:
    calc_name = 'flood_' + calc
#    calc_nameori = 'flood_out4_' + calc
    cama_file = os.path.join(flood_path, calc_name+'.bin')
    cama_file1 = os.path.join(flood_path, 'flood_lev_c000_zero_kantol4.bin')

#    cama_fileori = os.path.join(flood_path, calc_nameori+'.bin')
#    cama_fileori1 = os.path.join(flood_path, 'flood_out4_lev_c000_zero_kantol4.bin')

    df_cama['fld_dph'] = np.fromfile(cama_file, dtype='float32')
    df_cama['fld_dph1'] = np.fromfile(cama_file1, dtype='float32')
    df_cama['fld_dph'].replace(0, np.nan, inplace=True)
    df_cama['fld_dph'].replace(cama_outv, np.nan, inplace=True)
    df_cama.loc[df_cama['fld_dph'] >= 100, 'fld_dph'] -= 100
    df_cama.loc[df_cama['fld_dph'] < 0, 'fld_dph'] = np.nan 
    df_mask = df_cama['fld_dph'].loc[df_cama['fld_dph'].notna().tolist()]

#    df_cama['fld_dphori'] = np.fromfile(cama_fileori, dtype='float32')
#    df_cama['fld_dphori1'] = np.fromfile(cama_fileori1, dtype='float32')
#    df_cama['fld_dphori'].replace(0, np.nan, inplace=True)
#    df_cama['fld_dphori'].replace(cama_outv, np.nan, inplace=True)
#    df_cama.loc[df_cama['fld_dphori'] >= 100, 'fld_dphori'] -= 100
#    df_cama.loc[df_cama['fld_dphori'] < 0, 'fld_dphori'] = np.nan 
#    df_maskori = df_cama['fld_dphori'].loc[df_cama['fld_dphori'].notna().tolist()]

   
    df_cama['home_rate'] = np.nan ; 
    df_cama['home_rate'].where(df_cama['fld_dph'] == np.nan, estimate_damage(df_mask, 1.826, 2.355), inplace=True)

#    df_cama['home_rate'].where(df_cama['fld_dph'] == np.nan, estimate_damage(df_mask, 1.895, 3.374), inplace=True)

#    df_cama['home_rateori'] = np.nan ; 
#    df_cama['home_rateori'].where(df_cama['fld_dphori'] == np.nan, estimate_damage(df_maskori, 1.826, 2.355), inplace=True)


#    df_cama.loc[df_cama['fld_dph'] < 2.0, 'home_rate'] = 0.266   
    df_cama.loc[df_cama['fld_dph'] < 1.0, 'home_rate'] = 0.119  
    df_cama.loc[df_cama['fld_dph'] < 0.5, 'home_rate'] = 0.092    
    df_cama.loc[df_cama['fld_dph'] < 0.45, 'home_rate'] = 0.032  
    df_cama.loc[df_cama['fld_dph'] < 0.3, 'home_rate'] = 0  
    df_cama.loc[df_cama['fld_dph1'] > 0, 'home_rate'] = 0  

#    df_cama.loc[df_cama['fld_dphori'] < 1.0, 'home_rateori'] = 0.119  
#    df_cama.loc[df_cama['fld_dphori'] < 0.5, 'home_rateori'] = 0.092    
#    df_cama.loc[df_cama['fld_dphori'] < 0.45, 'home_rateori'] = 0.032  
#    df_cama.loc[df_cama['fld_dphori'] < 0.3, 'home_rateori'] = 0  
#    df_cama.loc[df_cama['fld_dphori1'] > 0, 'home_rateori'] = 0  

    household_sum = df_cama['household'].sum(axis=0)
    with open(f'test19_{calc_name}_household.csv', 'w') as f:
        f.write(f"household_sum,{household_sum}")

    df_cama.loc[df_cama['household'] < 0.5, 'household'] = 0  
    df_cama['floor'] = 1/np.ceil(df_cama['household']*500/df_cama['area'])

    
    df_cama['home_damage'] = df_cama['household']*df_cama['home_rate']*(9.801+3.441+3.957)*df_cama['floor']
    df_cama['house_damage'] = df_cama['household']*df_cama['home_rate']*df_cama['floor']

#    df_cama['home_damageori'] = df_cama['household']*df_cama['home_rateori']*(9.801+3.441+3.957)*df_cama['floor']
#    df_cama['house_damageori'] = df_cama['household']*df_cama['home_rateori']*df_cama['floor']

    home_sum = df_cama['home_damage'].sum(axis=0)
    with open(f'test19_{calc_name}_home.csv', 'w') as f:
        f.write(f"home_damage_sum,{home_sum}")
    
    house_sum = df_cama['house_damage'].sum(axis=0)
    with open(f'test19_{calc_name}_house.csv', 'w') as f:
        f.write(f"house_damage_sum,{house_sum}")

#    home_sumori = df_cama['home_damageori'].sum(axis=0)
#    with open(f'test18_{calc_name}_homeori.csv', 'w') as f:
#        f.write(f"home_damage_sumori,{home_sumori}")
    
#    house_sumori = df_cama['house_damageori'].sum(axis=0)
#    with open(f'test18_{calc_name}_houseori.csv', 'w') as f:
#        f.write(f"house_damage_sumori,{house_sumori}")
    
    df_home[calc] = np.nan; df_house[calc] = np.nan

    df_home[calc] = df_cama['home_damage'].astype('float32').copy()
    df_house[calc] = df_cama['house_damage'].astype('float32').copy()

#    df_homeori[calc] = df_cama['home_damageori'].astype('float32').copy()
#    df_houseori[calc] = df_cama['house_damageori'].astype('float32').copy()

#    df_home[calc] = df_cama['home_damage'].copy()
#    df_house[calc] = df_cama['house_damage'].copy()
#    df_sum[calc] = df_cama['sum_damage'].copy()

##    df_cama4 = df_cama.merge(df_cama2[['fid', 'lon1', 'lat1', 'geometry']], on='fid', how='left')
##    df_cama.to_csv('test3_'+calc_name+'.csv')    

#    df_cama[df_cama['fld_dphori'] > 0.1].to_csv('test18_'+calc_name+'.csv')
    df_cama[df_cama['fld_dph'] > 0.1].to_csv('test19_'+calc_name+'.csv')
#    df_cama[df_cama['home_damage'] > 2.0].to_csv('test15f10_'+calc_name+'.csv')
#    df_cama.drop(['fld_dph1', 'home_rate', 'floor'], axis=1, inplace=True)
#    df_cama.to_csv('test14_'+calc_name+'.csv')

out_csv = os.path.join(out_dir, 'total_kanto4e6')
df_home.sum(axis=0).to_csv(out_csv+'_home.csv')
df_house.sum(axis=0).to_csv(out_csv+'_house.csv')
#df_homeori.sum(axis=0).to_csv(out_csv+'_homeori.csv')
#df_houseori.sum(axis=0).to_csv(out_csv+'_houseori.csv')


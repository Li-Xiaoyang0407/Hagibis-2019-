import os, sys, warnings
from distutils.util import strtobool
import math
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from scipy import stats


warnings.simplefilter('ignore')

def write_geojson_file(head, gdf):
    gdf.to_file(head + '.geojson', driver='GeoJSON')

def calc_area_val(rarea_df, para_list, sum_area):
    areav_df = rarea_df
    for para in para_list:
        areav_df[para] = rarea_df[para]/rarea_df[sum_area]
    return areav_df

def calc_area_ratio(oarea_df, group_list, para_list):
    sarea_df = oarea_df
    for para in para_list:
        sarea_df[para] = oarea_df[para]*oarea_df['area']
    agg_dict = {'area':np.sum}
    rarea_df = oarea_df.groupby(group_list, as_index=False).agg(agg_dict)
    return sarea_df.merge(rarea_df, on=group_list, suffixes=['', '_sum'])

def calc_over_area(poly_gdf, para_gdf, group_list, para_list):
    inter_df = gpd.overlay(poly_gdf.to_crs('epsg:3410'), para_gdf.to_crs('epsg:3410'), how='intersection')
    inter_df['area'] = inter_df['geometry'].area
    agg_dict = {para:np.mean for para in para_list} ; agg_dict['area'] = np.sum
    oarea_df = inter_df.groupby(group_list, as_index=False).agg(agg_dict)
    return oarea_df

def make_2dpoly_lonlat(nx, ny, lon, lat, crs):
    poly = gpd.GeoDataFrame(crs=crs, geometry=[])
    idpoly = [] ; geopoly = []
    for j in range(ny+1):
        for i in range(nx+1):
            if i != nx and j != ny:
                id = nx*j + i
                gpoly = Polygon([(lon[i],lat[j]), (lon[i+1],lat[j]), (lon[i+1],lat[j+1]), (lon[i],lat[j+1])])
                idpoly.append(id) ; geopoly.append(gpoly)
    poly['fid'] = idpoly ; poly['geometry'] = geopoly
    return poly

argvs = sys.argv  # command line argument

# Get input&output file from argment
mesh_path = argvs[1] ; popu_path = argvs[2] ; popu_case = argvs[3] ; pick_num = argvs[4]
out_range = argvs[5] ; cama_res = argvs[6] ; out_name = argvs[7]

#mesh_path = '/data29/y-miura/Land_data/region_mesh/mesh'
#popu_path = '/data29/y-miura/Land_data/region_mesh/No1'
#popu_case = 'tblT000876Q' ; pick_num = 'T000876026'
#out_range = '138,139,35,36' ; cama_res = '1sec' ; out_name = 'household_average'

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

np_lon = np.linspace(west, east, nx_num+1) ; np_lat = np.linspace(north, south, ny_num+1)
gdf_cama = make_2dpoly_lonlat(nx_num, ny_num, np_lon, np_lat, 'epsg:4326')

#write_geojson_file('cama', gdf_cama)

list_mesh = ['KEY_CODE', pick_num, 'geometry']
list_drop = ['MESH1_ID', 'MESH2_ID', 'MESH3_ID', 'MESH4_ID', 'MESH5_ID', 'OBJ_ID']
gdf_popu = gpd.GeoDataFrame(columns=list_mesh, crs='epsg:4612')

yy = [] ; xx = []
for lat in range(south, north+1):
    yy.append(int(math.ceil((lat-20)*1.5) + 30))
    for lon in range(west, east+1):
        xx.append(int(lon - 100.0))

print(yy)
print(xx)

for y in range(yy[0], yy[-1]+1):
    for x in range(xx[0], xx[-1]+1):
        mesh_name = 'MESH0' + str(y) + str(x) + '.shp'
        popu_name = popu_case + str(y) + str(x) + '.txt'
        try:
            gdf_mesh = gpd.read_file(os.path.join(mesh_path, mesh_name)).drop(list_drop, axis=1)
        except FileNotFoundError:
            print(f"File not found: {mesh_name}")
            continue  
        except Exception as e:
            print(f"Error processing {mesh_name}: {e}")
            continue  

        try:        
            df_popu = pd.read_csv(os.path.join(popu_path, popu_name), encoding='shift-jis', skiprows=[1])[['KEY_CODE', pick_num]]
            df_popu = df_popu.astype({'KEY_CODE': 'str'})
            gdf_popu = pd.concat([gdf_popu, gdf_mesh.merge(df_popu, on='KEY_CODE')])
        except FileNotFoundError:
            print(f"File not found: {popu_name}")
        except Exception as e:
            print(f"Error processing {popu_name}: {e}")
  
list_group = ['fid', 'KEY_CODE']
# Calculate overlap area
df_oarea = calc_over_area(gdf_cama, gdf_popu, list_group, pick_num.split())

# Calculate area ratio
df_arear = calc_area_ratio(df_oarea, 'KEY_CODE', pick_num.split())

# Calculate area average value
df_areav = calc_area_val(df_arear, pick_num.split(), 'area_sum')
df_areav.drop(['KEY_CODE', 'area', 'area_sum'], axis=1, inplace=True)
df_areav.to_csv(out_name + '.csv')

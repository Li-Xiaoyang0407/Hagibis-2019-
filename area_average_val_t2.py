import os, sys, warnings
from distutils.util import strtobool
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
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
    idpoly = [] ; geopoly = [] ; lonpoly = [] ; latpoly = []
    for j in range(ny+1):
        for i in range(nx+1):
            if i != nx and j != ny:
                id = nx*j + i
                gpoly = Polygon([(lon[i],lat[j]), (lon[i+1],lat[j]), (lon[i+1],lat[j+1]), (lon[i],lat[j+1])])
                lnpoly = (lon[i]+lon[i+1])*0.5
                ltpoly = (lat[j]+lat[j+1])*0.5
                idpoly.append(id) ; geopoly.append(gpoly) ; lonpoly.append(lnpoly) ; latpoly.append(ltpoly)
    poly['fid'] = idpoly ; poly['geometry'] = geopoly ; poly['lon1'] = lonpoly ; poly['lat1'] = latpoly
    return poly

def parse_polygon(polygon_str):
    coords = polygon_str.replace('POLYGON ((', '').replace('))', '').split(', ')
    coords = [tuple(map(float, coord.split())) for coord in coords]
    return Polygon(coords)

#def plot_household_distribution(df, cell_size, west, east, south, north, pick_num):
    # Create a grid for the plot
#    lon_bins = np.arange(west, east, cell_size)
#    lat_bins = np.arange(south, north, cell_size)
    
    # Convert the DataFrame to a GeoDataFrame
    #gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon1, df.lat1))
    #df['geometry'] = df['geometry'].apply(lambda x: Polygon(eval(x.split('POLYGON ')[1])))
    #df['geometry'] = df['geometry']
    #df['geometry'] = df['geometry'].apply(parse_polygon)
    #polygon = Polygon(df.geometry)
#    gdf = gpd.GeoDataFrame(df, crs='EPSG:4326', geometry='geometry')
#    gdf = gdf.to_crs('EPSG:3410')
    # Plot the household distribution
#    fig, ax = plt.subplots(figsize=(12, 8))
    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #world.boundary.plot(ax=ax, linewidth=1)
    
    # Plot the points
    #gdf.plot(ax=ax, column=pick_num, cmap='OrRd', markersize=5)
#    gdf.plot(ax=ax, column=pick_num, cmap='OrRd')
    # Manually add colorbar
#    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=gdf[pick_num].min(), vmax=gdf[pick_num].max()))
#    sm._A = []
#    cbar = plt.colorbar(sm, ax=ax)
#    cbar.set_label("Number of Households")
    
#    plt.title("Household Distribution")
#    plt.xlabel("Longitude")
#    plt.ylabel("Latitude")

    # Set the x and y limits to the specified range
#    plt.xlim(west, east)
#    plt.ylim(south, north)
#    plt.grid(True)
    
#    plt.savefig("./fig/flddph_hokkaido.jpg")
#    plt.savefig("./flddph_t3.png")
#    plt.show()

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
  
##list_group = ['fid', 'KEY_CODE', 'lon1', 'lat1', 'geometry'] 
list_group = ['fid', 'KEY_CODE', 'lon1', 'lat1']
# Calculate overlap area
df_oarea = calc_over_area(gdf_cama, gdf_popu, list_group, pick_num.split())

# Calculate area ratio
df_arear = calc_area_ratio(df_oarea, 'KEY_CODE', pick_num.split())

# Calculate area average value
df_areav = calc_area_val(df_arear, pick_num.split(), 'area_sum')
#df_areav.drop(['KEY_CODE', 'area', 'area_sum'], axis=1, inplace=True)
df_areav.to_csv(out_name + '.csv')

# Plot household distribution
# plot_household_distribution(gdf_cama, cell_size, west, east, south, north)
#plot_household_distribution(df_areav, cell_size, west, east, south, north, pick_num)
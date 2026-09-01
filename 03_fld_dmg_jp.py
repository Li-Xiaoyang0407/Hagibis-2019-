import sys
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from rasterio.features import rasterize
import numpy as np
import math
from scipy import stats
from scipy.special import ndtr

Runoff = sys.argv[1] ; Route = sys.argv[2]
# ==== File paths ====
building_raster = "./tif/japan_building_area_count_1secn.tif"
output_tif = f"./tif/jp_fld_dmgn_lev{Runoff}_{Route}.tif"
fld_raster = f"./tif/jp_fld_dphn_lev{Runoff}_{Route}.tif"

# ==== Flood binary format ====
dtype = np.float32  # or np.uint16 etc.
shape = (57600, 61200)  # (rows, cols) ? must match GeoTIFF shape
bbox = (129.0, 46.0, 1/3600, 1/3600)  # (lon_min, lat_max, xres, yres)
crs = "EPSG:4326"

# ==== Read flood raster metadata ====
with rasterio.open(fld_raster) as csrc:
    depth = csrc.read(1)
    flood_meta = csrc.meta.copy()

# ==== Read building raster metadata ====
with rasterio.open(building_raster) as bsrc:
    area = bsrc.read(1)
    building_meta = bsrc.meta.copy()


def damage_ratio1(depth):
    depth = depth.astype(np.float32)
    return np.where(
        depth < 0.05, 0,
        np.where(depth < 0.45, 0.044,
        np.where(depth < 0.5, 0.126,
        np.where(depth < 1.0, 0.176,
        np.where(depth < 2.0, 0.343,
        np.where(depth < 3.0, 0.647, 0.870)))))).astype(np.float32)


def damage_ratio2(depth):
    depth = depth.astype(np.float32)
    return np.where(
        depth < 0.05, 0,
        np.where(depth < 0.45, 0.021,
        np.where(depth < 0.5, 0.145,
        np.where(depth < 1.0, 0.326,
        np.where(depth < 2.0, 0.508,
        np.where(depth < 3.0, 0.928, 0.991)))))).astype(np.float32)

# ==== Parameters ====
unit_cost1 = 0.037054  # House Asset 1000000JPY per m2
unit_cost2 = 0.09178  #House content 1000000JPY per m2
#unit_cost = unit_cost1 + unit_cost2
area = np.where(area < 0, 0, area)

# ==== Calculate damage ====
dmg_ratio1 = damage_ratio1(depth.astype(np.float32))
dmg_ratio2 = damage_ratio2(depth.astype(np.float32))

area = area.astype(np.float32)
dmg_ratio1 = dmg_ratio1.astype(np.float32)
dmg_ratio2 = dmg_ratio2.astype(np.float32)
damage = area * (dmg_ratio1 * unit_cost1 + dmg_ratio2 * unit_cost2)
damage = np.where(damage < 0, 0, damage)

# ==== Save GeoTIFF ====
building_meta.update({
    "count": 1,
    "dtype": "float32",
    "compress": "lzw"
})
with rasterio.open(output_tif, "w", **building_meta) as dst:
    dst.write(damage.astype("float32"), 1)

print(f"? Flood damage raster saved: {output_tif}")

total = np.sum(damage)
print(f"Total estimated damage: \{total:,.0f}")

# Option 1: Save as a 1-element row
np.savetxt(f"./csv/flood_damage_flat_jp_lev{Runoff}_{Route}.csv", [total], delimiter=",")

# Option 2: Save as a 1x1 array (row and column)
np.savetxt(f"./csv/flood_damage_flat_jp_lev{Runoff}_{Route}.csv", [[total]], delimiter=",")
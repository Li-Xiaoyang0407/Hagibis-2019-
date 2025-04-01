import os, sys, warnings
import datetime
from distutils.util import strtobool
import netCDF4
import numpy as np

warnings.simplefilter('ignore')

def write_binary(out_data, out_name):
    with open(out_name, 'wb') as bfile:
        out_data.tofile(bfile)

def read_ils_cdf(ncfile, vari, noval):
    nc = netCDF4.Dataset(ncfile, 'r')
    lon = int(nc.dimensions['longitude'].size) ; lat = int(nc.dimensions['latitude'].size)
    time = int(nc.dimensions['time'].size)
    data = nc.variables[vari][:] ; data[np.where(data <= noval)] = np.nan
    return lon, lat, time, data

argvs = sys.argv  # command line argument

if len(argvs) < 10:
    ils_path = argvs[1] ; calc_date = argvs[2] ; pick_date = argvs[3]
    calc_dir = argvs[4] ; pick_val = argvs[5] ; unit_conv = int(argvs[6])
    ils_outv = float(argvs[7]) ; out_dir = argvs[8] ; base_dir = ''
else:
    ils_path = argvs[1] ; calc_date = argvs[2] ; pick_date = argvs[3]
    calc_dir = argvs[4] ; pick_val = argvs[5] ; unit_conv = int(argvs[6])
    ils_outv = float(argvs[7]) ; out_dir = argvs[8] ; base_dir = argvs[9]

#ils_path = '../runs' ; calc_date = '2019/10/01' ; pick_date = '2019/10/11-2019/10/18'
#calc_dir = 'out' ; pick_val = 'flddph' ; unit_conv = 1
#ils_outv = -999.0 ; out_dir = './convert' ; base_dir = ''

cama_outv = 1.0e+20

calc_sdate = datetime.datetime.strptime(calc_date, '%Y/%m/%d')
pick_sdate = datetime.datetime.strptime(pick_date.split('-')[0], '%Y/%m/%d')
pick_edate = datetime.datetime.strptime(pick_date.split('-')[1], '%Y/%m/%d')
sta_dnum = (pick_sdate-calc_sdate).days*24 ; end_dnum = ((pick_edate-calc_sdate).days+1)*24
hour_num = end_dnum - sta_dnum

calc_file = os.path.join(ils_path, calc_dir, pick_val + '.nc')
nx, ny, ils_time, read_calc = read_ils_cdf(calc_file, pick_val, ils_outv)

if len(base_dir) != 0:
    base_file = os.path.join(ils_path, base_dir, pick_val + '.nc')
    nx, ny, ils_time, read_base = read_ils_cdf(base_file, pick_val, ils_outv)
else:
    read_base = np.zeros(ils_time*ny*nx)

read_calc = read_calc.reshape(ils_time, ny*nx) ; read_base = read_base.reshape(ils_time, ny*nx)
pick_calc = read_calc[sta_dnum:end_dnum,:].reshape(hour_num, ny, nx)
pick_base = read_base[sta_dnum:end_dnum,:].reshape(hour_num, ny, nx)

np_calc = np.where(pick_calc == ils_outv, np.nan, pick_calc)
np_base = np.where(pick_base == ils_outv, np.nan, pick_base)

np_max = np.max(np_calc-np_base, axis=0)
np_max[np.isnan(np_max)] = cama_outv

np_write = np.full((1800, 1800), cama_outv, dtype='float32')
np_write[4*60:26*60,3*60:28*60] = np_max

if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

out_file = os.path.join(out_dir, pick_val + '_' + calc_dir + '.bin')
write_binary(np_write, out_file)

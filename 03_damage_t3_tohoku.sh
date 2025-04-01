#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l mem=100gb

cd /data37/li.xiaoyang/to_xiaoyang/estimate_damage/damage_lev

mesh_path="/data37/li.xiaoyang/region_mesh/mesh"
popu_path="/data29/y-miura/Land_data/region_mesh/No1"
popu_case="tblT000876Q" ; pick_num="T000876026"
out_range="139,142,38,42" ; cama_res="1sec" ; out_name="household_average_tohoku1_t3"

#python3 area_average_val_t2.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

in_val=$out_name".csv" ; flood_path="../flood_lev"
#in_val=$out_name".csv" ; flood_path="../flood"

#calc_case="ori_w040_tohoku,ori_w020_tohoku,ori_c000_tohoku,ori_e020_tohoku,ori_e040_tohoku,ori_era5_tohoku,lev_w040_tohoku,lev_w020_tohoku,lev_c000_tohoku,lev_e020_tohoku,lev_e040_tohoku,lev_era5_tohoku" ; out_dir="./damage_lev"

#calc_case="lev_c000_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_c000_tohokul4,lev_e002_tohokul4,lev_e004_tohokul4,lev_e006_tohokul4,lev_e008_tohokul4,lev_e010_tohokul4,lev_e012_tohokul4,lev_e014_tohokul4,lev_e016_tohokul4,lev_e018_tohokul4,lev_e020_tohokul4,lev_e022_tohokul4,lev_e024_tohokul4,lev_e026_tohokul4,lev_e028_tohokul4,lev_e030_tohokul4,lev_e032_tohokul4,lev_e034_tohokul4,lev_e036_tohokul4,lev_e038_tohokul4,lev_e040_tohokul4,lev_e042_tohokul4,lev_e044_tohokul4,lev_e046_tohokul4,lev_e048_tohokul4,lev_e050_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_e032_tohokul4,lev_e034_tohokul4,lev_e036_tohokul4,lev_e038_tohokul4,lev_e040_tohokul4,lev_e042_tohokul4,lev_e044_tohokul4,lev_e046_tohokul4,lev_e048_tohokul4,lev_e050_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_c000_tohokul4,lev_e002_tohokul4,lev_e004_tohokul4,lev_e006_tohokul4,lev_e008_tohokul4,lev_e010_tohokul4,lev_e012_tohokul4,lev_e014_tohokul4,lev_e016_tohokul4,lev_e018_tohokul4,lev_e020_tohokul4,lev_e022_tohokul4,lev_e024_tohokul4,lev_e026_tohokul4,lev_e028_tohokul4,lev_e030_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_w002_tohokul4,lev_w004_tohokul4,lev_w006_tohokul4,lev_w008_tohokul4,lev_w010_tohokul4,lev_w012_tohokul4,lev_w014_tohokul4,lev_w016_tohokul4,lev_w018_tohokul4,lev_w020_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_w002_tohokul4,lev_w004_tohokul4,lev_w006_tohokul4,lev_w008_tohokul4,lev_w010_tohokul4,lev_w012_tohokul4,lev_w014_tohokul4,lev_w016_tohokul4,lev_w018_tohokul4,lev_w020_tohokul4,lev_w022_tohokul4,lev_w024_tohokul4,lev_w026_tohokul4,lev_w028_tohokul4,lev_w030_tohokul4,lev_w032_tohokul4,lev_w034_tohokul4,lev_w036_tohokul4,lev_w038_tohokul4,lev_w040_tohokul4,lev_w042_tohokul4,lev_w044_tohokul4,lev_w046_tohokul4,lev_w048_tohokul4,lev_w050_tohokul4" ; out_dir="./damage_lev"

calc_case="lev_e008_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_w022_tohokul4,lev_w024_tohokul4,lev_w026_tohokul4,lev_w028_tohokul4,lev_w030_tohokul4,lev_w032_tohokul4,lev_w034_tohokul4,lev_w036_tohokul4,lev_w038_tohokul4,lev_w040_tohokul4,lev_w042_tohokul4,lev_w044_tohokul4,lev_w046_tohokul4,lev_w048_tohokul4,lev_w050_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_w052_tohokul4,lev_w054_tohokul4,lev_w056_tohokul4,lev_w058_tohokul4,lev_w060_tohokul4,lev_w062_tohokul4,lev_w064_tohokul4,lev_w066_tohokul4,lev_w068_tohokul4,lev_w070_tohokul4,lev_w072_tohokul4,lev_w074_tohokul4,lev_w076_tohokul4,lev_w078_tohokul4,lev_w080_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_w082_tohokul4,lev_w084_tohokul4,lev_w086_tohokul4,lev_w088_tohokul4,lev_w090_tohokul4,lev_w092_tohokul4,lev_w094_tohokul4,lev_w096_tohokul4,lev_w098_tohokul4,lev_w100_tohokul4,lev_w102_tohokul4,lev_w104_tohokul4,lev_w106_tohokul4,lev_w108_tohokul4,lev_w110_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_w096_tohokul4,lev_w098_tohokul4,lev_w100_tohokul4,lev_w102_tohokul4,lev_w104_tohokul4,lev_w106_tohokul4,lev_w108_tohokul4,lev_w110_tohokul4" ; out_dir="./damage_lev"

#calc_case="lev_w020_tohokul4,lev_w040_tohokul4,lev_e020_tohokul4,lev_e040_tohokul4,lev_c000_tohokul4" ; out_dir="./damage_lev"

#calc_case="out4_lev_w020_tohokul4,out4_lev_w040_tohokul4,out4_lev_e020_tohokul4,out4_lev_e040_tohokul4,out4_lev_c000_tohokul4" ; out_dir="./damage_lev" 

python3 estimate_damage_lev_t6_tohoku.py $cama_res $in_val $pick_num $flood_path $calc_case $out_dir $out_range

#python3 draw_area_t1.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

#mpiexec -n <number_of_processes> sh myscript.sh

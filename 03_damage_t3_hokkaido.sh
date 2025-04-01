#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l mem=100gb

cd /data37/li.xiaoyang/to_xiaoyang/estimate_damage/damage_lev

mesh_path="/data37/li.xiaoyang/region_mesh/mesh"
popu_path="/data29/y-miura/Land_data/region_mesh/No1"
popu_case="tblT000876Q" ; pick_num="T000876026"
out_range="139,146,42,46" ; cama_res="1sec" ; out_name="household_average_hokkaido1_t3"

#python3 area_average_val_t2.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

in_val=$out_name".csv" ; flood_path="../flood_lev"
#in_val=$out_name".csv" ; flood_path="../flood"

#calc_case="lev_e032_hokkaidol4,lev_e034_hokkaidol4,lev_e036_hokkaidol4,lev_e038_hokkaidol4,lev_e040_hokkaidol4,lev_e042_hokkaidol4,lev_e044_hokkaidol4,lev_e046_hokkaidol4,lev_e048_hokkaidol4,lev_e050_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_e012_hokkaidol4,lev_e014_hokkaidol4,lev_e016_hokkaidol4,lev_e018_hokkaidol4,lev_e020_hokkaidol4,lev_e022_hokkaidol4,lev_e024_hokkaidol4,lev_e026_hokkaidol4,lev_e028_hokkaidol4,lev_e030_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_w002_hokkaidol4,lev_w004_hokkaidol4,lev_w006_hokkaidol4,lev_w008_hokkaidol4,lev_w010_hokkaidol4,lev_c000_hokkaidol4,lev_e002_hokkaidol4,lev_e004_hokkaidol4,lev_e006_hokkaidol4,lev_e008_hokkaidol4,lev_e010_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_e006_hokkaidol4,lev_e008_hokkaidol4,lev_e010_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_w012_hokkaidol4,lev_w014_hokkaidol4,lev_w016_hokkaidol4,lev_w018_hokkaidol4,lev_w020_hokkaidol4,lev_w022_hokkaidol4,lev_w024_hokkaidol4,lev_w026_hokkaidol4,lev_w028_hokkaidol4,lev_w030_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_w032_hokkaidol4,lev_w034_hokkaidol4,lev_w036_hokkaidol4,lev_w038_hokkaidol4,lev_w040_hokkaidol4,lev_w042_hokkaidol4,lev_w044_hokkaidol4,lev_w046_hokkaidol4,lev_w048_hokkaidol4,lev_w050_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_w052_hokkaidol4,lev_w054_hokkaidol4,lev_w056_hokkaidol4,lev_w058_hokkaidol4,lev_w060_hokkaidol4,lev_w062_hokkaidol4,lev_w064_hokkaidol4,lev_w066_hokkaidol4,lev_w068_hokkaidol4,lev_w070_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_w072_hokkaidol4,lev_w074_hokkaidol4,lev_w076_hokkaidol4,lev_w078_hokkaidol4,lev_w080_hokkaidol4,lev_w082_hokkaidol4,lev_w084_hokkaidol4,lev_w086_hokkaidol4,lev_w088_hokkaidol4,lev_w090_hokkaidol4" ; out_dir="./damage_lev"

calc_case="lev_e050_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_w092_hokkaidol4,lev_w094_hokkaidol4,lev_w096_hokkaidol4,lev_w098_hokkaidol4,lev_w100_hokkaidol4,lev_w102_hokkaidol4,lev_w104_hokkaidol4,lev_w106_hokkaidol4,lev_w108_hokkaidol4,lev_w110_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="lev_w020_hokkaidol4,lev_w040_hokkaidol4,lev_c000_hokkaidol4,lev_e020_hokkaidol4,lev_e040_hokkaidol4" ; out_dir="./damage_lev"

#calc_case="out4_w020_hokkaido,out4_w040_hokkaido,out4_c000_hokkaido,out4_e020_hokkaido,out4_e040_hokkaido" ; out_dir="./damage_lev"

python3 estimate_damage_lev_t6_hokkaido.py $cama_res $in_val $pick_num $flood_path $calc_case $out_dir $out_range

#python3 draw_area_t1.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

#mpiexec -n <number_of_processes> sh myscript.sh

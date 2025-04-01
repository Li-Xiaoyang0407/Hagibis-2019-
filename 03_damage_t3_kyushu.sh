#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l mem=100gb

cd /data37/li.xiaoyang/to_xiaoyang/estimate_damage/damage_lev

mesh_path="/data37/li.xiaoyang/region_mesh/mesh"
popu_path="/data29/y-miura/Land_data/region_mesh/No1"
popu_case="tblT000876Q" ; pick_num="T000876026"
out_range="129,132,31,35" ; cama_res="1sec" ; out_name="household_average_kyushu1_t4"

#python3 area_average_val_t2.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

in_val=$out_name".csv" ; flood_path="../flood_lev"
#in_val=$out_name".csv" ; flood_path="../flood"

#calc_case="lev_e032_kyushul5,lev_e034_kyushul5,lev_e036_kyushul5,lev_e038_kyushul5,lev_e040_kyushul5,lev_e042_kyushul5,lev_e044_kyushul5,lev_e046_kyushul5,lev_e048_kyushul5,lev_e050_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_c000_kyushul5,lev_e002_kyushul5,lev_e004_kyushul5,lev_e006_kyushul5,lev_e008_kyushul5,lev_e010_kyushul5,lev_e012_kyushul5,lev_e014_kyushul5,lev_e016_kyushul5,lev_e018_kyushul5,lev_e020_kyushul5,lev_e022_kyushul5,lev_e024_kyushul5,lev_e026_kyushul5,lev_e028_kyushul5,lev_e030_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_w002_kyushul5,lev_w004_kyushul5,lev_w006_kyushul5,lev_w008_kyushul5,lev_w010_kyushul5,lev_w012_kyushul5,lev_w014_kyushul5,lev_w016_kyushul5,lev_w018_kyushul5,lev_w020_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_w022_kyushul5,lev_w024_kyushul5,lev_w026_kyushul5,lev_w028_kyushul5,lev_w030_kyushul5,lev_w032_kyushul5,lev_w034_kyushul5,lev_w036_kyushul5,lev_w038_kyushul5,lev_w040_kyushul5,lev_w042_kyushul5,lev_w044_kyushul5,lev_w046_kyushul5,lev_w048_kyushul5,lev_w050_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_w052_kyushul5,lev_w054_kyushul5,lev_w056_kyushul5,lev_w058_kyushul5,lev_w060_kyushul5,lev_w062_kyushul5,lev_w064_kyushul5,lev_w066_kyushul5,lev_w068_kyushul5,lev_w070_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_w072_kyushul5,lev_w074_kyushul5,lev_w076_kyushul5,lev_w078_kyushul5,lev_w080_kyushul5,lev_w082_kyushul5,lev_w084_kyushul5,lev_w086_kyushul5,lev_w088_kyushul5,lev_w090_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_w020_kyushul4,lev_w040_kyushul4,lev_e020_kyushul4,lev_e040_kyushul4,lev_c000_kyushul4" ; out_dir="./damage_lev"

#calc_case="out4_lev_w020_kyushul5,out4_lev_w040_kyushul5,out4_lev_e020_kyushul5,out4_lev_e040_kyushul5,out4_lev_c000_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_w020_kyushul5,lev_w040_kyushul5,lev_e020_kyushul5,lev_e040_kyushul5,lev_c000_kyushul5" ; out_dir="./damage_lev"
calc_case="lev_e040_kyushul5" ; out_dir="./damage_lev"

#calc_case="lev_w092_kyushul5,lev_w094_kyushul5,lev_w096_kyushul5,lev_w098_kyushul5,lev_w100_kyushul5,lev_w102_kyushul5,lev_w104_kyushul5,lev_w106_kyushul5,lev_w108_kyushul5,lev_w110_kyushul5" ; out_dir="./damage_lev"

#calc_case="ori_c000_zero_kanto,lev_c000_zero_kanto" ; out_dir="./damage_lev" 

python3 estimate_damage_lev_t6_kyushu.py $cama_res $in_val $pick_num $flood_path $calc_case $out_dir $out_range

#python3 draw_area_t1.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

#mpiexec -n <number_of_processes> sh myscript.sh

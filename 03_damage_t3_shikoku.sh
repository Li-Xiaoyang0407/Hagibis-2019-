#!/bin/sh
#PBS -l nodes=1:ppn=2
#PBS -l mem=100gb

cd /data37/li.xiaoyang/to_xiaoyang/estimate_damage/damage_lev

mesh_path="/data37/li.xiaoyang/region_mesh/mesh"
popu_path="/data29/y-miura/Land_data/region_mesh/No1"
popu_case="tblT000876Q" ; pick_num="T000876026"
out_range="132,136,32,36" ; cama_res="1sec" ; out_name="household_average_shikoku1_t3"

#python3 area_average_val_t2.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

in_val=$out_name".csv" ; flood_path="../flood_lev"
#in_val=$out_name".csv" ; flood_path="../flood"

#calc_case="lev_e032_shikokul4,lev_e034_shikokul4,lev_e036_shikokul4,lev_e038_shikokul4,lev_e040_shikokul4,lev_e042_shikokul4,lev_e044_shikokul4,lev_e046_shikokul4,lev_e048_shikokul4,lev_e050_shikokul4" ; out_dir="./damage_lev"

calc_case="lev_e050_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_e012_shikokul4,lev_e014_shikokul4,lev_e016_shikokul4,lev_e018_shikokul4,lev_e020_shikokul4,lev_e022_shikokul4,lev_e024_shikokul4,lev_e026_shikokul4,lev_e028_shikokul4,lev_e030_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_w002_shikokul4,lev_w004_shikokul4,lev_w006_shikokul4,lev_w008_shikokul4,lev_w010_shikokul4,lev_c000_shikokul4,lev_e002_shikokul4,lev_e004_shikokul4,lev_e006_shikokul4,lev_e008_shikokul4,lev_e010_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_w012_shikokul4,lev_w014_shikokul4,lev_w016_shikokul4,lev_w018_shikokul4,lev_w020_shikokul4,lev_w022_shikokul4,lev_w024_shikokul4,lev_w026_shikokul4,lev_w028_shikokul4,lev_w030_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_w032_shikokul4,lev_w034_shikokul4,lev_w036_shikokul4,lev_w038_shikokul4,lev_w040_shikokul4,lev_w042_shikokul4,lev_w044_shikokul4,lev_w046_shikokul4,lev_w048_shikokul4,lev_w050_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_w052_shikokul4,lev_w054_shikokul4,lev_w056_shikokul4,lev_w058_shikokul4,lev_w060_shikokul4,lev_w062_shikokul4,lev_w064_shikokul4,lev_w066_shikokul4,lev_w068_shikokul4,lev_w070_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_w072_shikokul4,lev_w074_shikokul4,lev_w076_shikokul4,lev_w078_shikokul4,lev_w080_shikokul4,lev_w082_shikokul4,lev_w084_shikokul4,lev_w086_shikokul4,lev_w088_shikokul4,lev_w090_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_w092_shikokul4,lev_w094_shikokul4,lev_w096_shikokul4,lev_w098_shikokul4,lev_w100_shikokul4,lev_w102_shikokul4,lev_w104_shikokul4,lev_w106_shikokul4,lev_w108_shikokul4,lev_w110_shikokul4" ; out_dir="./damage_lev"

#calc_case="lev_w020_shikokul4,lev_w040_shikokul4,lev_e020_shikokul4,lev_e040_shikokul4,lev_c000_shikokul4" ; out_dir="./damage_lev"
#calc_case="out4_w020_shikoku,out4_w040_shikoku,out4_e020_shikoku,out4_e040_shikoku,out4_c000_shikoku" ; out_dir="./damage_lev"

python3 estimate_damage_lev_t6_shikoku.py $cama_res $in_val $pick_num $flood_path $calc_case $out_dir $out_range

#python3 draw_area_t1.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

#mpiexec -n <number_of_processes> sh myscript.sh

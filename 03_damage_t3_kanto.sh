#!/bin/sh
#PBS -l nodes=1:ppn=2
#PBS -l mem=100gb

cd /data37/li.xiaoyang/to_xiaoyang/estimate_damage/damage_lev

mesh_path="/data37/li.xiaoyang/region_mesh/mesh"
popu_path="/data29/y-miura/Land_data/region_mesh/No1"
popu_case="tblT000876Q" ; pick_num="T000876026"
out_range="136,141,34,38" ; cama_res="1sec" ; out_name="household_average_kanto1_t3"

#python3 area_average_val_t2_kanto.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

in_val=$out_name".csv" ; flood_path="../flood_lev"
#in_val=$out_name".csv" ; flood_path="../flood"

#calc_case="lev_e032_kantol4,lev_e034_kantol4,lev_e036_kantol4,lev_e038_kantol4,lev_e040_kantol4,lev_e042_kantol4,lev_e044_kantol4,lev_e046_kantol4,lev_e048_kantol4,lev_e050_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_e012_kantol4,lev_e014_kantol4,lev_e016_kantol4,lev_e018_kantol4,lev_e020_kantol4,lev_e022_kantol4,lev_e024_kantol4,lev_e026_kantol4,lev_e028_kantol4,lev_e030_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_w002_kantol4,lev_w004_kantol4,lev_w006_kantol4,lev_w008_kantol4,lev_w010_kantol4,lev_c000_kantol4,lev_e002_kantol4,lev_e004_kantol4,lev_e006_kantol4,lev_e008_kantol4,lev_e010_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_w012_kantol4,lev_w014_kantol4,lev_w016_kantol4,lev_w018_kantol4,lev_w020_kantol4,lev_w022_kantol4,lev_w024_kantol4,lev_w026_kantol4,lev_w028_kantol4,lev_w030_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_w032_kantol4,lev_w034_kantol4,lev_w036_kantol4,lev_w038_kantol4,lev_w040_kantol4,lev_w042_kantol4,lev_w044_kantol4,lev_w046_kantol4,lev_w048_kantol4,lev_w050_kantol4" ; out_dir="./damage_lev"

calc_case="lev_e050_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_w052_kantol4,lev_w054_kantol4,lev_w056_kantol4,lev_w058_kantol4,lev_w060_kantol4,lev_w062_kantol4,lev_w064_kantol4,lev_w066_kantol4,lev_w068_kantol4,lev_w070_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_w072_kantol4,lev_w074_kantol4,lev_w076_kantol4,lev_w078_kantol4,lev_w080_kantol4,lev_w082_kantol4,lev_w084_kantol4,lev_w086_kantol4,lev_w088_kantol4,lev_w090_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_w092_kantol4,lev_w094_kantol4,lev_w096_kantol4,lev_w098_kantol4,lev_w100_kantol4,lev_w102_kantol4,lev_w104_kantol4,lev_w106_kantol4,lev_w108_kantol4,lev_w110_kantol4" ; out_dir="./damage_lev"    

#calc_case="lev_w020_kantol4,lev_w040_kantol4,lev_e020_kantol4,lev_e040_kantol4,lev_c000_kantol4" ; out_dir="./damage_lev"

#calc_case="lev_w040_kantol4,lev_e020_kantol4,lev_c000_kantol4" ; out_dir="./damage_lev" 

#calc_case="out4_w020_kanto,out4_w040_kanto,out4_e020_kanto,out4_e040_kanto,out4_c000_kanto" ; out_dir="./damage_lev" 

python3 estimate_damage_lev_t6_kanto.py $cama_res $in_val $pick_num $flood_path $calc_case $out_dir $out_range

#python3 draw_kanto_damage_dif.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name
#python3 draw_kanto_dph_dif1.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

#mpiexec -n <number_of_processes> sh myscript.sh

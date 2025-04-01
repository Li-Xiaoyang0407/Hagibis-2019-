#!/bin/sh
#PBS -l nodes=1:ppn=24

mesh_path="/data37/li.xiaoyang/region_mesh/mesh"
popu_path="/data29/y-miura/Land_data/region_mesh/No1"
popu_case="tblT000876Q" ; pick_num="T000876026"
#out_range="129,132,31,34" ; cama_res="1sec" ; out_name="household_average_kyushu"
out_range="129,132,31,35" ; cama_res="1sec" ; out_name="household_average_kyushu1_t4"

python3 /data37/li.xiaoyang/to_xiaoyang/estimate_damage/area_average_val.py $mesh_path $popu_path $popu_case $pick_num $out_range $cama_res $out_name

in_val=$out_name".csv" ; flood_path="./flood"
calc_case="out_w040,out_e040" ; out_dir="./damage"

#python3 estimate_damage.py $cama_res $in_val $pick_num $flood_path $calc_case $out_dir $out_range



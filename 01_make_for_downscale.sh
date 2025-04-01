#!/bin/sh

ils_path="../runs" ; calc_date="2019/10/1" ; pick_date="2019/10/12-2019/10/15"
calc_dir="out4_e020 out4_e040" ; pick_val="flddph" ; unit_conv="1"
ils_outv="-999.0" ; out_dir="./convert" ; base_dir=""

if [ -n "$base_dir" ]; then
  for calc in $calc_dir ; do
    python3 ils_cdf2bin_little.py $ils_path $calc_date $pick_date $calc $pick_val $unit_conv $ils_outv $out_dir $base_dir
  done
else
  for calc in $calc_dir ; do
    python3 ils_cdf2bin_little.py $ils_path $calc_date $pick_date $calc $pick_val $unit_conv $ils_outv $out_dir
  done
fi

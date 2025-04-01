#!/bin/sh

mkdir flood
mkdir fig

calc_case="out4_w040 out4_w020 out4_c000 out4_e020 out4_e040 out4_c000_zero" conv_dir="./convert"

for calc in $calc_case ; do
  ./s01-downscale_flddph_chikuma.sh $calc $conv_dir
done

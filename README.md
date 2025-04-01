And this is for the explanation:
The tools to produce the amount of damage should be implemented in the following order in /data37/li.xiaoyang/to_xiaoyang/estimate_damage/.

(1) Run 01_make_for_downscale.sh
This tool performs the processing necessary to implement downscaling; because the range of the ils calculation differs from the range of the CaMa-Flood elevation data, and because the maximum inundation depth is calculated.
This also allows for numerous calculations to be performed at once by specifying the calculation case in the variable $calc_dir, separated by spaces.
In addition, there are cases where the CaMa-Flood calculation always seems to have water on the ground surface.
If you want to remove this, specify the directory of the result of that calculation in the variable $base_dir in 01_make_for_downscale.sh.
I ran a calculation with zero precipitation in Hgibis and used that for $base_dir.

The calculation results are stored in a directory named $out_dir in 01_make_for_downscale.sh

(2) Run 02_make_downscale_flddpt.sh
This is a tool to downscale many ils calculation results in the same region. In fact, s01-downscale_flddph_chikuma.sh(revised CaMa tool) is running.
If you want to calculate in a different region, please change the values of WEST, EAST, SOUTH, and NORTH in s01-downscale_flddph_chikuma.sh. You must enter integer latitude and longitude coordinates for each.

The calculation results are stored in a directory named [fig,flood]

(3) Run 03_make_damage_estimate.sh
This is a tool to estimate flood damage. In fact, the amount of damage is calculated in estimate_damage.py.
The damage amount is only for three items, a home and housewares, and their total.
This also allows for numerous calculations to be performed at once by specifying the calculation case in the variable $calc_case, separated by spaces.
Before that, area_average_val.py interpolates the number of households from the Japanese census into CaMa-Flood's high-resolution grid. This value is used to produce the amount of damage.

The calculation results are stored in a directory named $out_dir in 03_make_damage_estimate.sh

#!/bin/sh

## CaMa-Flood: simulation map directory & simulation output dorectory
## Below is the example to downscale the result of sample simulation "test1"
MAPDIR="/data29/y-miura/tej/CaMa-Flood_v4/map/"
OUTDIR=$2

## downscale project tag
TAG="tej"

## specify tartget downscale domain 

#tohoku
#WEST=139
#EAST=142
#SOUTH=38
#NORTH=42

#shikoku
#WEST=132
#EAST=136
#SOUTH=32
#NORTH=36

#kanto
#WEST=136
#EAST=141
#SOUTH=34
#NORTH=38

#hokkaido
#WEST=139
#EAST=146
#SOUTH=42
#NORTH=46

#kyushu
WEST=129
EAST=132
SOUTH=31
NORTH=35

#WEST=129
#EAST=146
#SOUTH=31
#NORTH=46



## specity downscale period
#SYEAR=2019
#SMON=10
#EYEAR=2019
#EMON=10

CASE=$1

## specify downscale resolution (high resolution file directory should exist in the used map directory)
RES=1sec
#RES=30sec
#RES=15sec
#RES=5sec

## For visualization:  NGRID=pixels to aggregate,  MAXDPH:maximum water depth for colorbar
NGRID=1
MAXDPH=10.0

##########

rm -f map
rm -f out
ln -sf $MAPDIR map
ln -sf $OUTDIR out

##########

## downscale target domain using fortran code
#./t01-downscale.sh   $WEST $EAST $SOUTH $NORTH $SYEAR $SMON $EYEAR $EMON $RES
./t01-downscale.sh   $WEST $EAST $SOUTH $NORTH $CASE $RES

## visualization using PyThon
#./t02-draw_flddph.sh $WEST $EAST $SOUTH $NORTH $SYEAR $SMON $EYEAR $EMON $RES $NGRID $MAXDPH
./t02-draw_flddph.sh $WEST $EAST $SOUTH $NORTH $CASE $RES $NGRID $MAXDPH

##########

#rm -rf flood_${TAG}
#rm -rf fig_${TAG}
#mv     flood       flood_${TAG}
#mv     fig         fig_${TAG}

#!/bin/sh

USER=`whoami`

WEST=$1
EAST=$2
SOUTH=$3
NORTH=$4

#SYEAR=$5
#SMON=$6
#EYEAR=$7
#EMON=$8

CASE=$5

#RES=$9
RES=$6

#SDATE=$(( $SYEAR * 10000 + $SMON * 100 + 1 ))
#EDATE=$(( $EYEAR * 10000 + $EMON * 100 + 31 ))

#rm -rf flood
#mkdir -p flood

FLDDPH="./out/flddph_$CASE.bin"      # input:  original flood depth file
FFLOOD="./flood/flood_$CASE.bin"     # output: downscaled flood depth file
IREC=1

./src/downscale_flddph $WEST $EAST $SOUTH $NORTH $RES $FLDDPH $FFLOOD $IREC &

wait

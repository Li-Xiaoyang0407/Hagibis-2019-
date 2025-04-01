#!/bin/bash

#USER=`whoami`

WEST=$1
EAST=$2
SOUTH=$3
NORTH=$4

#SYEAR=$5
#SMON=$6
#EYEAR=$7
#EMON=$8

CDATE=$5

#RES=$9
#NGRID=${10}
#MAXDPH=${11}

RES=$6
NGRID=$7
MAXDPH=$8

#SDATE=$(( $SYEAR * 10000 + $SMON * 100 + 1 ))
#EDATE=$(( $EYEAR * 10000 + $EMON * 100 + 31 ))
#CDATE=$(( $SYEAR * 10000 + $SMON * 100 + 0 ))

#rm -rf fig
#mkdir -p fig

#rm -f slp.bin
./src/conv_slp $WEST $EAST $SOUTH $NORTH $RES $NGRID    ## convert high-resolution slope file for PyThon figure.

./u02-flddph.sh $WEST $EAST $SOUTH $NORTH $CDATE $NGRID $MAXDPH $RES    ##  draw figure

wait
#rm ./slp.bin

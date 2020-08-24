#!/bin/bash

#DIR=${HOME}/data/head_seas_000

if [ "$#" -ne 1 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 DIRECTORY" >&2
  exit 1
fi

DIR=$1

#shopt -s nullglob
echo "Looking in $DIR"
#for f in "${DIR}/*.bag"
for f in ${DIR}/*.bag
do
    echo "Processing <${f}>"
    ./bag2p_modelstates.py $f

done
	 

#for FILE in ${HOME}/*.*; do echo "$FILE"; done

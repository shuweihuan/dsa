#!/usr/bin/bash

source ../conf/global.conf

################################
######### Environment ##########
################################

mkdir -p "$DATA_PATH"

################################
########### Get Data ###########
################################

cd $SRC_PATH/spider
python download_new_data.py
cd - > /dev/null


#!/usr/bin/bash

source ../conf/global.conf

################################
######### Environment ##########
################################

if [ -z $DATA_PATH ]; then
	mkdir $DATA_PATH
fi

################################
########### Get Data ###########
################################

cd $SRC_PATH/spider
python download_history_data.py
cd - > /dev/null


#!/usr/bin/sh

source ../conf/global.conf

function help {
    echo "  spider: ./$0 spider [--history|--new]"
    echo "  train: ./$0 train [--tiny|--full]"
    echo "  predict: ./$0 predict [--tiny|--full]"
    echo "  help: ./$0 help|-h|--help"
    exit 0
}

while true; do
	cmd=$1
	if [[ "$cmd" == "" ]]; then
		cmd="--help"
	fi
	case "$cmd" in
		spider) # spider
			spider_opt=$2
			case "$spider_opt" in
				--history) # download history data
					echo ">>> spider: download history data"
					exit 0
					;;
				--new) # download new data
					echo ">>> spider: download new data"
					exit 0
					;;
				*) # others
					echo "invalid spider options"
					exit 1
					;;
			esac
			;;
		train) # train
			train_opt=$2
			case "$train_opt" in
				--tiny) # train tiny data
					echo ">>> train: train tiny data"
					exit 0
					;;
				--full) # train full data
					echo ">>> train: train full data"
					exit 0
					;;
				*) # others
					echo "invalid train options"
					exit 1
					;;
			esac
			;;
		predict) # predict
			predict_opt=$2
			case "$predict_opt" in
				--tiny) # predict tiny data
					echo ">>> predict: predict tiny data"
					exit 0
					;;
				--full) # predict full data
					echo ">>> predict: predict full data"
					exit 0
					;;
				*) # others
					echo "invalid predict options"
					exit 1
					;;
			esac
			;;
		help|-h|--help) # help
		    help
			exit 0
			;;
		*) # others
			echo "invalid command"
			exit 1
			;;
	esac
done


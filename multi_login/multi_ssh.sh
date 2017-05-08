#!/bin/sh

if [ "$1" == "" ]
then
	echo "command missing"
	exit 0
fi
if [ "$2" == "" ]
then
	echo "file missing"
	exit 0
fi

HOST1[0]=${host1}

HOST2[0]=${host2}
HOST2[1]=${host3}
HOST2[2]=${host4}

DIR1=/home/soft/resty/nginx/logs
DIR2=/home/work/nginx/logs

index=1
CMD_ARGS=
ARGS_COUNT=$#
for i in "$@"
do
	if [ $index -lt $ARGS_COUNT ]
	then
		a=${i:0:1}
		if [ "$a" == "-" ]
		then
			CMD_ARGS="$CMD_ARGS $i"
		else
			CMD_ARGS="$CMD_ARGS '$i'"
		fi
	else
		FILE=$i
	fi
	index=`expr $index + 1`
done

if [[ $FILE =~ _[0-9]{8}\.log$ ]]
then
#	DIR2=/home/work/nginx/logs/archived
	DIR2=/home/disk2/logs
fi

for i in ${HOST1[@]}
do
	ssh work@$i $CMD_ARGS $DIR1/$FILE
done
for i in ${HOST2[@]}
do
	ssh work@$i $CMD_ARGS $DIR2/$FILE
done

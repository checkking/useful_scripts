#########################################################################
# File Name: mysqlSync.sh
# Author: checkking
# mail: ${Author}@foxmail.com
# Created Time: 2017-03-01 12:39:21
#########################################################################
#!/bin/bash

today=`date +%Y%m%d`

if [ $# -gt 0 ]; then
   for table in $*
   do
       mysqldump -${remoteHost} -P${remotePort} -u${remoteUser} -p${remotePsswd} --default-character-set=utf8 ${db} ${table} >${db}.${table}.${today}.sql
       mysql -h127.0.0.1 -uroot  -P6336 -P6336 ${db}<${db}.${table}.${today}.sql
   done
else
    mysqldump -${remoteHost} -P${remotePort} -u${remoteUser} -p${remotePsswd} --default-character-set=utf8 ${db} >${db}.${today}.sql
    mysql -h127.0.0.1 -uroot  -P6336 -P6336 ${db}<${db}.${today}.sql
fi

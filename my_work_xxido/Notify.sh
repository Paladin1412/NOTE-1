#!/bin/sh
. /home/qspace/bin/.bash_env


if [[ $# < 4 ]];then
    echo "usage: notify.sh 'type(rtx|sms|mm|bizmp|mail)' 'rtxname1;rtxnam2..' 'title'  'content'"
    exit 0
fi

sendtype=$1
rcptname=$2
title=$3
content=$4

ossdb="/home/qspace/bin/ossdb"

if [[ $sendtype == "rtx" ]]
then
    $ossdb notify "insert into notify (type,rcpt,title,content,add_time,\`from\`) values ('1', '$rcptname', '$title', '$content', NOW(), 'notify.sh')"
    
elif [[ $sendtype == "sms" ]]
then
    mobileNum=''
    for name in `echo $rcptname | sed 's/\;/ /g'`
    do
        num=`$ossdb dept_db "select MobilePhoneNumber from staff where EnglishName='$name'" | tail -n 1`
        if [[ -n $num ]]
        then
            mobileNum=${mobileNum}${num}';'
        fi
    done
    if [[ -n $mobileNum ]]
    then
        $ossdb notify "insert into notify (type,rcpt,title,content,add_time,\`from\`) values ('0', '$mobileNum', '$title', '$content', NOW(), 'notify.sh')"
    fi

elif [[ $sendtype == "mm" ]]
then
    $ossdb notify "insert into notify (type,rcpt,title,content,add_time,\`from\`) values ('3', '$rcptname', '$title', '$content', NOW(), 'notify.sh')"
elif [[ $sendtype == "bizmp" ]]
then
    $ossdb notify "insert into notify (type,rcpt,title,content,add_time,\`from\`) values ('4', '$rcptname', '$title', '$content', NOW(), 'notify.sh')"
elif [[ $sendtype == "mail" ]]
then
    $ossdb notify "insert into notify (type,rcpt,title,content,add_time,\`from\`) values ('2', '$rcptname', '$title', '$content', NOW(), 'notify.sh')"
else
    echo "usage: notify.sh 'type(rtx|sms|mm|bizmp)' 'rtxname1;rtxnam2..' 'title'  'content'"
fi
exit 0

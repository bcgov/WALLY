PROJECT_NAME=$1

databasePodName=`oc get pods -n $PROJECT_NAME | grep wally-psql | awk 'NR==1{print $1}'`

databaseDiskUsagePercent=`oc exec $databasePodName -c postgresql -n $PROJECT_NAME -- df -k | grep "/home/postgres/pgdata" | awk '{print $5}'`
databaseDiskUsage=${databaseDiskUsagePercent%?}
if [ ${databaseDiskUsage} -gt 70 ]; then
        diskusageAlarm=true
fi
if [ ${diskusageAlarm} = true ]; then
        echo "CRITICAL - [$1] Postgresql diskusage at $databaseDiskUsagePercent "
        exit 2
fi
echo "OK - [$1] Postgresql diskusage under limit"
exit 0

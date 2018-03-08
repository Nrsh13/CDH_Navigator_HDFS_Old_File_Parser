## Setup Different Paths
OWNPATH=`cd $(dirname $0);pwd;cd - >/dev/null 2>/dev/null`
ROOT_DIR=$(dirname $OWNPATH)
SRCPATH=$ROOT_DIR/src
LOGPATH=$ROOT_DIR/logs
jobpid_path=$ROOT_DIR/pids
jobrunner=`basename $0`
jobpidfile=$jobpid_path/$jobrunner.pid

## Print the Usage
usage="This Program will read the $ROOT_DIR/conf/properties.yml, 
get the required details, use these details to find all
files which were never accessed in last N days and store the results in Hive Table.

Usage:
sh $ROOT_DIR/bin/$(basename "$0") [-h]

where:
    -h  show this help text

Example:
	sh $ROOT_DIR/bin/$(basename "$0")
"


seed=42

## Display --help
while getopts ':h' option; do
  case "$option" in
    h) echo -e "\n$usage"
       exit
       ;;
  esac
done
shift $((OPTIND - 1))


####################################################
#                 M A I N - P A R T                #
####################################################

echo -e " PROJECT: \t Navigator Files Parser \n AUTHOR: \t Naresh Jangra \n CREATED: \t 15th Feb, 2018 \n PURPOSE: \t Get the Files which were Never accessed in last N Days"

## Already Running job Check
if [ -e $jobpidfile ]
then
   echo -e "\nWARNING: Same job instance can not be started !! Exiting !!"
   echo -e "\nIf this is NOT the case, remove $jobpidfile and try again !!\n" 
   exit 0
fi

## Trigger the Main Python Code
cd $SRCPATH
(spark2-submit navigator_hdfs_old_file_parser.py > /dev/null 2>&1 &)
job_status="$?"

if [ "$job_status" == "0" ]
then
    cd $ROOT_DIR
    touch $jobpidfile
    echo -e "\nJob Triggered. Check latest log file at $LOGPATH\n"
else
    cd $ROOT_DIR
    exit 127
fi

#END


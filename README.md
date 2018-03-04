# CDH_Navigator_HDFS_Old_File_Parser
Cloudera Navigator amazingly holds every possible information about your CDH Cluster. This repo uses Navigator to generate a list of Files which were never accessed in last N number of Days.

# Dependencies
CDH 5.10 or Higher
Spark 2.0 or Higher

# Prerequisites
For a Kerberized Cluster, make sure you have valid Kerberos ticket before you run this Program.

# Installation
Clone the repo:
```
export https_proxy=https://yourproxy:10568 # if any
git clone https://github.com/Nrsh13/CDH_Navigator_HDFS_Old_File_Parser.git
```

OR Download the Zip repo, Move to your Linux machine and unzip
```
[nrsh13@apache-hadoop]$ unzip CDH_Navigator_HDFS_Old_File_Parser-master.zip
Archive:  CDH_Navigator_HDFS_Old_File_Parser-master.zip
c61a5e45751de5fd47ace408f8a7e8a0ce5b7277
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/
  inflating: CDH_Navigator_HDFS_Old_File_Parser-master/README.md
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/bin/
  inflating: CDH_Navigator_HDFS_Old_File_Parser-master/bin/trigger_navigator_hdfs_old_file_parser.sh
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/conf/
  inflating: CDH_Navigator_HDFS_Old_File_Parser-master/conf/properties.yml
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/data/
 extracting: CDH_Navigator_HDFS_Old_File_Parser-master/data/myresult_0.json
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/logs/
 extracting: CDH_Navigator_HDFS_Old_File_Parser-master/logs/navigator_hdfs_old_file_parser.log
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/pids/
 extracting: CDH_Navigator_HDFS_Old_File_Parser-master/pids/trigger_navigator_hdfs_old_file_parser.sh.pid
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/src/
   creating: CDH_Navigator_HDFS_Old_File_Parser-master/src/lib/
  inflating: CDH_Navigator_HDFS_Old_File_Parser-master/src/lib/Logger.py
  inflating: CDH_Navigator_HDFS_Old_File_Parser-master/src/lib/PyUtils.py
 extracting: CDH_Navigator_HDFS_Old_File_Parser-master/src/lib/__init__.py
  inflating: CDH_Navigator_HDFS_Old_File_Parser-master/src/navigator_hdfs_old_file_parser.py
```

# Usage
```
[nrsh13@apache-hadoop]$ sh CDH_Navigator_HDFS_Old_File_Parser-master/bin/trigger_navigator_hdfs_old_file_parser.sh -h

This Program will read the /home/nrsh13/CDH_Navigator_HDFS_Old_File_Parser-master/conf/properties.yml, get the required details, use these details to find all files which were never accessed in last N days and store the results in Hive Table.

Usage:
sh /tmp/test/CDH_Navigator_HDFS_Old_File_Parser-master/bin/trigger_navigator_hdfs_old_file_parser.sh [-h]

where:
    -h  show this help text

Example:
        sh /tmp/test/CDH_Navigator_HDFS_Old_File_Parser-master/bin/trigger_navigator_hdfs_old_file_parser.sh
```

# Example
```
[nrsh13@apache-hadoop]$ sh CDH_Navigator_HDFS_Old_File_Parser-master/bin/trigger_navigator_hdfs_old_file_parser.sh
 PROJECT:        Navigator Files Parser
 AUTHOR:         Naresh Jangra
 CREATED:        15th Feb, 2018
 PURPOSE:        Get the Files which were Never accessed in last N Days

Job Triggered. Check latest log file at /tmp/test/CDH_Navigator_HDFS_Old_File_Parser-master/logs
```

# Contact
nrsh13@gmail.com

# CDH_Navigator_HDFS_Old_File_Parser
Cloudera Navigator amazingly holds every possible information about your CDH Cluster. 

This Program reads the conf/properties.yml, get the required details, use these details to find all files which were never accessed in last N days. Finally stores the results in a Hive Table.

## Dependencies
CDH 5.10 or Higher

Spark 2.0 or Higher

## Installation
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

## Prerequisites
1) For a Kerberized Cluster, make sure you have valid Kerberos ticket before you run this Program.
2) Prepare the conf/properties.yml having

      Navigator Host, Navigator Port, Username, Password, HDFS Paths to be Processed, Hive Database and Table Names, Number of Days
3) Write permissions for the user (running this Program) on Hive Database used in conf/properties.yml

## Usage
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

## Example
```
[nrsh13@apache-hadoop]$ sh CDH_Navigator_HDFS_Old_File_Parser-master/bin/trigger_navigator_hdfs_old_file_parser.sh
 PROJECT:        Navigator Files Parser
 AUTHOR:         Naresh Jangra
 CREATED:        15th Feb, 2018
 PURPOSE:        Get the Files which were Never accessed in last N Days

Job Triggered. Check latest log file at /home/nrsh13/CDH_Navigator_HDFS_Old_File_Parser-master/logs
```

## Sample logs
```
2018-03-04 22:14:56,549 NAVIGATOR-PARSER INFO  Creating the Table default.mytest if NOT EXISTS
2018-03-04 22:14:58,068 NAVIGATOR-PARSER INFO  INSERT INTO TABLE Table Command Prepared:
2018-03-04 22:14:58,068 NAVIGATOR-PARSER INFO  INSERT INTO TABLE default.mytest SELECT owner,parentPath,originalName,created,lastModified,lastAccessed,size,sourceType,permissions,group,identity FROM mytable
2018-03-04 22:14:58,069 NAVIGATOR-PARSER INFO  Inserting the Data in default.mytest Table
2018-03-04 22:14:58,838 NAVIGATOR-PARSER INFO  45 Records Inserted successfully in default.mytest
2018-03-04 22:14:58,839 NAVIGATOR-PARSER INFO  Data Processed Successfully !!
```

## Contact
nrsh13@gmail.com

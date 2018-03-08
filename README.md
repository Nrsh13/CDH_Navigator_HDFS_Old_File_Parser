# CDH_Navigator_HDFS_Old_File_Parser
Cloudera Navigator amazingly holds every possible information about your CDH Cluster. HDFS Storage utilization can continuously go high with time and can arise a need of OLD/Unused files Cleanup.

This Program reads the conf/properties.yml, get the required details, use these details to find all files which were never accessed in last N days. Finally stores the results in a Hive Table for further actions.

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

## Prerequisites
1) For a Kerberized Cluster, make sure you have valid Kerberos ticket before you run this Program.
2) Prepare the conf/properties.yml having

      Navigator Host, Navigator Port, Username, Password, HDFS Paths to be Processed, Hive Database and Table Names, Number of Days
3) Write permissions for the user (running this Program) on Hive Database used in conf/properties.yml

## Usage
```
[nrsh13@apache-hadoop]$ sh CDH_Navigator_HDFS_Old_File_Parser/bin/trigger_navigator_hdfs_old_file_parser.sh -h

This Program will read the /home/nrsh13/CDH_Navigator_HDFS_Old_File_Parser/conf/properties.yml, get the required details, use these details to find all files which were never accessed in last N days and store the results in Hive Table.

Usage:
sh /home/nrsh13/CDH_Navigator_HDFS_Old_File_Parser/bin/trigger_navigator_hdfs_old_file_parser.sh [-h]

where:
    -h  show this help text

Example:
        sh /home/nrsh13/CDH_Navigator_HDFS_Old_File_Parser/bin/trigger_navigator_hdfs_old_file_parser.sh
```

## Example
```
[nrsh13@apache-hadoop]$ sh CDH_Navigator_HDFS_Old_File_Parser/bin/trigger_navigator_hdfs_old_file_parser.sh
 PROJECT:        Navigator Files Parser
 AUTHOR:         Naresh Jangra
 CREATED:        15th Feb, 2018
 PURPOSE:        Get the Files which were Never accessed in last N Days

Job Triggered. Check latest log file at /home/nrsh13/CDH_Navigator_HDFS_Old_File_Parser-master/logs
```

## Contact
nrsh13@gmail.com

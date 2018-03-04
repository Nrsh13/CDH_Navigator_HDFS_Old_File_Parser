'''
This Program will read the conf/properties.yml, get the required details, use these details to find all files which were never accessed in last N days and store the results in Hive Table.

Project: Navigator HDFS Old File Parser
Purpose: To Create a Hive table for all HDFS files which were never accessed in last N number of Days.
Date: 01-Mar-2018

Inputs: Takes from properties.yml
- hostport: Navigator Host and Port
- user: Username for Navigator login
- password: Password for Navigator login
- db: Hive Database Name
- table: Hive Table Name
- inpaths: HDFS paths to be checked
- days: Check Files never accessed in last N Number of days 
Outputs:
- Hive Table

'''

## Import Pyspark Modules
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

## Import Python Modules
import sys, os, argparse
import subprocess
from types import *
import requests, json, urllib
from datetime import datetime, timedelta

## Import My Modules
from lib.Logger import LogAdmin
from lib.PyUtils import Utils

def banner():
	'''
	Purpose: To logging Start of Program execution
	'''
	logger('INFO', '')
	logger('INFO', '************************************************')
	logger('INFO', '*               NAVIGATOR PARSER               *')
	logger('INFO', '************************************************')
        logger('INFO', '')


def runShell(cmd):
        '''
        Purpose: To Run any Shell Command
        '''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE ,shell=True)
        p.communicate()
        return p

	
def get_old_files(user, password, hostport, path, days, data_path) :
        '''
        Purpose: To Make Navigator API calls and Stored results in HDFS
        '''
	logger('INFO',"Removing old data files from %s" %(data_path))
	cmd = "rm -f "+data_path+"/*"
	runShell(cmd)

	assert type(days) is IntType, "days is not an integer: %r" % days

        logger('INFO',"Setting up API details")
	host = """http://{hostport}/api/v10/""".format(hostport=hostport)

	##  Query Filters & Parameters
	from_ts = (datetime.utcnow() - timedelta(days=days+180)).strftime('%Y-%m-%dT%H:%M:%SZ')
	to_ts  = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
	o = 0
	l = 1000
	backlog = True # set to True to do backlog search

	## Get first page of query
	q = ("""+fileSystemPath:"{path}" -fileSystemPath:*.temp* """+
        	"""+type:file +sourceType:hdfs +deleted:false """+
	        """+lastAccessed:[{from_ts} TO {to}]""").format(path=path, from_ts=from_ts, to=to_ts)

	query = """interactive/entities?query={q}&limit={lim}&offset={offset}""".format(q=urllib.quote_plus(q), lim = l, offset = o)

	logger('INFO',"Below is the Prepared query for RANGE %s TO %s" %(from_ts,to_ts))
	logger('INFO',"%s%s" %(host,query))
	logger('INFO',"Making the API Call to Navigator")

	try:
		response = requests.get(host + query, auth=(user, password))
	except Exception,e:
		logger('ERROR',"API Call Failed while making Connection")
		os.system("rm -f "+data_path+"/../pids/*.pid")
		logger('ERROR',"%s" %e)
                logger('ERROR',"Exiting !!")

	## Check API results
	if response.ok:
		response = response.json()
		logger('INFO',"API Call Ended")
		json_data = response['results']
		logger('INFO',"We got %s matching Results for ==> %s" %(response['totalMatched'],path))

		if response['totalMatched'] == 0:
			logger('INFO',"Existing as Zero Matching Results Found !!")
	                logger('INFO',"Exiting !!\n")
			return False

		logger('INFO',"Writing Results to %s/myresult_0.json" %(data_path))
		
		with open(data_path+"/myresult_0.json", "a+") as outfile:
        		json.dump(response['results'],outfile)

	else:
		logger('ERROR',"API Call FAILED %s\n" %(response.reason))
                logger('ERROR',"Exiting !!")
                os.system("rm -f "+data_path+"/../pids/*.pid")
		sys.exit()
	
	## Paginate through remaining results
	pages = range(1, response['totalMatched']/response['limit'] + 1)

	if backlog :
        	pages = pages[:50]
        	logger('INFO',"pages are : %s" %(pages))

	for o in pages :
	       	query = """interactive/entities?query={q}&limit={lim}&offset={offset}""".format(q=urllib.quote_plus(q), lim = l, offset = o*l)
	        logger('INFO',"Below is the prepared Query for offset %s " %(o*l))
		logger('INFO',"%s%s" %(host,query))
	        logger('INFO',"Making the API Call to Navigator")
		response = requests.get(host + query, auth=(user, password)).json()
                logger('INFO',"API Call Ended")

                logger('INFO',"Writing Results to "+data_path+"/myresult_"+str(o)+".json")
        	with open(data_path+"/myresult_"+str(o)+".json", "a+") as outfile:
			json.dump(response['results'],outfile)

	logger('INFO',"Creating HDFS directory /tmp/tempfiles, Removing Old Files and putting new Results")

	res = runShell("hadoop fs -test -d /tmp/tempfiles")

	if res.poll() != 0:
		logger('INFO',"HDFS Path /tmp/tempfiles does not exists. Creating it and placing the API results here")
		cmd = "hadoop fs -mkdir /tmp/tempfiles;hadoop fs -put "+data_path+"/myresult* /tmp/tempfiles/"
                logger('INFO', "Shell Command prepared is")
                logger('INFO',cmd)
		runShell(cmd)             
		logger('INFO',"Files placed in HDFS at /tmp/tempfiles Successfully !!")

	else:
                logger('INFO',"HDFS Path /tmp/tempfiles exists. Placing all the API results in a single file in HDFS")
		cmd = "hadoop fs -rm -r /tmp/tempfiles/*;hadoop fs -put "+data_path+"/myresult* /tmp/tempfiles/"
		logger('INFO', "Shell Command prepared is")
		logger('INFO',cmd)
		runShell(cmd)
                logger('INFO',"Files placed in HDFS at /tmp/tempfiles Successfully !!")

        return True

def process_data(database,table):
        '''
        Purpose: To Process the API results using SPARK and store in HDFS
        '''
	try:
	        logger('INFO',"LOADING the Data in Spark for Processing ")

		df = myspark.read.format("json").options(inferSchema=True,dateFormat="yyyy-MM-dd", timestampFormat="yyyy-MM-dd'T'HH:mm:ss.SSSZZ", ignoreLeadingWhiteSpace=True,ignoreTrailingWhiteSpace=True, path="/tmp/tempfiles/").load()

	        logger('INFO',"Changing the Data Type to Timestamp for few Columns")

		df = df.withColumn("created",F.from_utc_timestamp(df.created, "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'").cast(T.TimestampType())).withColumn("lastModified",F.from_utc_timestamp(df.lastModified, "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'").cast(T.TimestampType())).withColumn("lastAccessed",F.from_utc_timestamp(df.lastAccessed, "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'").cast(T.TimestampType()))

		df = df.withColumn("created", F.date_format(df.created, "yyyy-MM-dd HH:mm:ss")).withColumn("lastModified", F.date_format(df.lastModified, "yyyy-MM-dd HH:mm:ss")).withColumn("lastAccessed", F.date_format(df.lastAccessed, "yyyy-MM-dd HH:mm:ss"))

	        logger('INFO',"Choosing the 11 required Columns ")

		finaldf = df.select("owner","parentPath","originalName","created","lastModified","lastAccessed","size","sourceType","permissions","group","identity")

	        logger('INFO',"%s Records will be LOADED into %s.%s Table "  %(finaldf.count(),database,table))

		logger('INFO',"Create Table Command Prepared:")

		cmd = "CREATE EXTERNAL TABLE IF NOT EXISTS %s.%s (owner STRING,parentPath STRING,originalName STRING,created timestamp,lastModified timestamp,lastAccessed timestamp,size BIGINT,sourceType STRING,permissions STRING,group STRING,identity BIGINT)STORED AS PARQUET LOCATION  '/z0/tech/%s'" %(database,table,table)

		logger('INFO',cmd)
	
		logger('INFO',"Creating the Table %s.%s if NOT EXISTS" %(database,table))

		myspark.sql(cmd)

		finaldf.createOrReplaceTempView("mytable")

	        logger('INFO',"INSERT INTO TABLE Table Command Prepared:")

		cmd = """INSERT INTO TABLE {database}.{table} SELECT owner,parentPath,originalName,created,lastModified,lastAccessed,size,sourceType,permissions,group,identity FROM mytable""".format(database=database, table=table)

	        logger('INFO',cmd)

	        logger('INFO',"Inserting the Data in %s.%s Table" %(database,table))

		myspark.sql(cmd)

		logger('INFO',"%s Records Inserted successfully in %s.%s" %(finaldf.count(),database,table))

        except Exception,e :
		logger('ERROR',"Job Failed with below Details !!")
		logger('ERROR',"%s\n" %e)
		logger('ERROR',"Exiting !!")
		sys.exit()

if __name__ == '__main__':

	## Setting up Different Paths
	src_path = os.path.dirname(os.path.abspath(__file__)) # Your Scripts Parent Path
	project_path = os.path.dirname(src_path)
        data_path = os.path.join(project_path, 'data')
	conf_path = os.path.join(project_path, 'conf')
	properties = os.path.join(conf_path, 'properties.yml')
	job_name = os.path.basename(__file__).strip(".py")
	log_path = os.path.join(project_path, 'logs')
	logfile = os.path.join(log_path, job_name + '.log')

	## Get required details from conf/properties.yml
	doc = Utils.parse_yaml(properties)
	host = doc['navconf']['host']
	port = doc['navconf']['port']
	hostport = host+':'+str(port)
	user = doc['navconf']['user']
	password = doc['navconf']['password']
	database = doc['dbconf']['hive']['db']
        table = doc['dbconf']['hive']['table']
	days = doc['numdays']['days']
	pathlist = doc['taskconf']['inpaths']

	## Setting up the Logger
        loggername = 'NAVIGATOR-PARSER'
	logger = LogAdmin(loggername, logfile).setLog
        banner()

	logger('INFO',"Job Started")
	logger('INFO',"Details Collected: hostport=%s, database=%s, table=%s, basePath=%s, days=%s" %(hostport,database,table,pathlist,days))

	## Run the JOB on required HDFS Paths
	for basePath in pathlist:

        	logger('INFO',"Get OLD Files for %s using get_old_files() Function" %(basePath))

		status = get_old_files(user, password, hostport, basePath, days, data_path)

		if status is True:

		        logger('INFO',"Creating Spark Session 'myspark'")
	
		        myspark = SparkSession.builder.master("yarn").appName("Old_File_Listing").enableHiveSupport().getOrCreate()

			logger('INFO',"Spark Session Created successfully")

			logger('INFO',"Processing HDFS data from /tmp/tempfiles")
	
			logger('INFO',"Calling process_data() Function")

			process_data(database, table)
        
			logger('INFO',"Data Processed Successfully !! \n")
		else:
			pass

	# Remove the JOB Lock after completion
	lock_path = os.path.join(project_path, 'pids/')
	os.system("rm -f "+lock_path+"*.pid")

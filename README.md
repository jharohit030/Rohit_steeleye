# Rohit_steeleye
## Main.py

In this file i have done the my operation related to same mention in assignment which as follow:
1. download and extract the zip file from the url
2. After extraction done make this zip file to xml file
3. when zip converted to xml successful, create the csv file and write the columns name mention in assignment
4. after writing the row to the csv file 
5. Make separate class for testting and doing some unit test case
6. check for file extraction, convert to xml , creation of output file and check for the null values.

## connection.py
1. In this file we first make connection establishment with the Aws CLI by using the aws secret key
2. After that check for the existing bucket in s3
3. Create the new bucket in s3 with the name and respective location
4. After creation, upload the output file to that particular bucket
5. give the file access to public in aws interface


## Steeleye.log

All the logs related to the code in main.py are present here, like file creation , conversion, extraction, downloading and if 
some point any erro occur all the things are log in this file.


## output.csv

this file is basically our output file that we got after the process


#connec_log

Inside this file all the log are present related connection.py, as listing bucket, creation bucket, file upload and if sone error occur all
the log are present in the file.

##requirement.txt

this file basically have the all the module list that we are importing in the code.

# s1 and s2 are the png image of file upload and bucket creation in AWS interface.

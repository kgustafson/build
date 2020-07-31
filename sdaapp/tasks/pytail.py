import csv
import os
import sys
import glob
from pygtail import Pygtail as pt
from io import StringIO

indir = '/usr/local/airflow/ingest/'
inpost = '.csv'
outdir = '/usr/local/airflow/snippets/'
outpost = '.csv'
timecolumn = 0
filelist = indir + 'fileMonitor'
headerfile = indir + 'header.csv'

def printHeader(fo):
   headin = open(headerfile, "r")
   for line in headin:
      fo.write(line)
   headin.close
   return

def getBucket(indate):
    if len(indate) > 0:
       val = indate.split(":")
       if len(val) > 1:
          mins = int(val[1])
          bucketNum=int(mins/15) + 1
          if bucketNum == 1:
             retval = infile+"-"+val[0]+":00"
          if bucketNum == 2:
             retval = infile+"-"+val[0]+":15"
          if bucketNum == 3:
             retval = infile+"-"+val[0]+":30"
          if bucketNum == 4:
             retval = infile+"-"+val[0]+":45"
       else:
          retval=""
    else:
       retval=""
    return (retval)
getFiles = open(filelist, "r")
for infile in getFiles:
     infile = infile.strip()
     # Check that file exists
     infiler = indir + infile + inpost
     if not(os.path.isfile(infiler)):
         print("*** Error *** : File " + infiler + " does not exist...")
     else:
         cnt=1
         offset = infiler + '.offset'
         process1 = os.path.isfile(offset)
         for line in pt(infiler):
             readCSV = csv.reader([line])
             for row in readCSV:
                if ((process1) or (cnt != 1)):
                   bucketNum = getBucket(row[timecolumn])
                   fileout = outdir + bucketNum + outpost

                   # check if file exists.  If it doesn't write out header
                   if not(os.path.isfile(fileout)): 
                       print("Creating output file " + fileout)
                       printheader = True
                   else:
                       printheader = False
                   fo = open(fileout, "a+")
                   if (printheader):
                      printHeader(fo)
                   fo.write(','.join(row) + "\n")
                   fo.close
                cnt+=1

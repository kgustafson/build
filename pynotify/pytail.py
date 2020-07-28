import sys
import os
import glob
from pygtail import Pygtail as pt
incoming_Hz = 1 # in seconds
interval = 15 # in minutes
numrecs = interval * incoming_Hz * 60
outdir = "outdir/"
outpost = ".csv"
prefix = "snip"
inpost = ".csv"
indir = "indir/"

def getSnipNum(filecheck):
   list_of_files = glob.glob(filecheck) 
   if len(list_of_files) == 0:
      snipnum = 1
   else:
       latest_file = max(list_of_files, key=os.path.getctime)[-9:]
       snipnum=int(latest_file[:5])
       snipnum+=1
   return(snipnum)

def removeEmptyFiles(filedir):
   filecheck=filedir+"*.csv"
   fileList=glob.glob(filecheck)
   for filename in fileList:
       if os.stat(filename).st_size==0:
           print("Removing empty file " + filename + "...")
           os.remove(filename)

if (len(sys.argv) < 2):
   print("Usage : python pytail.py <Filename>")
   sys.exit()
for infile in sys.argv[1:]:
   print("Processing " + infile + ".csv...")
   # Check that file exists
   infiler = indir + infile + inpost 
   if not(os.path.isfile(infiler)):
   # If it doesn't print error here
       print("*** Error *** : File " + infiler + " does not exist...")
   # Else go on
   else:
       filecheck = outdir + infile + "_" + prefix + "*"

       # Get snippet_num for file name
       snippet_num = getSnipNum(filecheck) 
       currnum = str(snippet_num).zfill(5)
       outfile = outdir + infile + "_" + prefix + currnum + outpost
       totcnt = 1
       cnt = 1
       of = open(outfile,"a+")
       for line in pt(infiler):
            of.write(line)
            if (cnt == numrecs):
                cnt = 1
                of.close()
                snippet_num += 1
                currnum = str(snippet_num).zfill(5)
                outfile = outdir + infile + "_" + prefix + currnum + outpost
                of = open(outfile,"w")
            else:
                cnt += 1
            totcnt += 1
       of.close()
       totcnt -=1
       print("\tProcessed " + str(totcnt) + " Records...")
removeEmptyFiles(outdir)

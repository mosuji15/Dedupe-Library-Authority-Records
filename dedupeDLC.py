#example usage: $ python dedupeDLC.py 'MONTHLY RELATED.352' 'MONTHLY RELATED.353' -outFile 'dedupedSeptemberDLC.txt'
#note: get help with the params to pass with 'python dedupeDLC.py -h'
#note: you can pass many files to the program
#note: all files' deduped output are combined and appended to into the output file

import argparse
import re

def dedupe():
  #parse command line arguments e.g. get input vs output file names
  args = getParsedArgs()

  #keep a set of the recordNumbers we've encountered
  recordNumbersSet = set()

  #open the output file in write mode
  outFile = args.outFile
  with open(outFile, 'a') as outfile: #change from 'a' append mode to 'w' if we want to overwrite the output file
    #for each filepath in the command line arguments
    for filepath in args.files:
      #open the file for reading, fp is the pointer to the file object
      with open(filepath, 'r') as fp:        
        #start reading each line from file
        line = fp.readline()      
        while line:
          #get the record number (returns None if no record number in line)
          recordNumber = getRecordNumber(line)
          if(recordNumber):
            #check if we've already seen this record number
            if (recordNumber in recordNumbersSet):
              duplicateRecordNumber = recordNumber
              writeDuplicateSkipped(outfile, duplicateRecordNumber, line)
              
              #we're searching for the next record b/c we found a dupilicate section
              line = fp.readline() 
              while(len(duplicateRecordNumber) > 0 and line):
                if(not isDLCLine(line)):
                  writeSkippedAssociatedLine(outfile, duplicateRecordNumber, line)
                  line = fp.readline()        
                else:
                  #encountered next DLC line, no longer skipping duplicate, continue with this line as the next line
                  duplicateRecordNumber = ''
            else:
              #write the line as is to the outfile
              recordNumbersSet.add(recordNumber)
          #write the file and move to the next line for the next loop iteration
          outfile.write(line)
          line = fp.readline()


#helper methods
def getRecordNumber(line):
  if (isDLCLine(line)):
    #use regex to get the record number from DLC line
    recordNumberRegex = re.compile('[0-9]+')
    matches = recordNumberRegex.findall(line)
    if (len(matches) > 0):
      return matches[0]
    else:
      return None
  else:
    return None

def isDLCLine(line):
  dlcRegex = re.compile('^\(DLC\)')
  if (len(dlcRegex.findall(line)) > 0):
    return True
  else:
    return False

def getParsedArgs():
  parser = argparse.ArgumentParser(prog='dedupeDLC', usage='%(prog)s fileName1 [fileName2...] -outputFile filePath',description='Program to dedupe DLC records')
  parser.add_argument('files', metavar='file', type=str, nargs='+', help='file path for the input files')
  parser.add_argument('-outFile', metavar='outFile', type=str, help='file path for the output file', required=True)
  return parser.parse_args()

def writeDuplicateSkipped(outfilePointer, duplicateRecordNumber, line):
  #TODO: add line number and file name to printed message
  outfilePointer.write('\n***DUPLICATE SKIPPED*** record number:{}, skipped line:{}\n'.format(duplicateRecordNumber, line))

def writeSkippedAssociatedLine(outfilePointer, duplicateRecordNumber, line):
  #TODO: add line number and file name to printed message
  outfilePointer.write('***ASSOCIATED LINE SKIPPED*** record number:{}, skipped line:{}\n'.format(duplicateRecordNumber, line))

#run the program
dedupe()

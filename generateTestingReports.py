from helperFunctions import *
import sys
import os

print "Reading in test data...\n\n"

# <3 because the generateTestingReports.py counts as an argument
if(len(sys.argv) < 3):
    print "Please provide two arguments: the path of the automation project and the output path for the csv file."    
else:
    sourceDirectory = sys.argv[1]
    outputDirectory = sys.argv[2]

    try:
        fileLibrary = processFileTree(sourceDirectory, [])
        createCSVReport(fileLibrary, outputDirectory)
    except:
        print "Bad source or output directory, report was not generated."
        print "If the path contains a space, enclose it in quotes."

raw_input("Press enter")
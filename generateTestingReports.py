from helperFunctions import *
from fileData import *
import re
import os
import csv

def processFileTree(currentDir, fileLibrary):
    # recursively move through directory finding .cs files and processing them.
    # returns the full file library.
    currentDir = os.path.abspath(currentDir)
    filesInCurDir = os.listdir(currentDir)

    for file in filesInCurDir:
        curFile = os.path.join(currentDir, file)
        if os.path.isfile(curFile):
            curFileExtension = curFile[-2:]

            if curFileExtension in ['cs']:
                fileData = findAttributes(curFile, currentDir)
                if(fileData.nTests > 0):
                    fileLibrary.append(fileData)
        else:
            processFileTree(curFile, fileLibrary)
    return fileLibrary

def findAttributes(fileName, directoryName):
# look through file, identify tests, ignores, test type etc.
# returns fileData list
    lines = splitFileIntoLines(fileName)
    tests, fixtures, ignores, lineNumber, testType = 0, 0, 0, 0, "nonbrowser"
    notImplemented, needsInvestigation = 0, 0
    for line in lines:
        #remove starting tabs, skip comments
        line = removeTabs(line)
        if isComment(line):
            lineNumber += 1
            continue
        #check if there are signs of Watin/Selenium files
        attemptTestType = findTestType(line)
        if(attemptTestType != -1): testType = attemptTestType
        if containsPhrase(line, getTestFixturePhrases()): fixtures += 1
        #look for tests and ignores
        if containsPhrase(line, getTestPhrases()):
            skip = 1
            while not (re.search('[a-zA-Z]', lines[lineNumber+skip])):
                skip += 1
            
            #add a test unless it's part of a TestCase structure
            if not (containsPhrase(lines[lineNumber-1], getTestCasePhrases())):
                tests += 1

            if containsPhrase(line, getIgnorePhrases()):
                ignores += 1
                if(containsPhrase(line, getNotImplementedPhrases())):
                    notImplemented += 1
                if(containsPhrase(line, getNeedsInvestigationPhrases())):
                    needsInvestigation += 1
                    
        if containsPhrase(line, getTestCasePhrases()):
            tests += 1

        lineNumber += 1
	
    fileObject = FileData(shortenFilename(fileName), determineSuite(directoryName), testType, tests, ignores, needsInvestigation, notImplemented)
    return fileObject

def createCSVReport(fileLibrary, directory):
#writes to the given directory
    path = directory + "\\testingreport.csv"
    with open(path, 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        data = createTestReport(fileLibrary)
        a.writerows(data)
        print "Report was generated in " + path

print "Reading in test data...\n\n"

fileLibrary = []

path = splitFileIntoLines("SET_SOURCE_PATH_HERE.txt")[0]
driveDirectory = splitFileIntoLines("SET_OUTPUT_PATH_HERE.txt")[0]

fileLibrary = processFileTree(path, fileLibrary)
createCSVReport(fileLibrary, driveDirectory)

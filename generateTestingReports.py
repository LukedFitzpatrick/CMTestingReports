from helperFunctions import *
import re
import os
import csv

# index of each piece of data within the standard fileData format
NAMEINDEX, FIXTURESINDEX, TESTSINDEX, TESTLISTINDEX, IGNORESINDEX, IGNORELISTINDEX, TESTTYPEINDEX = 0, 1, 2, 3, 4, 5, 6
SUITEINDEX, INVESTIGATIONINDEX, INVESTIGATIONLISTINDEX, NOTIMPLEMENTEDINDEX, NOTIMPLEMENTEDLISTINDEX = 7, 8, 9, 10, 11

# identifiers of filetypes.
WATIN, WEBDRIVER, NONBROWSER = 0, 1, 2

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
                if(fileData[FIXTURESINDEX] > 0):
                   fileLibrary.append(fileData)
        else:
            processFileTree(curFile, fileLibrary)
    return fileLibrary

def findAttributes(fileName, directoryName):
# look through file, identify tests, ignores, test type etc.
# returns fileData list
    lines = splitFileIntoLines(fileName)
    testNames, ignoreNames, tests, fixtures, ignores, lineNumber, testType = [], [], 0, 0, 0, 0, NONBROWSER
    notImplemented, needsInvestigation, notImplementedList, needsInvestigationList = 0, 0, [], []
    for line in lines:
        #remove starting tabs, skip comments
        line = removeTabs(line)
        if isComment(line):
            lineNumber += 1
            continue
        #check if there are signs of Watin/Selenium files
        attemptTestType = findTestType(line)
        if(attemptTestType != -1):
            testType = attemptTestType

        if containsPhrase(line, getTestFixturePhrases()):
            fixtures += 1
        #look for tests and ignores
        if containsPhrase(line, getTestPhrases()):
            skip = 1
            while not (re.search('[a-zA-Z]', lines[lineNumber+skip])):
                skip += 1
            
            testNames.append(getFunctionNameFromLine(lines[lineNumber+skip])) 
            #add a test unless it's part of a TestCase structure
            if not (containsPhrase(lines[lineNumber-1], getTestCasePhrases())):
                tests += 1

            if containsPhrase(line, getIgnorePhrases()):
                ignoreNames.append(getFunctionNameFromLine(lines[lineNumber+skip]))
                ignores += 1
                if(containsPhrase(line, getNotImplementedPhrases())):
                    notImplemented += 1
                    notImplementedList.append(getFunctionNameFromLine(lines[lineNumber+skip]))
                if(containsPhrase(line, getNeedsInvestigationPhrases())):
                    needsInvestigation += 1
                    needsInvestigationList.append(getFunctionNameFromLine(lines[lineNumber+skip]))
                    
        if containsPhrase(line, getTestCasePhrases()):
            tests += 1

        lineNumber += 1
    return [shortenFilename(fileName), fixtures, tests, testNames, ignores, ignoreNames, testType, determineSuite(directoryName),
            needsInvestigation, needsInvestigationList, notImplemented, notImplementedList]


def createCSVReport(fileLibrary, directory):
#writes to the given directory
    path = directory + "\\testingreport.csv"
    with open(path, 'wb') as fp:
        totalSelenium, totalWatin, totalNeutral, totalIgnores, totalNotImplemented, totalNeedsInvestigation = 0, 0, 0, 0, 0, 0

        a = csv.writer(fp, delimiter=',')
        data = []
        
        data.append(["Suite Name", "Selenium Tests", "Watin Tests", "Neutral Tests", "Ignored Tests", "Not Implemented", "Needs Investigation", "Total Tests"])
        for suite in getSuites():
            selenium = suiteTestCount(fileLibrary, suite, WEBDRIVER)
            totalSelenium += selenium
            watin = suiteTestCount(fileLibrary, suite, WATIN)
            totalWatin += watin
            neutral = suiteTestCount(fileLibrary, suite, NONBROWSER)
            totalNeutral += neutral
            total = selenium + watin + neutral
            ignores = countBySuite(fileLibrary, suite, IGNORESINDEX)
            totalIgnores += ignores
            notImplemented = countBySuite(fileLibrary, suite, NOTIMPLEMENTEDINDEX)
            totalNotImplemented += notImplemented
            needsInvestigation = countBySuite(fileLibrary, suite, INVESTIGATIONINDEX)
            totalNeedsInvestigation += needsInvestigation
            if total > 0:
                data.append([suite, selenium, watin, neutral, ignores, notImplemented, needsInvestigation, total])

        totalTotal = totalSelenium + totalWatin + totalNeutral
        data.append(["Total", totalSelenium, totalWatin, totalNeutral, totalIgnores, totalNotImplemented, totalNeedsInvestigation, totalTotal])
        a.writerows(data)
        print "Report was generated in " + path

print "Reading in test data...\n\n"
fileLibrary = []

path = splitFileIntoLines("SET_SOURCE_PATH_HERE.txt")[0]
driveDirectory = splitFileIntoLines("SET_DRIVE_PATH_HERE.txt")[0]

fileLibrary = processFileTree(path, fileLibrary)
createCSVReport(fileLibrary, driveDirectory)

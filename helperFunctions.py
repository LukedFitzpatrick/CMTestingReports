from fileData import *
import re
import os
import csv

# Phrases to look for in each .cs file
def getTestPhrases():
    return ["[Test]", "[Test ", "[Test,"]
def getTestFixturePhrases():
    return ["[TestFixture"]
def getTestCasePhrases():
    return ["[TestCase"]
def getIgnorePhrases():
    return ["Ignore(", "(Ignore", "Ignore]"]
def getNotImplementedPhrases():
    return ["NotImplemented"]
def getNeedsInvestigationPhrases():
    return ["NeedsInvestigation"]
def getWatinPhrases():
    return ["WebBrowserController", "WatinTestContext", "\"WatinTest"]
def getSeleniumPhrases():
    return ["WebDriverTestContext"]

# searches through the fileLibrary and creates an array of the encountered suites.
def getSuites(fileLibrary):
    suites = []
    for file in fileLibrary:
        if not file.suite in suites:
            suites.append(file.suite)
    return suites

# recursively move through directory finding .cs files and processing them, returns a file library
def processFileTree(currentDir, fileLibrary):
    currentDir = os.path.abspath(currentDir)
    filesInCurDir = os.listdir(currentDir)
    for file in filesInCurDir:
        curFile = os.path.join(currentDir, file)
        if os.path.isfile(curFile):
            curFileExtension = curFile[-2:]
            if curFileExtension in ['cs']:
                fileData = findAttributes(curFile)
                if(fileData.nTests > 0):
                    fileLibrary.append(fileData)
        else:
            processFileTree(curFile, fileLibrary)
    return fileLibrary

# finds whether a file is a "selenium", "watin" or "nonbrowser" test, returns a string with the test type
def determineTestType(lines):
    testType = "nonbrowser"
    for line in lines:
        line = removeTabs(line)
        if not isComment(line):
            attemptTestType = findTestType(line)
            if(attemptTestType != -1):
                testType = attemptTestType
    return testType

# count the number of tests, ignores and specific ignores in a list of lines, returns a fileData object
def countData(lines, filePath):
    lineNumber = 0
    fileObject = FileData(shortenFilename(filePath), determineSuite(filePath), "nonbrowser")
    fileObject.testType = determineTestType(lines)
    
    for line in lines:
        line = removeTabs(line)
        if not isComment(line):
            #if there's not a test case in the few lines above, add a test if it's there
            if addPossibleOccurence(lines[lineNumber-1], getTestCasePhrases) == 0:
                fileObject.nTests += addPossibleOccurence(line, getTestPhrases)
            
            fileObject.nIgnores += addPossibleOccurence(line, getIgnorePhrases)
            fileObject.nNotImplemented += addPossibleOccurence(line, getNotImplementedPhrases)
            fileObject.nNeedsInvestigation += addPossibleOccurence(line, getNeedsInvestigationPhrases)
            fileObject.nTests += addPossibleOccurence(line, getTestCasePhrases)
        lineNumber += 1
    return fileObject

# takes a fileName and directoryName and returns a fileData object of the file.
def findAttributes(fullPath):
    lines = splitFileIntoLines(fullPath)
    return countData(lines, fullPath)

# gets a ready made test report and output it as a .csv
# NOTTESTED
def createCSVReport(fileLibrary, directory):
    path = directory + "\\testingreport.csv"
    with open(path, 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        data = createTestReport(fileLibrary)
        a.writerows(data)
        print "Report was generated in " + path
    
# returns 1 if any phrase in phrases occurs in line, otherwise returns 0
# note that phrases is a function, to just pass in a string, use lambda: "string"
def addPossibleOccurence(line, phrases):
    if containsPhrase(line, phrases()):
        return 1
    else:
        return 0

# creates and returns a list of lists of a test report.
# NOTTESTED
def createTestReport(fileLibrary):
    totalSelenium, totalWatin, totalNeutral, totalIgnores, totalNotImplemented, totalNeedsInvestigation = 0, 0, 0, 0, 0, 0
    data = []
    data.append(["Suite Name", "Selenium Tests", "Watin Tests", "Neutral Tests", "Ignored Tests", "Not Implemented", "Needs Investigation", "Total Tests"])
    for suite in getSuites(fileLibrary):

        selenium = suiteTestCount(fileLibrary, suite, "selenium")
        watin = suiteTestCount(fileLibrary, suite, "watin")
        neutral = suiteTestCount(fileLibrary, suite, "nonbrowser")     
        ignores = countIgnoresBySuite(fileLibrary, suite)
        notImplemented = countNotImplementedBySuite(fileLibrary, suite)
        needsInvestigation = countNeedsInvestigationBySuite(fileLibrary, suite)

        totalSelenium += selenium
        totalWatin += watin
        totalNeutral += neutral
        totalIgnores += ignores
        totalNotImplemented += notImplemented
        totalNeedsInvestigation += needsInvestigation
        total = selenium + watin + neutral
        
        if total > 0:
            data.append([suite, selenium, watin, neutral, ignores, notImplemented, needsInvestigation, total])

    totalTotal = totalSelenium + totalWatin + totalNeutral
    data.append(["Total", totalSelenium, totalWatin, totalNeutral, totalIgnores, totalNotImplemented, totalNeedsInvestigation, totalTotal])
    return data
    
def splitFileIntoLines(fileName):
# splits a file into a list of its lines.
    try:
        f = open(fileName, 'r')
        lines = []
        for line in f:
            lines.append(line)
        return lines
    except IOError:
        print "Couldn't open " + fileName
        x = raw_input("")
    
def suiteTestCount(fileLibrary, suite, testType):
    count = 0
    for file in fileLibrary:
        if(file.suite == suite):
            if(file.testType == testType):
                count += file.nTests
    return count

def countIgnoresBySuite(fileLibrary, suite):
    count = 0
    for file in fileLibrary:
        if(file.suite == suite):
            count += file.nIgnores
    return count
	
def countNotImplementedBySuite(fileLibrary, suite):
    count = 0
    for file in fileLibrary:
        if(file.suite == suite):
            count += file.nNotImplemented
    return count

def countNeedsInvestigationBySuite(fileLibrary, suite):
    count = 0
    for file in fileLibrary:
        if(file.suite == suite):
            count += file.nNeedsInvestigation
    return count
    
def countAttributeBySuite(fileLibrary, suite, attribute):
    count = 0
    for file in fileLibrary:
        if(file.suite == suite):
            count += file.attribute
            
def determineSuite(filepath):
    parts = filepath.split("\\")
    for directory in parts:
        if "Automation." in directory:
            return directory
    return "Unknown"

def findTestType(line):
# look for Watin/Selenium phrases in a line
    testType = -1
    if containsPhrase(line, getSeleniumPhrases()):
        testType = "selenium"
    if containsPhrase(line, getWatinPhrases()):
        testType = "watin"
    return testType

def isComment(line):
    return (line[:2] == "//")

def removeTabs(line):
    return line.strip(' \t\n\r')

def shortenFilename(fileName):
    fileName = fileName.split("\\")
    return fileName[len(fileName)-1]

def containsPhrase(line, phrases):
    for phrase in phrases:
        if phrase in line:
            return True
    return False

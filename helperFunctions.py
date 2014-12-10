# identifiers of filetypes.

def getSuites(fileLibrary):
    suites = []
    for file in fileLibrary:
        if not file.suite in suites:
            suites.append(file.suite)
    return suites

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
    f = open(fileName, 'r')
    lines = []
    for line in f:
        lines.append(line)
    return lines

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

def getFunctionNameFromLine(line):
    line = line.strip(' \t\n\r')
    line = line.split(" ")
    return line[len(line) - 1]

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

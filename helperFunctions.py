# identifiers of filetypes.
WATIN, WEBDRIVER, NONBROWSER = 0, 1, 2

def getSuites():
    return ["Automation.Admin", "Automation.API", "Automation.APIWebhooks", "Automation.Autoresponders", "Automation.Browsers", "Automation.CampaignPayment",
          "Automation.Canvas", "Automation.Client", "Automation.Common", "Automation.CreateSend", "Automation.CreateSendExtra",
          "Automation.CustomDomains", "Automation.Database", "Automation.DataTransferObject", "Automation.DynamicContent", "Automation.Enum", "Automation.Helpers",
          "Automation.NUnitAddIns", "Automation.Observer", "Automation.PageData", "Automation.Reports", "Automation.Segments", "Automation.Smoke",
          "Automation.Subscribers", "Automation.SupportAdmin", "Automation.SystemEmails", "Automation.TestContext", "Automation.TestData", "Automation.Triggered", "Automation.Verification",
          "Tools"]

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
        testType = WEBDRIVER
    if containsPhrase(line, getWatinPhrases()):
        testType = WATIN
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

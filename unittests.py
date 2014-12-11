import unittest
from helperFunctions import *
from fileData import *

class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_getSuites(self):
        file1 = FileData("File1", "suite1", TestType.watin)
        file2 = FileData("File2", "suite1", TestType.watin)
        file3 = FileData("File3", "suite.2", TestType.selenium)
        file4 = FileData("File4", "suite2", TestType.selenium)
        fileLibrary = [file1, file2, file3, file4]
        self.assertEqual(getSuites(fileLibrary), ["suite1", "suite.2", "suite2"])
    
    def test_processFileTree(self):
        fileLibrary = []
        fileLibrary = processFileTree("", fileLibrary)
        self.assertIsNotNone(fileLibrary)
        
    def test_determineTestType(self):
        self.assertEqual(determineTestType(getWatinPhrases()), TestType.watin)
        self.assertEqual(determineTestType(getSeleniumPhrases()), TestType.selenium)
        self.assertEqual(determineTestType(["line1", "line2"]), TestType.nonbrowser)
     
    def test_countData(self):
        lines = ["[TestCase Red]", "[TestCase Blue]", "[Test Ignore(\"NotImplemented\")]", "[Test]", "[Test Ignore(\"NeedsInvestigation\")]"]
        file1 = FileData("name", "Automation.suite", TestType.selenium, 4, 2, 1, 1)
        actual = countData(lines, "Automation.suite\\name")
        self.assertEqual(actual.name, file1.name)
        self.assertEqual(actual.suite, file1.suite)
        self.assertEqual(actual.nTests, file1.nTests)
        self.assertEqual(actual.nIgnores, file1.nIgnores)
        self.assertEqual(actual.nNotImplemented, file1.nNotImplemented)
        self.assertEqual(actual.nNeedsInvestigation, file1.nNeedsInvestigation)

    def test_findAttributes(self):
        actual = findAttributes("C:\\Projects\\automation\\src\\Automation.Smoke\\SmokeTests.cs")
        self.assertEqual(actual.name, "SmokeTests.cs")
        self.assertEqual(actual.suite, "Automation.Smoke")
        self.assertEqual(actual.testType, TestType.selenium)
        self.assertEqual(actual.nTests, 16)
        self.assertEqual(actual.nIgnores, 1)
        self.assertEqual(actual.nNeedsInvestigation, 0)
        self.assertEqual(actual.nNotImplemented, 0)
    
    def test_addPossibleOccurence(self):
        self.assertEqual(addPossibleOccurence("shortlonglong", lambda: ["short"]), 1)
        self.assertEqual(addPossibleOccurence("longlonglong", lambda: ["short"]), 0)

    def test_countBySuite(self):
        fileLibrary = []
        fileLibrary.append(FileData("name1", "suite1", TestType.selenium, 5, 0, 0, 0))
        fileLibrary.append(FileData("name2", "suite1", TestType.selenium, 3, 0, 0, 0))
        fileLibrary.append(FileData("name3", "suite2", TestType.selenium, 2, 0, 0, 0))
        fileLibrary.append(FileData("name4", "suite1", TestType.watin, 5, 0, 0, 0))
        self.assertEqual(countBySuite(fileLibrary, "suite1", FileAttribute.nTests, TestType.selenium), 8)
    
    def test_determineSuite(self):
        self.assertEqual(determineSuite("C:\\Projects\\automation\\src\\Automation.Smoke\\SmokeTests.cs"), "Automation.Smoke")
    
    def test_findTestType(self):
        self.assertEqual(findTestType("//WebBrowserController.This()"), -1)
        self.assertEqual(findTestType("WebBrowserController.This()"), TestType.watin)
        self.assertEqual(findTestType("WebDriverTestContext //comment"), TestType.selenium)
    
    def test_isComment(self):
        self.assertEqual(isComment("//commented line"), True)
        self.assertEqual(isComment("    //tabbed comment line"), True)
        self.assertEqual(isComment("not a comment"), False)
    
    def test_removeTabs(self):
        self.assertEqual(removeTabs("   line of code    "), "line of code")
    
    def test_shortenFilename(self):
        self.assertEqual(shortenFilename("C:\\projects\\file.cs"), "file.cs")
    
    def test_containsPhrase(self):
        self.assertEqual(containsPhrase("chickenandcheese", ["chicken"]), True)
        self.assertEqual(containsPhrase("chickenandnodairy", ["cheese"]), False)
    
    def test_typeTests(self):
        file1 = FileData("name1", "suite1", TestType.selenium, 6, 0, 0, 0)
        self.assertEqual(file1.typeTests(TestType.selenium), 6)
        self.assertEqual(file1.typeTests(TestType.nonbrowser), 0)
if __name__ == '__main__':
    unittest.main()
import unittest
from helperFunctions import *
from fileData import *

class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_getSuites(self):
        file1 = FileData("File1", "suite1", "watin")
        file2 = FileData("File2", "suite1", "watin")
        file3 = FileData("File3", "suite.2", "webdriver")
        file4 = FileData("File4", "suite2", "webdriver")
        fileLibrary = [file1, file2, file3, file4]
        self.assertEqual(getSuites(fileLibrary), ["suite1", "suite.2", "suite2"])
    
    def test_processFileTree(self):
        fileLibrary = []
        fileLibrary = processFileTree("", fileLibrary)
        self.assertIsNotNone(fileLibrary)
        
    def test_determineTestTypeWatin(self):
        self.assertEqual(determineTestType(getWatinPhrases()), "watin")
    
    def test_determineTestTypeSelenium(self):
        self.assertEqual(determineTestType(getSeleniumPhrases()), "selenium")
    
    def test_determineTestTypeNonBrowser(self):
        self.assertEqual(determineTestType(["line1", "line2"]), "nonbrowser")
    
    def test_countData(self):
        lines = ["[TestCase Red]", "[TestCase Blue]", "[Test Ignore(\"NotImplemented\")]", "[Test]", "[Test Ignore(\"NeedsInvestigation\")]"]
        file1 = FileData("name", "Automation.suite", "selenium", 4, 2, 1, 1)
        actual = countData(lines, "name", "Automation.suite")
        self.assertEqual(actual.name, file1.name)
        self.assertEqual(actual.suite, file1.suite)
        self.assertEqual(actual.nTests, file1.nTests)
        self.assertEqual(actual.nIgnores, file1.nIgnores)
        self.assertEqual(actual.nNotImplemented, file1.nNotImplemented)
        self.assertEqual(actual.nNeedsInvestigation, file1.nNeedsInvestigation)

    def test_findAttributes(self):
        
        
if __name__ == '__main__':
    unittest.main()
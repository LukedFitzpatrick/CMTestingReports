class FileData: 
	def __init__(self, name, suite, testType, nTests=0, nIgnores=0, nNeedsInvestigation=0, nNotImplemented=0):
		self.name = name
		self.suite = suite
		self.testType = testType
		self.nTests = nTests
		self.nIgnores = nIgnores
		self.nNeedsInvestigation = nNeedsInvestigation
		self.nNotImplemented = nNotImplemented

    
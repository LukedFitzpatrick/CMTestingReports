class FileData:
	def __init__(self):
		pass
	
	def __init__(self, name, suite, testType, nTests, nIgnores, nNeedsInvestigation, nNotImplemented):
		self.name = name
		self.suite = suite
		self.testType = testType
		self.nTests = nTests
		self.nIgnores = nIgnores
		self.nNeedsInvestigation = nNeedsInvestigation
		self.nNotImplemented = nNotImplemented

class FileData:
    def __init__(self, name, suite, testType):
        self.name = name
        self.suite = suite
        self.testType = testType
        self.nTests = 0
        self.nIgnores = 0
        self.nNeedsInvestigation = 0
        self.nNotImplemented = 0
    
	def __init__(self, name, suite, testType, nTests, nIgnores, nNeedsInvestigation, nNotImplemented):
		self.name = name
		self.suite = suite
		self.testType = testType
		self.nTests = nTests
		self.nIgnores = nIgnores
		self.nNeedsInvestigation = nNeedsInvestigation
		self.nNotImplemented = nNotImplemented

    
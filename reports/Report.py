class Report:
	""" Base class for reports """

	def __init__(self):
		self.name = None
		self.description = None

	def run(self):
		''' Stub class that must be implemented in sub classes '''
		pass

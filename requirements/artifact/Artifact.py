from ..Utility import write_file

class Artifact:
	""" Base class for all artifact generators """

	def __init__(self):
		self.name = None
		self.description = None

	def generate(self, target_file):
		""" Stub class must be implemented in sub classes """
		pass

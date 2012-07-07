import os 

class Document:
	""" Save info about document """

	def __init__(self):
		self.name = ''
		self.path = ''

	def load_document(self, path):
		""" Check document exists and assign attribute values """
		if os.path.isfile(path):
			self.name = os.path.basename(path)
			self.path = os.path.abspath(path)
		else:
			raise Exception('can not find document "%s"' % path)

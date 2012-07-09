import os 

class Document:
	""" Save info about document """

	def __init__(self):
		self._file_name = None
		self._file_path = None

	def load_document(self, path):
		""" Check document exists and assign attribute values """
		if os.path.isfile(path):
			self._file_name = os.path.basename(path)
			self._file_path = os.path.abspath(path)
		else:
			raise Exception('can not find document "%s"' % path)

from ..Document import *
import pytest

class TestDocument():
	'''Unit tests'''

	def test_document_loads(self):
		doc = Document()
		doc.load_document('unittests/test_data/sample-repository/documents/design/erd.png')
		assert doc._file_name == 'erd.png'
		# The path should be absolute, so in order to make the unit tests
		# portable it is hard to check what it should be, will just have to do
		# to know it isn't empty..
		assert doc._file_path != ''

	def test_non_existent_document(self):
		doc = Document()
		random_document = 'xxx121231afwefwawef12.xxasfapeihiulhwafx'
		with pytest.raises(Exception):
			doc.load_document('random_document')

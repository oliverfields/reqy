from ..ConfigFile import *
import pytest

class TestConfigFile():
	'''Unit tests'''

	def test_file_nameing(self):
		cf = ConfigFile()
		cf._valid_file_extension = 'req'
		cf.set_name_and_id('1-1_some-amazing-requirement.req')
		assert cf._name == 'some-amazing-requirement'
		assert cf._id == '1-1'
		assert cf._pretty_name == '1-1 Some amazing requirement'

	def test_file_nameing_1(self):
		cf = ConfigFile()
		cf._valid_file_extension = 'req'
		cf.set_name_and_id('some-amazing-requirement.req')
		assert cf._name == 'some-amazing-requirement'
#		assert cf._id == ''
		assert cf._pretty_name == 'Some amazing requirement'

	def test_file_nameing_2(self):
		""" Check invalid file name """
		cf = ConfigFile()
		cf._valid_file_extension = 'req'
		with pytest.raises(SystemExit):
			cf.set_name_and_id('_afs.req')

	def test_file_nameing_3(self):
		cf = ConfigFile()
		cf._valid_file_extension = 'req'
		cf.set_name_and_id('/a/directory/hiearachy/some-amazing-requirement.req')
		assert cf._name == 'some-amazing-requirement'
		assert cf._pretty_name == 'Some amazing requirement'

	def test_file_nameing_4(self):
		cf = ConfigFile()
		cf._valid_file_extension = 'req'
		cf.set_name_and_id('/a/directory/hiearachy/22-21-11_some-amazing-requirement.req')
		assert cf._name == 'some-amazing-requirement'
		assert cf._id == '22-21-11'
		assert cf._pretty_name == '22-21-11 Some amazing requirement'

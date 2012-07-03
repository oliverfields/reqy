from ConfigFile import *

class Requirement(ConfigFile):

	def __init__(self):
		self.valid_settings = {
				'test': '',
				'test2': '',
				'test3': '',
			}
		self.valid_file_extension = 'req'

	def validate_settings(self):
		if hasattr(self, 'test'):
			if self.test == '':
				report_error(1, '%s: Test attribute can not be empty' % self._file_name)
		else:
			report_error(1, '%s: Test attribute missing' % self._file_name)

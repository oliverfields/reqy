import Settings
from ConfigFile import *

class Stakeholder(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.email = ''
		self.name = ''
		self.note = ''
		self.organization = ''
		self.phone = ''
		self.role = ''
		self._valid_file_extension = 'sth'

	def validate_settings(self):
		""" All checks to ensure the settings obey the business rules (syntax checks handled by parent class) """
		# Check all attributes exist
		for key, value in vars(self).items():
		  if hasattr(self, key) == False:
				report_error(1, '%s: Missing attribute "%s"' % (self._file_path, key))

		# Check mandatory attributes

		if self.name == '':
			report_error(1, '%s: Name field is empty or missing' % (self._file_path))
		
		if self.role == '':
			report_error(1, '%s: Role field is empty or missing' % (self._file_path))

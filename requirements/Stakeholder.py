from ConfigFile import *

class Stakeholder(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.email = None
		self.name = None
		self.note = None
		self.organization = None
		self.phone = None
		self.role = None
		self._valid_file_extension = 'sth'

	def validate_settings(self):
		""" All checks to ensure the settings obey the business rules (syntax checks handled by parent class) """
		# Check all attributes exist
		for key, value in vars(self).items():
		  if hasattr(self, key) == False:
				report_error(1, '%s: Missing attribute "%s"' % (self._file_path, key))

		# Check mandatory attributes

		if self.name == '' or self.name == None:
			report_error(1, '%s: Name field is empty or missing' % (self._file_path))
		
		if self.role == '' or self.name == None:
			report_error(1, '%s: Role field is empty or missing' % (self._file_path))

from ConfigFile import *

class ProjectConfig(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.name = None
		self._valid_file_extension = 'conf'

	def validate_settings(self):
		""" All checks to ensure the settings obey the business rules (syntax checks handled by parent class) """
		# Check all attributes exist
		for key, value in vars(self).items():
		  if hasattr(self, key) == False:
				Utility.report_error(1, '%s: Missing attribute "%s"' % (self._file_path, key))

		# Check mandatory attributes
		if self.name == None or self.name == '':
			Utility.report_error(1, '%s: Project name "%s" is not valid' % (self._file_path, self.name))

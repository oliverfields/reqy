import Settings
from ConfigFile import *
from LinkList import *

class GlossaryTermDefinition(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.created_by = ''
		self.created_on = ''
		self.definition = ''
		self.note = ''
		self.rejected_by = ''
		self.rejected_on = ''
		self.replaced_by = ''
		self.status = 'elaboration'
		self.status_reason = ''
		self.term = ''
		self.todo = ''
		self._valid_file_extension = 'def'

	def is_valid_status(self, status):
		if status == 'elaboration' or status == 'rejected' or status == 'approved' or status == 'replaced':
			return True
		else:
			return False

	def validate_settings(self):
		""" All checks to ensure the settings obey the business rules (syntax checks handled by parent class) """
		# Check all attributes exist
		for key, value in vars(self).items():
		  if hasattr(self, key) == False:
				report_error(1, '%s: Missing attribute "%s"' % (self._file_path, key))

		# Check mandatory attributes
		if self.is_valid_status(self.status) == False:
			report_error(1, '%s: Status "%s" is not valid' % (self._file_path, self.status))

		if self.definition == '':
			report_error(1, '%s: Definition field is empty or missing' % (self._file_path))
		
		if self.term == '':
			report_error(1, '%s: Term field is empty or missing' % (self._file_path))

		# If status is neither approved or elaboration reject reason must be stated
		if (self.status == 'rejected' or self.status == 'replaced') and self.status_reason == '':
			report_error(1, '%s: "Status reason" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is rejected a rejected by user must be specified
		if self.status == 'rejected' and self.rejected_by == '':
			report_error(1, '%s: "Rejected by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is replaced then Replaced by must be specified
		if self.status == 'replaced' and self.replaced_by == '':
			report_error(1, '%s: "Replaced by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

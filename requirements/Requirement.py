from ConfigFile import *

class Requirement(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.assigned_on = ''
		self.assigned_to = ''
		self.created_by = ''
		self.created_on = ''
		self.description = ''
		self.depends_on = ''
		self.documents = ''
		self.estimated_effort = ''
		self.estimated_cost = ''
		self.note = ''
		self.rationale = ''
		self.rejected_by = ''
		self.status = 'elaboration'
		self.status_reason = ''
		self.todo = ''
		self._valid_file_extension = 'req'

	def is_valid_status(self, status):
		if status == 'elaboration' or status == 'rejected' or status == 'approved' or status == 'postponed':
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

		if self.description == '':
			report_error(1, '%s: Description field is empty or missing' % (self._file_path))

		if self.rationale == '':
			report_error(1, '%s: Rationale field is empty or missing' % (self._file_path))

		# If status is neither approved or elaboration reject reason must be stated
		if (self.status == 'rejected' or self.status == 'postponed') and self.status_reason == '':
			report_error(1, '%s: "Status reason" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

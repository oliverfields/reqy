import Settings
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
		self.estimated_effort = '0'
		self.estimated_cost = '0'
		self.note = ''
		self.rationale = ''
		self.rejected_by = ''
		self.rejected_on = ''
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

		if self.is_integer(self.estimated_effort) == False:
			report_error(1, '%s: Estimated effort field has value "%s", but it must be an integer' % (self._file_path, self.estimated_effort))

		if self.is_integer(self.estimated_cost) == False:
			report_error(1, '%s: Estimated cost field has value "%s", but it must be an integer' % (self._file_path, self.estimated_cost))

		if self.is_string_date(self.created_on) == False:
			report_error(1, '%s: Created on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.created_on))

		if self.is_string_date(self.rejected_on) == False:
			report_error(1, '%s: Rejected on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.rejected_on))

		if self.is_string_date(self.assigned_on) == False:
			report_error(1, '%s: Assigned on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.assigned_on))

		try:
			self.are_valid_links('stakeholders', 'Assigned to', self.assigned_to, False)
			self.are_valid_links('stakeholders', 'Created by', self.created_by, False)
			self.are_valid_links('stakeholders', 'Rejected by', self.rejected_by, False)
			self.are_valid_links('documents', 'Documents', self.documents)
			self.are_valid_links('requirements', 'Depends on', self.depends_on)
		except Exception, error_message:
			report_error(1, '%s: %s' % (self._file_path, error_message))

		# If status is neither approved or elaboration reject reason must be stated
		if (self.status == 'rejected' or self.status == 'postponed') and self.status_reason == '':
			report_error(1, '%s: "Status reason" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is rejected a rejected by user must be specified
		if self.status == 'rejected' and self.rejected_by == '':
			report_error(1, '%s: "Rejected by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

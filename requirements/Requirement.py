from ConfigFile import *

class Requirement(ConfigFile):

	def __init__(self):
		self.valid_settings = {
				'assigned_on': '',
				'assigned_to': '',
				'created_by': '',
				'created_on': '',
				'description': '',
				'depends_on': '',
				'documents': '',
				'estimated_effort': '',
				'estimated_cost': '',
				'note': '',
				'rationale': '',
				'rejected_by': '',
				'status': 'elaboration',
				'status_reason': '',
				'todo': '',
			}
		self.setup_attributes()
		self.valid_file_extension = 'req'

	def is_valid_status(self, status):
		if status == 'elaboration' or status == 'rejected' or status == 'approved' or status == 'postponed':
			return True
		else:
			return False

	def validate_settings(self):
		# Check all attributes exist
		for key in self.valid_settings.keys():
		  if hasattr(self, str(key)) == False:
				report_error(1, '%s: Missing attribute "%s"' % (self._file_name, key))

		# Check mandatory attributes
		if self.is_valid_status(self.status) == False:
			report_error(1, '%s: Status "%s" is not valid' % (self._file_name, self.status))

		if self.description == '':
			report_error(1, '%s: Description field is empty/missing' % (self._file_name))

		if self.rationale == '':
			report_error(1, '%s: Rationale field is empty/missing' % (self._file_name))

		# If status is neither approved or elaboration reject reason must be stated
		if (self.status == 'rejected' or self.status == 'postponed') and self.status_reason == '':
			report_error(1, '%s: "Status reason" is missing, this is not allowed when status is "%s"' % (self._file_name, self.status))

import Settings
from ConfigFile import *
from Document import *
from Stakeholder import *

class Requirement(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.assigned_on = ''
		self.assigned_to = None
		self.created_by = None
		self.created_on = ''
		self.description = ''
		self.depends_on = None
		self.documents = None
		self.estimated_effort = '0'
		self.estimated_cost = '0'
		self.note = ''
		self.rationale = ''
		self.rejected_by = None
		self.rejected_on = ''
		self.status = 'elaboration'
		self.status_reason = ''
		self.todo = ''
		self._valid_file_extension = 'req'

	def parse_link_list_string(self, link_list_string):
		""" Accepts comma seperated string (may include line breaks) and returns array of each element """
		link_list = []

		if link_list_string == None:
			return None

		link_list_string.replace('\n', '')

		for link in link_list_string.split(','):
			link = link.strip()
			if len(link) > 0:
				link_list.append(link)
		
		if len(link_list) > 0:
			return link_list
		else:
			return None

	def load_link_targets(self, root_directory, link_list_string, file_extension):
		""" Load link list targets and return link list """
		link_list_string = self.parse_link_list_string(link_list_string)
		link_list = [] 
		if link_list_string:
			for link in link_list_string:
				file_path = os.path.join(Settings.repository_directory, os.path.join(root_directory, link)) + file_extension

				if os.path.isfile(file_path) == False:
					raise Exception('"%s" is broken' % link)

				if root_directory == 'documents':
					link_object = Document()
					link_object.load_document(file_path)
				elif root_directory == 'stakeholders':
					link_object = Stakeholder()
					link_object.load_config_from_file(file_path)
				elif root_directory == 'requirements':
					link_object = Requirement()
					link_object.load_config_from_file(file_path)
				else:
					raise Exception('unknown link list type "%s"' % root_directory)

				link_list.append(link_object)

			return link_list

	def make_link_list(self, root_directory, nice_attribute_name, link_list_string, multiple_allowed = True):
		""" Returns list of appropriate objects and check that each link exists as a file on disk """

		# If value None, then we are done:)
		if link_list_string == None or link_list_string == 'none':
			return None

		link_list_string = link_list_string.strip()

		if root_directory == 'requirements':
			file_extension = '.req'
		elif root_directory == 'documents':
			# Any extension is permissable
			file_extension = ''
		elif root_directory == 'stakeholders':
			file_extension = '.sth'
		else:
			raise Exception('Field "%s" has unknown link list type "%s"' % (nice_attribute_name, root_directory))

		# If multiple links not allowed, but there are more than one (i.e. a comma)
		if multiple_allowed == False and link_list_string.find(',') > 0:
			raise Exception('Field "%s" may only contain one link (content "%s")' % (nice_attribute_name, link_list_string))

		try:
			return self.load_link_targets(root_directory, link_list_string, file_extension)
		except Exception, error_message:
			raise Exception('Field "%s" %s link %s' % (nice_attribute_name, root_directory, error_message))

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

		# Read the link list attributes and change the string values to appropriate
		# list objects, bit dirty..
		try:
			self.assigned_to = self.make_link_list('stakeholders', 'Assigned to', self.assigned_to, False)
			self.created_by = self.make_link_list('stakeholders', 'Created by', self.created_by, False)
			self.rejected_by = self.make_link_list('stakeholders', 'Rejected by', self.rejected_by, False)
			self.documents = self.make_link_list('documents', 'Documents', self.documents)
			self.depends_on = self.make_link_list('requirements', 'Depends on', self.depends_on)
		except Exception, error_message:
			report_error(1, '%s: %s' % (self._file_path, error_message))

		# If status is neither approved or elaboration reject reason must be stated
		if (self.status == 'rejected' or self.status == 'postponed') and self.status_reason == '':
			report_error(1, '%s: "Status reason" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is rejected a rejected by user must be specified
		if self.status == 'rejected' and self.rejected_by == None:
			report_error(1, '%s: "Rejected by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

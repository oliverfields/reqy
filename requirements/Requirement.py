# Copyright (c) 2012 - Oliver Fields, oliver@phnd.net
#
# This file is part of Reqy.
#
# Reqy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Reqy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Reqy.  If not, see <http://www.gnu.org/licenses/>.

from ConfigFile import *
import re

class Requirement(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.approved_on = None
		self.approved_by = None
		self.assigned_on = None
		self.assigned_to = None
		self.change_log = None
		self.created_by = None
		self.created_on = None
		self.description = None
		self.depends_on = None
		self.documents = None
		self.estimated_effort = None
		self.estimated_cost = None
		self.note = None
		self.postponed_by = None
		self.postponed_on = None
		self.preconditions = None
		self.priority = 'must'
		self.rationale = None
		self.rejected_by = None
		self.rejected_on = None
		self.delineation = None
		self.status = 'elaboration'
		self.status_reason = None
		self.title = None
		self.todo = None
		self._valid_file_extension = 'req'


	def is_valid_status(self, status):
		if status == 'elaboration' or status == 'rejected' or status == 'implementation' or status == 'postponed' or status == 'approved':
			return True
		else:
			return False


	def is_valid_priority(self, priority):
		if priority == 'must' or priority == 'should' or priority == 'could':
			return True
		else:
			return False


	def validate_settings(self):
		""" All checks to ensure the settings obey the business rules (syntax checks handled by parent class) """

		# Check all attributes exist
		for key, value in vars(self).items():
		  if hasattr(self, key) == False:
				Utility.report_error(1, '%s: Missing attribute "%s"' % (self._file_path, key))

		# Check mandatory attributes
		if self.is_valid_status(self.status) == False:
			Utility.report_error(1, '%s: Status "%s" is not valid' % (self._file_path, self.status))

		if self.is_valid_priority(self.priority) == False:
			Utility.report_error(1, '%s: Priority "%s" is not valid' % (self._file_path, self.priority))

		if self.description == '' or self.description == None:
			Utility.report_error(1, '%s: Description attribute is empty or missing' % (self._file_path))

		if self.rationale == '' or self.rationale == None:
			Utility.report_error(1, '%s: Rationale attribute is empty or missing' % (self._file_path))

		if self.delineation == '' or self.delineation == None:
			Utility.report_error(1, '%s: Delineation attribute is empty or missing' % (self._file_path))

		if self.is_integer(self.estimated_effort) == False and self.is_triple_point_estimate(self.estimated_effort) == False:
			Utility.report_error(1, '%s: Estimated effort field has value "%s", but it must be either an integer or a triple point (best/likely/worst)' % (self._file_path, self.estimated_effort))

		if self.is_integer(self.estimated_cost) == False:
			Utility.report_error(1, '%s: Estimated cost field has value "%s", but it must be an integer' % (self._file_path, self.estimated_cost))

		if self.is_string_date(self.created_on) == False:
			Utility.report_error(1, '%s: Created on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.created_on))

		if self.is_string_date(self.rejected_on) == False:
			Utility.report_error(1, '%s: Rejected on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.rejected_on))

		if self.is_string_date(self.postponed_on) == False:
			Utility.report_error(1, '%s: Postponed on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.postponed_on))

		if self.is_string_date(self.approved_on) == False:
			Utility.report_error(1, '%s: Approved on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.approved_on))

		if self.is_string_date(self.assigned_on) == False:
			Utility.report_error(1, '%s: Assigned on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.assigned_on))

		# Read the link list attributes and re assign string attribute to
		# appropriate list elements
		self.approved_by = self.make_link_list('stakeholders', 'Approved by', self.approved_by, False)
		self.assigned_to = self.make_link_list('stakeholders', 'Assigned to', self.assigned_to, False)
		self.created_by = self.make_link_list('stakeholders', 'Created by', self.created_by, False)
		self.rejected_by = self.make_link_list('stakeholders', 'Rejected by', self.rejected_by, False)
		self.postponed_by = self.make_link_list('stakeholders', 'Postponed by', self.postponed_by, False)
		self.documents = self.make_link_list('documents', 'Documents', self.documents)
		self.depends_on = self.make_link_list('requirements', 'Depends on', self.depends_on)

		# Make change log list array
		self.change_log = self.make_change_log_list(self)

		# If status is neither implementation or elaboration status reason must be stated
		if (self.status == 'rejected' or self.status == 'postponed') and (self.status_reason == '' or self.status_reason == None):
			Utility.report_error(1, '%s: "Status reason" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is rejected a rejected by user must be specified
		if self.status == 'rejected' and (self.rejected_by == None or self.rejected_by == ''):
			Utility.report_error(1, '%s: "Rejected by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is approved a approved_by user must be specified
		if self.status == 'approved' and (self.approved_by == None or self.approved_by == ''):
			Utility.report_error(1, '%s: "Approved by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is postponed a postponed_by user must be specified
		if self.status == 'postponed' and (self.postponed_by == None or self.postponed_by == ''):
			Utility.report_error(1, '%s: "Postponed by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If assigned on, then must have assigned to
		if self.assigned_on and self.assigned_to == None:
			Utility.report_error(1, '%s: Item has "Assigned on" date, but missing "Assigned to" attribute' % self._file_path)

		# Check appropriate by and on attributes for the status
		self.check_appropriate_by_and_on_attributes(self.status, 'approved', self.approved_by, 'Approved by', self.approved_on, 'Approved on')
		self.check_appropriate_by_and_on_attributes(self.status, 'rejected', self.rejected_by, 'Rejected by', self.rejected_on, 'Rejected on')
		self.check_appropriate_by_and_on_attributes(self.status, 'postponed', self.postponed_by, 'Postponed by', self.postponed_on, 'Postponed on')

		# If title attribute not set then set to same as pretty name
		if self.title == None:
			self.title = self._pretty_name

		# Prefix the title if it does not start with numbers and dots, ie _id
		if not re.match('^[0-9.]*\ ', self.title):
			self.title = self._id + ' ' + self.title


	def check_appropriate_by_and_on_attributes(self, actual_status_string, status_string, by_value_string, by_lable_string, on_value_string, on_lable_string):
		if (status_string != actual_status_string) and (by_value_string != None):
			Utility.report_error(1, '%s: Item has attribute %s, but status is not %s' % (self._file_path, by_lable_string, status_string))

		if status_string != actual_status_string and on_value_string != None:
			Utility.report_error(1, '%s: Item has attribute %s, but status is not %s' % (self._file_path, on_lable_string, status_string))


	def display_priority(self):
		""" Get translated priority string """

		if self.priority == 'must':
			string = _('must')
		elif self.priority == 'should':
			string = _('should')
		elif self.priority == 'could':
			string = _('could')

		return string


	def display_status(self):
		""" Get translated status string """

		if self.status == 'elaboration':
			string = _('elaboration')
		elif self.status == 'implementation':
			string = _('implementation')
		elif self.status == 'rejected':
			string = _('rejected')
		elif self.status == 'approved':
			string = _('approved')
		elif self.status == 'postponed':
			string = _('postponed')

		return string

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

class GlossaryTermDefinition(ConfigFile):

	def __init__(self):
		""" Public attributes (those not starting with underscore) are also the valid config file settings """
		ConfigFile.__init__(self)
		self.created_by = None
		self.created_on = None
		self.definition = None
		self.note = None
		self.rejected_by = None
		self.rejected_on = None
		self.replaced_by = None
		self.status = 'elaboration'
		self.status_reason = None
		self.term = None
		self.todo = None
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
				Utility.report_error(1, '%s: Missing attribute "%s"' % (self._file_path, key))

		# Check mandatory attributes
		if self.is_valid_status(self.status) == False:
			Utility.report_error(1, '%s: Status "%s" is not valid' % (self._file_path, self.status))

		if self.definition == '' or self.definition == None:
			Utility.report_error(1, '%s: Definition field is empty or missing' % (self._file_path))
		
		if self.term == '' or self.term == None:
			Utility.report_error(1, '%s: Term field is empty or missing' % (self._file_path))

		# If status is neither approved or elaboration reject reason must be stated
		if (self.status == 'rejected' or self.status == 'replaced') and (self.status_reason == '' or self.status_reason == None):
			Utility.report_error(1, '%s: "Status reason" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is rejected a rejected by user must be specified
		if self.status == 'rejected' and (self.rejected_by == '' or self.rejected_by == None):
			Utility.report_error(1, '%s: "Rejected by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		# If status is replaced then Replaced by must be specified
		if self.status == 'replaced' and (self.replaced_by == None or self.replaced == ''):
			Utility.report_error(1, '%s: "Replaced by" is missing, this is not allowed when status is "%s"' % (self._file_path, self.status))

		self.created_by = self.make_link_list('stakeholders', 'Created by', self.created_by, False)
		self.rejected_by = self.make_link_list('stakeholders', 'Rejected by', self.rejected_by, False)
		self.replaced_by = self.make_link_list('glossary', 'Replaced by', self.replaced_by)

		if self.is_string_date(self.created_on) == False:
			Utility.report_error(1, '%s: Created on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.created_on))

		if self.is_string_date(self.rejected_on) == False:
			Utility.report_error(1, '%s: Rejected on field has value "%s", but it must be date in YYYY-MM-DD format' % (self._file_path, self.rejected_on))



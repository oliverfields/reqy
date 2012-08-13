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

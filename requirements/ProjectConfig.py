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

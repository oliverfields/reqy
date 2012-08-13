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

from Requirement import *

class RequirementPackage(Requirement):
	""" Essentially same as Requirement, but a package is a directory and stores attributes in attributes.pkg file in itself """

	def __init__(self):
		Requirement.__init__(self)
		self._children = []
		self._valid_file_extension = 'pkg'

	def set_name_and_id(self, file_name):
		""" Extract from file name the parent folder name and an optional id prefix and a short name, slightly different from Requirements.set_name_and_id """
		file_name = os.path.basename(os.path.dirname(file_name))
		file_strings = file_name.partition('_')
		# If two last elements are empty the underscore wasn't there
		if file_strings[1] == '' and file_strings[2] == '':
			self._name = file_strings[0]
			self._id = ''
			self._pretty_name = self._name.replace('-', ' ').capitalize()
		else:
			self._name = file_strings[2]
			self._id = file_strings[0]
			self._pretty_name = '%s %s' % (self._id, self._name.replace('-', ' ').capitalize())

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

import Utility
import os 

class Document:
	""" Save info about document """

	def __init__(self):
		self._file_name = None
		self._file_path = None
		self._pretty_name = None

	def load_document(self, path):
		""" Check document exists and assign attribute values """
		if os.path.isfile(path):
			document_repo_path = '%s/documents/' % Utility.get_repo_dir() 
			self._file_name = os.path.basename(path)
			self._file_path = os.path.abspath(path)
			self._pretty_name = path.replace(document_repo_path, '')
		else:
			raise Exception('can not find document "%s"' % path)

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

from Artifact import *
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir
from ..Utility import documents_by_type
import os

class GenRequirementsTraceabilityMatrix(Artifact):
	"""
	Generate csv file format describing the requirements and their deliverables
	"""

	def __init__(self):
		self.name = 'rtm'
		self.description = 'Generate csv file format describing the requirements and their deliverables'


	def get_children_rows(self, parent, csv):
		for item in parent._children:
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				use_case = documents_by_type(item.documents, 'use-case')
				test_case = documents_by_type(item.documents, 'test-case')
				design = documents_by_type(item.documents, 'design')
				code = documents_by_type(item.documents, 'code')
				acceptance_test = documents_by_type(item.documents, 'acceptance-test')

				csv += '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (item._pretty_name,item.status, use_case, design, code, test_case, acceptance_test)

				if item._children:
					csv = self.get_children_rows(item, csv)

		return csv


	def generate(self, target_file):
		"""
		List each requirement and it's deliverables. The deliverables are
		are certain documents that are defined in the documents attribute.
		"""

		repo_dir = get_repo_dir()
		rt = RequirementTree()
		rt.load_repository(repo_dir)

		csv = self.get_children_rows(rt, '')
		
		csv_header = '"Name";"Status";"Use case";"Design";"Code ref";"Test case";"Acceptance test"\n'

		write_file(target_file, csv_header + csv)

from Artifact import *
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir
import os

class GenRequirementsTraceabilityMatrix(Artifact):
	"""
	Generate csv file format describing the requirements and their deliverables
	"""

	def __init__(self):
		self.name = 'rtm'
		self.description = 'Generate csv file format describing the requirements and their deliverables'


	def documents_by_type(self, link_list, document_type):
		""" Returns all items from list that match the filter type """

		file_list = ''

		if link_list == None:
			return file_list 

		for document in link_list:
			if document._pretty_name.startswith(document_type):
				file_list += document._pretty_name + ','

		if file_list.endswith(','):
			file_list.rstrip(',')

		return file_list


	def generate(self, target_file):
		"""
		List each requirement and it's deliverables. The deliverables are
		are certain documents that are defined in the documents attribute.
		"""

		repo_dir = get_repo_dir()
		rt = RequirementTree()
		rt.load_repository(repo_dir)

		csv = '"Name";"Use case";"Design";"Code ref";"Test case";"Acceptance validation";"Complete"\n'

		for item in rt.get_tree_items():
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				use_case = self.documents_by_type(item.documents, 'use-case')
				test_case = self.documents_by_type(item.documents, 'test-case')
				design = self.documents_by_type(item.documents, 'design')
				code = self.documents_by_type(item.documents, 'code')
				acceptance_validation = self.documents_by_type(item.documents, 'acceptance_validation')

				if len(use_case) > 0 and len(test_case) > 0 and len(design) > 0 and len(code) > 0 and len(acceptance_validation) > 0:
					complete = 'Yes'
				else:
					complete = 'No'

				csv += '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (item._pretty_name, use_case, design, code, test_case, acceptance_validation, complete)

		write_file(target_file, csv)

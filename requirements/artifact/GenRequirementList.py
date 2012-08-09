from Artifact import *
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H, P, Span
import os

class GenRequirementList(Artifact):
	"""
	Generate odt file with detailed listing of the requirements
	"""

	def __init__(self):
		self.name = 'overview'
		self.description = 'Generate odt file with detailed listing of the requirements'


	def format_list(self, alist):
		the_list = '' 
		for item in alist:
			the_list += make_path_relative(item._file_path) + ', '

		the_list = the_list.rstrip(', ')

		return the_list


	def write_child_details(self, tree, parent, odt):
		for item in parent._children:
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				use_case = documents_by_type(item.documents, 'use-case')
				test_case = documents_by_type(item.documents, 'test-case')
				design = documents_by_type(item.documents, 'design')
				code = documents_by_type(item.documents, 'code')
				acceptance_test = documents_by_type(item.documents, 'acceptance-test')

				traces = tree.list_direct_traces(item._file_path)

				print ''
				print item._pretty_name
				print '---------------'
				print item.description
				print ''
				print item.rationale
				print ''
				if item.note:
					print 'Note: %s' % item.note
					print ''
				print 'Created by: %s' % xstr(item.created_by)
				print 'Created on: %s' % xstr(item.created_on)
				print 'Assigned to: %s' % xstr(item.assigned_to)
				print 'Assigned on: %s' % xstr(item.assigned_on)
				print 'Rejected by: %s' % xstr(item.rejected_by)
				print 'Rejected on: %s' % xstr(item.rejected_on)
				print ''
				print 'Traces to: %s' % self.format_list(traces['to'])
				print 'Traces from: %s' % self.format_list(traces['from'])
				print ''
				print 'Design: %s' % design
				print 'Test case: %s'	 % test_case
				print 'Use case: %s' % use_case
				print 'Acceptance test: %s' % acceptance_test
				print ''
				print 'Estimated effort: !!!'
				print 'Estimated cost: !!!'
				print ''
				print 'Todo: %s' % item.todo

				if item._children:
					self.write_child_details(tree, item, odt)


	def generate(self, target_file):
		""" List each requirement and it's details """

		repo_dir = get_repo_dir()
		rt = RequirementTree()
		rt.load_repository(repo_dir)
		odt = OpenDocumentText()

		self.write_child_details(rt, rt, odt)

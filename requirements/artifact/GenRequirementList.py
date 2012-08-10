from Artifact import *
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H, P, Span
from odf.table import Table, TableCell, TableRow, TableColumn
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


	def stakeholder_trace(self, prefix_string, trace_string, stakeholder, date):
		""" Print string showing trace to stakeholder and date """
		s = prefix_string
		if stakeholder != None and len(stakeholder) > 0:
			if stakeholder[0].name:
				s += ' %s %s' % (trace_string, stakeholder[0].name)
			if date:
				s += ' on ' + date
		if s == prefix_string:
			s = ''
		return s


	def write_child_details(self, tree, level, parent, odt):
		""" Generate appropriate odt content for each requirement or package """

		# Ensure level is not larger than number of heading styles
		if level > 6:
			level = 6

		for item in parent._children:
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				use_case = documents_by_type(item.documents, 'use-case')
				test_case = documents_by_type(item.documents, 'test-case')
				design = documents_by_type(item.documents, 'design')
				code = documents_by_type(item.documents, 'code')
				acceptance_test = documents_by_type(item.documents, 'acceptance-test')

				traces = tree.list_direct_traces(item._file_path)
				print '%s - %s' % (level, item._pretty_name)

				# Heading
				heading = H(text=item._pretty_name, outlinelevel=level)
				odt.text.addElement(heading)

				# Attribute table
				tbl = Table()
				tbl.addElement(TableColumn(numbercolumnsrepeated='2'))
				odt.text.addElement(tbl)

				# Status
				tr = TableRow()
				tc = TableCell(valuetype='string')
				tc.addElement(P(text='Status'))
				tr.addElement(tc)
				tc = TableCell(valuetype='string')
				tc = TableCell(valuetype='string')
				if item.status_reason:
					tc.addElement(P(text='%s - %s' % (item.status, item.status_reason)))
				else:
					tc.addElement(P(text='%s' % (item.status)))
				tr.addElement(tc)
				tbl.addElement(tr)

				# Description, rationale and notes
				tr = TableRow()
				tc = TableCell(valuetype='string')
				tbl.addElement(tr.addElement(tc.addElement(P(text=item.description))))
				tr = TableRow()
				tc = TableCell(valuetype='string')
				odt.text.addElement(P(text=item.rationale))
				tbl.addElement(tr.addElement(tc.addElement(P(text=item.rationale))))
				if item.note:
					tr = TableRow()
					tc = TableCell(valuetype='string')
					tbl.addElement(tr.addElement(tc.addElement(P(text=item.note))))


				"""
				print ''
				print '%s - %s' % (level, item._pretty_name)
				print '---------------'
				print 'Status: %s' % item.status
				if item.status_reason:
					print 'Status reason: %s' % item.status_reason
				print ''
				print item.description
				print ''
				print item.rationale
				print ''
				if item.note:
					print 'Note: %s' % item.note
					print ''
				print self.stakeholder_trace('Created', 'by', item.created_by, item.created_on)
				print self.stakeholder_trace('Assigned', 'to', item.assigned_to, item.assigned_on)
				print self.stakeholder_trace('Rejected', 'by', item.rejected_by, item.rejected_on)
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
				if item.todo:
					print ''
					print 'Todo: %s' % xstr(item.todo)
				"""

				if item._children:
					self.write_child_details(tree, level+1, item, odt)


	def generate(self, target_file):
		""" List each requirement and it's details """

		repo_dir = get_repo_dir()
		rt = RequirementTree()
		rt.load_repository(repo_dir)
		odt = OpenDocumentText()

		self.write_child_details(rt, 1, rt, odt)

		odt.save(target_file, True)

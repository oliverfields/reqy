from Artifact import *
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr, report_error
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, TableColumnProperties
from odf.text import H, P, List, ListItem
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
			the_list += make_path_relative(item._file_path)

		the_list = the_list.rstrip(', ')

		return the_list


	def stakeholder_trace(self, table, key, trace_string, stakeholder, date):
		""" Print string showing trace to stakeholder and date """
		s = ''
		if stakeholder != None and len(stakeholder) > 0:
			if stakeholder[0].name:
				s += '%s %s' % (trace_string.capitalize(), stakeholder[0].name)
			if date:
				if s == '':
					s = date
				else:
					s += ' on ' + date

		if s != '':
			self.add_attribute_row(table, key, s)


	def add_attribute_row(self, table, key, value):
		""" Add a two cell row to the table """
		tr = TableRow()
		tc = TableCell(valuetype='string')
		tc.addElement(P(text=key))
		tr.addElement(tc)
		tc = TableCell(valuetype='string')
		tc.addElement(P(text=value))
		tr.addElement(tc)
		table.addElement(tr)

	def add_attribute_traces_row(self, table, key, list_items):
		""" Add a two cell row to the table """
		tr = TableRow()
		tc = TableCell(valuetype='string')
		tc.addElement(P(text=key))
		tr.addElement(tc)
		tc = TableCell(valuetype='string')
		tc.addElement(self.build_list(list_items))
		tr.addElement(tc)
		table.addElement(tr)

	def build_list(self, list_items):
		l = List()
		for item in list_items:
			name = ''
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				name = item._pretty_name
			elif isinstance(item, RequirementTree):
				name = 'Root' 
			elif isinstance(item, Document):
				#name = item._pretty_name
				continue
			else:
				name = item

			p = P(text=name)
			i = ListItem()
			i.addElement(p)
			l.addElement(i)

		return l


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
#				s = Style(name="attributenamecolumn", family="table-column")
#				s.addElement(TableColumnProperties(columnwidth="2cm"))
#				odt.automaticstyles.addElement(s)

				tbl = Table()
#				tbl.addElement(TableColumn(numbercolumnsrepeated='1', stylename=s))
#				tbl.addElement(TableColumn(numbercolumnsrepeated='1'))
				tbl.addElement(TableColumn(numbercolumnsrepeated='2'))
				odt.text.addElement(tbl)

				# Status
				status = item.status
				status = status.capitalize()
				if item.status_reason:
					status_string = '%s - %s' % (status, item.status_reason)
				else:
					status_string = '%s' % (status)
				self.add_attribute_row(tbl, 'Status', status_string)

				# Description, rationale and notes
				self.add_attribute_row(tbl, 'Description', item.description)
				self.add_attribute_row(tbl, 'Rationale', item.rationale)

				if item.note:
					self.add_attribute_row(tbl, 'Note', item.note)

				self.stakeholder_trace(tbl, 'Created', 'by', item.created_by, item.created_on)
				self.stakeholder_trace(tbl, 'Assigned', 'to', item.assigned_to, item.assigned_on)
				self.stakeholder_trace(tbl, 'Rejected', 'by', item.rejected_by, item.rejected_on)

				# Traces
				if traces['to']:
					self.add_attribute_traces_row(tbl, 'Dependency to', traces['to'])
				if traces['from']:
					self.add_attribute_traces_row(tbl, 'Dependency from', traces['from'])

				if use_case:
					self.add_attribute_traces_row(tbl, 'Use case', use_case.split(','))
				if design:
					self.add_attribute_traces_row(tbl, 'Design', design.split(','))
				if test_case:
					self.add_attribute_traces_row(tbl, 'Test case', test_case.split(','))
				if acceptance_test:
					self.add_attribute_traces_row(tbl, 'Acceptance test', acceptance_test.split(','))
				
				if item.todo:
					self.add_attribute_row(tbl, 'Todo', item.todo)

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

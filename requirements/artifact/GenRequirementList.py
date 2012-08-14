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
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr, report_error
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, TableColumnProperties, ParagraphProperties
from odf.text import H, P, List, ListItem, Span, TableOfContent, TableOfContentSource
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
		boldstyle = Style(name="Bold",family="text")
		boldstyle.addElement(TextProperties(attributes={'fontweight':"bold"}))

		title_span = Span(stylename=boldstyle, text=key)
		pt = P(text='')
		pt.addElement(title_span)

		tr = TableRow()
		tc = TableCell(valuetype='string')
		tc.addElement(pt)
		tr.addElement(tc)
		tc = TableCell(valuetype='string')
		tc.addElement(P(text=value))
		tr.addElement(tc)
		table.addElement(tr)


	def add_attribute_traces_row(self, table, key, list_items):
		""" Add a two cell row to the table """

		boldstyle = Style(name="Bold",family="text")
		boldstyle.addElement(TextProperties(attributes={'fontweight':"bold"}))

		title_span = Span(stylename=boldstyle, text=key)
		pt = P(text='')
		pt.addElement(title_span)

		tr = TableRow()
		tc = TableCell(valuetype='string')
		tc.addElement(pt)
		tr.addElement(tc)
		tc = TableCell(valuetype='string')
		tc.addElement(self.build_list(list_items))
		tr.addElement(tc)
		table.addElement(tr)


	def add_attribute_document_list_row(self, table, key, list_items):
		""" Add a two cell row to the table """

		boldstyle = Style(name="Bold",family="text")
		boldstyle.addElement(TextProperties(attributes={'fontweight':"bold"}))

		title_span = Span(stylename=boldstyle, text=key)
		pt = P(text='')
		pt.addElement(title_span)

		tr = TableRow()
		tc = TableCell(valuetype='string')
		tc.addElement(pt)
		tr.addElement(tc)
		tc = TableCell(valuetype='string')
		tc.addElement(self.build_document_list(list_items))
		tr.addElement(tc)
		table.addElement(tr)


	def get_dependency_to_items(self, item_list):
		""" Returns list of requirement and requirement package names """
		l = []
		for item in item_list:
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				l.append(item._pretty_name)
			elif isinstance(item, RequirementTree):
				l.append('Root')
			elif isinstance(item, Document):
				continue
			else:
				continue
		return l


	def build_list(self, list_items):
		l = List() 
		for item in self.get_dependency_to_items(list_items):
			p = P(text=item)
			i = ListItem()
			i.addElement(p)
			l.addElement(i)

		return l


	def build_document_list(self, list_items):
		l = List() 
		for item in list_items:
			p = P(text=item)
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

				# Heading
#				if item.status == 'rejected':
#					strikestyle = Style(name="Strike",family="text")
#					strikestyle.addElement(TextProperties(attributes={'strikethrough-position':2}))
#					odt.automaticstyles.addElement(strikestyle)
#					heading_span = Span(stylename=strikestyle, text=item._pretty_name)
#					odt.automaticstyles.addElement(strikestyle)
#					heading = H(text='', outlinelevel=level)
#					heading.addElement(heading_span)
#				else:
#					heading = H(text=item._pretty_name, outlinelevel=level)
				# Create a style for the paragraph with page-break
#				withbreak = Style(name="WithBreak", parentstylename="Standard", family="paragraph")
#				withbreak.addElement(ParagraphProperties(breakbefore="page"))
#				odt.automaticstyles.addElement(withbreak)
#				if level == 1:
#					heading = H(text='%s [%s]' % (item._pretty_name, item.status.capitalize()), outlinelevel=level, stylename=withbreak)
#				else:
				heading = H(text='%s [%s]' % (item._pretty_name, item.status.capitalize()), outlinelevel=level)

				odt.text.addElement(heading)

				tablecontents = Style(name="Table Contents", family="paragraph")
				tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
				odt.styles.addElement(tablecontents)

				# Create automatic styles for the column widths.
				# We want two different widths, one in inches, the other one in metric.
				# ODF Standard section 15.9.1
				widthshort = Style(name="Wshort", family="table-column")
				widthshort.addElement(TableColumnProperties(columnwidth="2cm"))
				odt.automaticstyles.addElement(widthshort)

				widthwide = Style(name="Wwide", family="table-column")
				widthwide.addElement(TableColumnProperties(columnwidth="7cm"))
				odt.automaticstyles.addElement(widthwide)

				# Attribute table

				tbl = Table()
				tbl.addElement(TableColumn(numbercolumnsrepeated='1',stylename=widthshort))
				tbl.addElement(TableColumn(numbercolumnsrepeated='1',stylename=widthwide))
				odt.text.addElement(tbl)

				# Status
				boldstyle = Style(name="Bold",family="text")
				boldstyle.addElement(TextProperties(attributes={'fontweight':"bold"}))
				odt.automaticstyles.addElement(boldstyle)
				p = P(text='')
				status = item.status
				status = status.capitalize()
				status_span = Span(stylename=boldstyle, text=status)
				p.addElement(status_span)

				status_text = ''

				if item.status == 'rejected':
					status_text += ' by ' + item.rejected_by[0]._pretty_name
					if item.rejected_on:
						status_text += ' on ' + item.rejected_on

				if item.status == 'approved':
					status_text += ' by ' + item.approved_by[0]._pretty_name
					if item.approved_on:
						status_text += ' on ' + item.approved_on

				if item.status == 'postponed':
					status_text += ' by ' + item.postponed_by[0]._pretty_name
					if item.postponed_on:
						status_text += ' on ' + item.postponed_on

				if item.status_reason:
					status_text += ' - %s' % item.status_reason

				if status_text != '':
					p.addText(status_text)

				title_span = Span(stylename=boldstyle, text='Status')
				pt = P(text='')
				pt.addElement(title_span)
				tr = TableRow()
				tc = TableCell(valuetype='string')
				tc.addElement(pt)
				tr.addElement(tc)
				tc = TableCell(valuetype='string')
				tc.addElement(p)
				tr.addElement(tc)
				tbl.addElement(tr)

				# Description, rationale and notes
				self.add_attribute_row(tbl, 'Description', item.description)
				self.add_attribute_row(tbl, 'Rationale', item.rationale)

				if item.note:
					self.add_attribute_row(tbl, 'Note', item.note)

				self.stakeholder_trace(tbl, 'Created', 'by', item.created_by, item.created_on)
				self.stakeholder_trace(tbl, 'Assigned', 'to', item.assigned_to, item.assigned_on)

				# Traces
				traces_to = self.get_dependency_to_items(traces['to'])
				if len(traces_to) > 0:
					self.add_attribute_traces_row(tbl, 'Dependency to', traces['to'])
				
				# Will always be a parent, which is enforced by file system, so just show
				self.add_attribute_traces_row(tbl, 'Dependency from', traces['from'])

				if use_case:
					self.add_attribute_document_list_row(tbl, 'Use case', use_case.split(','))
				if design:
					self.add_attribute_document_list_row(tbl, 'Design', design.split(','))
				if test_case:
					self.add_attribute_document_list_row(tbl, 'Test case', test_case.split(','))
				if acceptance_test:
					self.add_attribute_document_list_row(tbl, 'Acceptance test', acceptance_test.split(','))
				
				if item.todo:
					self.add_attribute_row(tbl, 'Todo', item.todo)

				if item._children:
					self.write_child_details(tree, level+1, item, odt)


	def add_toc(self, odt):
		# TOC
		tc = TableOfContent(name="Table of contents")
		tcs = TableOfContentSource()
		tc.addElement(tcs)
		odt.text.addElement(tc)


	def add_title_page(self, odt, title):
		# Requirements for <project name>
		# <project description>
		#
		# Author: <stakeholder name>
		# <date>
		#
		# <document description>
		# Title
		titlestyle = Style(name="TitleStyle",family="text")
		titlestyle.addElement(TextProperties(attributes={'fontweight':"bold", 'fontsize':'36pt'}))
		odt.automaticstyles.addElement(titlestyle)
		titlespan = Span(stylename=titlestyle, text='Requirements for "%s"' % title)
		p = P(text='')
		p.addElement(titlespan)
		odt.text.addElement(p)


	def generate(self, target_file):
		""" List each requirement and it's details """

		repo_dir = get_repo_dir()
		rt = RequirementTree()
		rt.load_repository(repo_dir)
		odt = OpenDocumentText()

		self.add_title_page(odt, rt._pretty_name)
		self.add_toc(odt)
		self.write_child_details(rt, 1, rt, odt)

		try:
			odt.save(target_file, True)
		except:
			report_error(1, 'Unable to write to "%s", is file open?' % target_file)

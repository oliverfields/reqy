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
from ..ProjectConfig import ProjectConfig
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr, report_error
import odf.opendocument
import odf.meta
import odf.dc
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
					s += ' ' + _('on') + ' ' + date

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
				status_text = item.display_status()
				heading_text='%s [%s]' % (item._pretty_name, status_text.capitalize())
				if item.status == 'rejected':
					s = Span(text=heading_text, stylename="Rejected")
				else:
					s = Span(text=heading_text, stylename="Not rejected")

				heading = H(outlinelevel=level)
				heading.addElement(s)

				odt.text.addElement(heading)

				#tablecontents = Style(name="Table Contents", family="paragraph")
				#tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
				#odt.styles.addElement(tablecontents)

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
				status_text = item.display_status()
				status_text = status_text.capitalize()
				status_span = Span(stylename=boldstyle, text=status_text)
				p.addElement(status_span)

				status_text = ''

				if item.status == 'rejected':
					status_text += ' ' + _('by') + ' ' + item.rejected_by[0]._pretty_name
					if item.rejected_on:
						status_text += ' ' + _('on') + ' ' + item.rejected_on

				if item.status == 'approved':
					status_text += ' ' + _('by') + ' ' + item.approved_by[0]._pretty_name
					if item.approved_on:
						status_text += ' ' + _('on') + ' ' + item.approved_on

				if item.status == 'postponed':
					status_text += ' ' + _('by') + ' ' + item.postponed_by[0]._pretty_name
					if item.postponed_on:
						status_text += ' ' + _('on') + ' ' + item.postponed_on

				if item.status_reason:
					status_text += ' - %s' % item.status_reason

				if status_text != '':
					p.addText(status_text)

				title_span = Span(stylename=boldstyle, text=_('Status'))
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

				# Priority
				if item.priority:
					self.add_attribute_row(tbl, _('Priority'), item.display_priority().capitalize())

				# Description, rationale, scope and notes
				self.add_attribute_row(tbl, _('Description'), item.description)
				self.add_attribute_row(tbl, _('Rationale'), item.rationale)
				self.add_attribute_row(tbl, _('Scope'), item.scope)

				if item.note:
					self.add_attribute_row(tbl, _('Note'), item.note)

				self.stakeholder_trace(tbl, _('Created'), _('by'), item.created_by, item.created_on)
				self.stakeholder_trace(tbl, _('Assigned'), _('to'), item.assigned_to, item.assigned_on)


				if item.estimated_effort:
					self.add_attribute_row(tbl, _('Estimated effort'), item.estimated_effort)
				if item.estimated_cost:
					self.add_attribute_row(tbl, _('Estimated cost'), item.estimated_cost)

				# Traces
				traces_to = self.get_dependency_to_items(traces['to'])
				if len(traces_to) > 0:
					self.add_attribute_traces_row(tbl, _('Dependency to'), traces['to'])
				
				# Will always be a parent, which is enforced by file system, so just show
				self.add_attribute_traces_row(tbl, _('Dependency from'), traces['from'])

				if use_case:
					self.add_attribute_document_list_row(tbl, _('Use case'), use_case.split(','))
				if design:
					self.add_attribute_document_list_row(tbl, _('Design'), design.split(','))
				if test_case:
					self.add_attribute_document_list_row(tbl, _('Test case'), test_case.split(','))
				if acceptance_test:
					self.add_attribute_document_list_row(tbl, _('Acceptance test'), acceptance_test.split(','))
				
				if item.todo:
					self.add_attribute_row(tbl, _('Todo'), item.todo)

				if item._children:
					self.write_child_details(tree, level+1, item, odt)


	def add_toc(self, odt):
		# TOC
		tc = TableOfContent(name=_("Table of contents"))
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
		titlespan = Span(stylename=titlestyle, text=_('Requirements for "%s"') % title)
		p = P(text='')
		p.addElement(titlespan)
		odt.text.addElement(p)


	def generate(self, target_file):
		""" List each requirement and it's details """

		repo_dir = get_repo_dir()

		project = ProjectConfig()
		project.load_config_from_file(os.path.join(repo_dir, 'project.conf'))

		rt = RequirementTree()
		rt.load_repository(repo_dir)
		template_file = 'requirement-list-template.odt'

		# If no template found, then create new file
		try:
			template_file_path = os.path.join('templates', template_file)
			template_file_path = os.path.join(repo_dir, template_file_path)
			odt = odf.opendocument.load(template_file_path)
		except Exception as e:
			odt = odf.opendocument.OpenDocumentText()

		#self.add_title_page(odt, rt._pretty_name)
		#self.add_toc(odt)
		#odt.meta.AutoReload(boolean=True)
		if project.name:
			odt.meta.addElement(odf.dc.Title(text=project.name))
		else:
			odt.meta.addElement(odf.dc.Title(text='[Set name in project.conf]'))

		if project.description:
			odt.meta.addElement(odf.dc.Description(text=project.description))
		#try:
		#	odt.meta.addElement(odf.dc.Creator(text=project.project_manager[0].name))
		#except:
		#	pass
		#odt.meta.addElement(odf.dc.Description(text="DESCRIPTION"))
		#odt.meta.addElement(odf.dc.Date(text="1979-05-11"))

		# Add styles
		rejected = Style(name="Rejected", family="text")
		rejected.addElement(TextProperties(color="#666666", textlinethroughstyle="solid"))
		odt.automaticstyles.addElement(rejected)
		notrejected = Style(name="Not rejected", family="text")
		odt.automaticstyles.addElement(notrejected)

		self.write_child_details(rt, 1, rt, odt)

		try:
			odt.save(target_file, True)
		except:
			report_error(1, 'Unable to write to "%s", is file open?' % target_file)

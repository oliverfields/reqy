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
from ..Stakeholder import Stakeholder
from ..Document import Document
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr, report_error
import os
import sys

class GenRequirementListRst(Artifact):
	"""
	Generate odt file with either detailed listing of the requirements or a simple listing
	"""

	def __init__(self, mode):
		self.name = 'overview'
		self.description = 'Generate rst file with detailed or sparse listing of the requirements'
		self.contents = ''

		if mode == "basiclist":
			self._verbose = False
		else:
			self._verbose = True 

		# Set utf-8 as default encoding
		reload(sys)
		sys.setdefaultencoding('utf-8')


	def write_change_logs(self, reqtree):
		""" Get all change log items, sort them by date and output table """

		change_log = []

		for item in reqtree.get_tree_items():
			if isinstance(item, RequirementPackage) or isinstance(item, Requirement):
				if item.change_log:
					for msg in item.change_log:
						change_log.append('* %s %s - %s\n    %s' % (msg['date'], msg['stakeholder'].capitalize(), msg['pretty_name'], msg['message']))

		self.contents += self.basic_heading_markup(1, _('Change log'))

		for msg in sorted(change_log):
			self.contents += '\n' + msg

		self.contents += '\n\n'


	def stakeholder_trace(self, key, trace_string, stakeholder, date):
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
			s = self.attribute_line(key, s)

		return s


	def attribute_documents(self, key, list_items):
		""" Add list of documents """
		docs = ''
		docs = self.build_document_list(list_items)
		return '\n:%s:\n%s\n' % (key, docs)


	def attribute_traces(self, key, list_items):
		""" Add a traces attribute """
		traces = ''
		#title_span = Span(stylename=boldstyle, text=key)
		traces = self.build_list(list_items)
		return '\n:%s:\n%s\n' % (key, traces)


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
		l = '' 
		for item in self.get_dependency_to_items(list_items):
			l += '    * %s\n' % (item)
		return l


	def build_document_list(self, list_items):
		l = '' 
		for item in list_items:
			l += '    * %s\n' % (item)
		return l


	def heading(self, verbose, level, item):
		""" Append markuped heading """
	
		status_text = item.display_status()
		if verbose:
			heading_text='%s [%s]' % (item.title, status_text.capitalize())
		else:
			heading_text='%s' % (item.title)
#		if item.status == 'rejected':
#			heading_text += "Rejected"
#		else:
#			heading_text += "Not Rejected"

		return self.basic_heading_markup(level, heading_text)


	def basic_heading_markup(self, level, heading_text):
		""" Basic rst heading """

		heading_underline = ''

		if level == 1:
			heading_markup = '#'
		elif level == 2:
			heading_markup = '*'
		elif level == 3:
			heading_markup = '='
		elif level == 4:
			heading_markup = '-'
		elif level == 5:
			heading_markup = '^'
		else:
			heading_markup = '"'

		for c in heading_text:
			heading_underline += heading_markup

		return '\n\n\n%s\n%s\n\n' % (heading_text, heading_underline)


	def attribute_line(self, key, value):
		return '\n:%s: %s' % (key, value)


	def write_child_details(self, tree, level, parent):
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

				self.contents += self.heading(self._verbose, level, item)

				# Attributes

				# Status
				if self._verbose:
					status_text = item.display_status()
					status_text = status_text.capitalize()

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
						self.contents += self.attribute_line(_('Status'), status_text)

					# Priority
					if item.priority:
						self.contents +=  self.attribute_line(_('Priority'), item.display_priority().capitalize())

				# Description, rationale, scope and notes
				self.contents += self.attribute_line(_('Description'), item.description)
				if item.rationale != 'none':
					self.contents += self.attribute_line(_('Rationale'), item.rationale)
				if item.scope != 'none':
					self.contents += self.attribute_line(_('Scope'), item.scope)

				if item.note:
					self.contents += self.attribute_line(_('Note'), item.note)

				self.contents += self.stakeholder_trace(_('Created'), _('by'), item.created_by, item.created_on)
				self.contents += self.stakeholder_trace(_('Assigned'), _('to'), item.assigned_to, item.assigned_on)

				if item.estimated_effort:
					self.contents += self.attribute_line(_('Estimated effort'), item.estimated_effort)
				if item.estimated_cost:
					self.contents += self.attribute_line(_('Estimated cost'), item.estimated_cost)

				# Traces
				if self._verbose:
					traces_to = self.get_dependency_to_items(traces['to'])
					if len(traces_to) > 0:
						self.contents += self.attribute_traces(_('Dependency to'), traces['to'])
					
					# Will always be a parent, which is enforced by file system, so just show
					self.contents +=  self.attribute_traces(_('Dependency from'), traces['from'])

					if use_case:
						self.contents += self.attribute_documents(_('Use case'), use_case.split(','))
					if design:
						self.contents += self.attribute_documents(_('Design'), design.split(','))
					if test_case:
						self.contents += self.attribute_documents(_('Test case'), test_case.split(','))
					if acceptance_test:
						self.contents += self.attribute_documents(_('Acceptance test'), acceptance_test.split(','))

				if item._children:
					self.write_child_details(tree, level+1, item)

				if item.change_log:
					rst_text = ''
					for logmsg in item.change_log:
						rst_text += '\n    * %s %s - %s' % (logmsg['date'], logmsg['stakeholder'].capitalize(), logmsg['message'])

					self.contents += self.attribute_line(_('Change log'), rst_text)

				if item.todo:
					self.contents += self.attribute_line(_('Todo') + ' ' + item.todo)


	def add_pagebreak(self):
		self.contents += '\n.. raw:: pdf\n\n    PageBreak\n\n'


	def generate(self, target_file):
		""" List each requirement and it's details """

		repo_dir = get_repo_dir()

		project = ProjectConfig()
		project.load_config_from_file(os.path.join(repo_dir, 'project.conf'))

		rt = RequirementTree()
		rt.load_repository(repo_dir)

		if project.name:
			title = project.name
		else:
			title = '[Set name in project.conf]'

		title_markup = ''
		for c in title:
			title_markup += '='

		self.contents += '%s\n%s\n%s\n\n' % (title_markup, title, title_markup)

		if project.description:
			self.contents += project.description

		self.contents += '\n\n.. header::\n\n    ###Title###\n\n.. footer::\n\n    ###Page###/###Total###'

		self.add_pagebreak()

		self.write_change_logs(rt)

		self.add_pagebreak()

		self.contents += '\n\n.. contents:: ' + _('Table of contents') + '\n\n'

		self.write_child_details(rt, 1, rt)

		write_file(target_file+'.rst', self.contents)

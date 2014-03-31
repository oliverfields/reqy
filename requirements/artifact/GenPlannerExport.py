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
from ..Stakeholder import Stakeholder
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr, report_error
from xml.sax import saxutils
import os
import time

class GenPlannerExport(Artifact):
	"""
	Export requirements, requirement packages and stakeholders to gnome planner.
	Intended only for one way export.
	"""

	def __init__(self):
		self.name = 'planner'
		self.description = 'Export requirements, requirement packages and stakeholders to gnome planner. Intended only for one way export'


	def generate(self, target_file):
		""" Export requirements, packages and stakeholders to planner file """
		now = time.localtime()
		timestamp = time.strftime("%Y%m%dT00000Z")

		repo_dir = get_repo_dir()

		rt = RequirementTree()
		rt.load_repository(repo_dir)

		if rt._pretty_name:
			project_name = rt._pretty_name
		else:
			project_name = '[Set name in project.conf]'

		tasks='<tasks>'

		counter = 1
		for item in rt.get_tree_items():
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				# Planner work is specified in seconds, reqy is shockingly less
				# granular at a whopping hour, so convert it
				if isinstance(item.estimated_effort, int) == True and item.estimated_effort > 0:
					effort=int(item.estimated_effort) * 3600
				else:
					effort=0
				name=item._name.replace('-', ' ')
				name=name.capitalize()
				planner_note = saxutils.quoteattr("Reqy requirement ref: " + item._id + "\n\n" + item.description + "\n\n" + item.rationale + "\n\n" + item.delineation)
				tasks+='<task id="%s" name="%s" note=%s work="%s" start="%s" end="%s" />\n' % (counter, name, planner_note, effort, timestamp, timestamp)
				counter+=1
		tasks+='</tasks>'

		# Get stakeholders
		resources='\n<resources>'
		stakeholder_dir = os.path.join(repo_dir, 'stakeholders')
		stakeholders = os.listdir(stakeholder_dir)
		counter = 0
		for config_file_name in stakeholders:
			config_file_path = os.path.join(stakeholder_dir, config_file_name)
			stakeholder = Stakeholder()
			short_name=config_file_name.rstrip('.sth')
			stakeholder.load_config_from_file(config_file_path)
			resources+='\n<resource id="%s" name="%s" short-name="%s" type="1" units="0" email="%s" note="" />' % (counter, stakeholder.name, short_name, stakeholder.email)
			counter+=1
		resources+='\n</resources>'

		contents='<?xml version="1.0"?>\n<project name="%s" project-start="%s" mrproject-version="2">' % (project_name, timestamp)
		contents+=tasks
		contents+=resources
		contents+='\n</project>'

		write_file(target_file, contents)

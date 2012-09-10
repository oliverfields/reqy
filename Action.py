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
from requirements import Requirement
from requirements.Utility import get_repo_dir
from requirements.Utility import report_error
from requirements.Utility import report_notice
from requirements.Utility import make_path_relative
from shutil import copyfile
import os

def get_parent_dir(item_path):
	parent_dir = item_path.rsplit(os.sep, 1)
	return parent_dir[0]

def new_item(item_type, item_path):
	repo_dir = get_repo_dir()
	item_settings = {
		'glossary': { 'directory': 'glossary', 'file_ext': '.def', 'template_file': 'glossary.def' },
		'package': { 'directory': 'requirements', 'file_ext': '.pkg', 'template_file': 'attributes.pkg' },
		'requirement': { 'directory': 'requirements', 'file_ext': '.req', 'template_file': 'requirement.req' },
		'stakeholder': { 'directory': 'stakeholders', 'file_ext': '.sth', 'template_file': 'stakeholder.sth' },
	}

	valid_item_type = False
	for key in item_settings.items():
		if item_type == key[0]:
			valid_item_type = True

	if valid_item_type == False:
		report_error(1, 'Unknown type "%s"' % item_type)

	if item_path.endswith(os.sep):
		report_error(1, 'Cannot specify directory as new item (trailing "/")')

	# Make path absolute if not
	cwd = os.getcwd()
	# If not a absolute path, then make it one based on cwd
	if item_path.startswith(os.sep) == False:
		item_path = os.path.join(cwd, item_path)

	# Check item is in repo/requirement dir
	if item_path.startswith(repo_dir) == False:
		report_error(1, 'Item must be created in "%s"' % repo_dir)

	file_name = os.path.basename(item_path)
	if file_name == '':
		report_error(1, 'Cannot create %s with no name')

	# Chop off item type directory if user supplied it, gets added later
	if item_path.startswith(item_settings[item_type]['directory']):
		item_path = item_path[len(item_settings[item_type]['directory']):]
		item_path = item_path.lstrip(os.sep)

	# If package add package attribute.pkg
	if item_type == 'package':
		if item_path.endswith('attributes.pkg') == False:
			item_path = os.path.join(item_path, 'attributes.pkg')
	elif item_path.endswith(item_settings[item_type]['file_ext']) == False:
		item_path += item_settings[item_type]['file_ext']

	parent_directory = get_parent_dir(item_path)

	abs_path = os.path.join(parent_directory, item_path)

	# Package is is a directory/attributes.pkg so check differently
	if item_type == 'package':
		if os.path.isdir(item_path):
			report_error(1, 'The package "%s" already exists' % parent_directory)
		else:
			try:
				os.mkdir(parent_directory)
			except:
				report_error(1, 'Unable to create package directory "%s"' % parent_directory)
	else:
		if os.path.isdir(parent_directory) == False:
			report_error(1, 'Directory "%s" does not exist' % parent_directory)

	if os.path.isfile(abs_path):
		report_error(1, 'The file "%s" already exists' % abs_path)

	# Check template exists
	template_file = os.path.join(repo_dir, 'templates', item_settings[item_type]['template_file'])
	if os.path.isfile(template_file) == False:
		report_error(1, 'Unable to find template "%s"' % template_file)

	# All is well, lets create new item by copying appropriate template
	try:
		copyfile(template_file, abs_path)
	except:
		report_error(1, 'Unable to copy template "%s" to "%s"' % (template_file, abs_path))


def list_direct_traces(item_file_path):
	"""
	For item, list direct traces to and from (i.e. indirect traces are not shown)
	"""

	from requirements import RequirementTree

	repo_dir = get_repo_dir()
	rt = RequirementTree.RequirementTree()
	rt.load_repository(repo_dir)

	# If not absolute path, add repo dir
	if item_file_path.startswith(os.sep) == False:
		item_file_path = os.path.join(repo_dir, item_file_path)

	# If package, add attributes.pkg
	if os.path.isdir(item_file_path):
		item_file_path = os.path.join(item_file_path, 'attributes.pkg')

	# Check item exists in tree
	if rt.is_item(item_file_path) == False:
		report_error(1, 'The item "%s" was not found in the repository' % item_file_path)

	# Loop over dependencies and compile list of dependencies to and from item
	# List direct traces to the item
	from_list = []
	to_list = []
	for item in rt.get_dependencies():
		if item[0]._file_path == item_file_path:
			to_list.append(item[1])
		elif item[1]._file_path == item_file_path:
			from_list.append(item[0])

	if from_list:
		print '\n  Traces from "%s" (%s):' % (make_path_relative(item_file_path), len(from_list))
		for item in from_list:
			print '    %s' % make_path_relative(item._file_path)
	else:
		print '\n  No traces from "%s"' % make_path_relative(item_file_path)

	if to_list:
		print '\n  Traces to "%s" (%s):' % (make_path_relative(item_file_path), len(to_list))
		for item in to_list:
			print '    %s' % make_path_relative(item._file_path)
	else:
		print '\n  No traces to "%s"' % make_path_relative(item_file_path)


def build_artifacts(artifact_name):
	from requirements import ProjectConfig 
	from requirements.artifact import GenDotGraph
	from requirements.artifact import GenRequirementsTraceabilityMatrix
	from requirements.artifact import GenRequirementList
	from requirements.artifact import GenEstimation
	from requirements.artifact import GenPlannerExport

	artifact_dir = os.path.join(get_repo_dir(), 'artifacts')

	project = ProjectConfig()
	project.load_config_from_file(os.path.join(get_repo_dir(), 'project.conf'))

	if project.short_name:
		short_name = '%s_' % project.short_name
	else:
		short_name = ''

	if artifact_name == 'estimate' or artifact_name == 'all':
		target_file = os.path.join(artifact_dir, '%sproject-estimation' % short_name)
		report = GenEstimation.GenEstimation()
		report.generate(target_file)

	if artifact_name == 'graph' or artifact_name == 'all':
		target_file = os.path.join(artifact_dir, '%soverview_graph.dot' % short_name)
		graph = GenDotGraph.GenDotGraph()
		graph.generate(target_file)

	if artifact_name == 'rtm' or artifact_name == 'all':
		target_file = os.path.join(artifact_dir, '%srequirements-traceability-matrix.csv' % short_name)
		rtm = GenRequirementsTraceabilityMatrix.GenRequirementsTraceabilityMatrix()
		rtm.generate(target_file)

	if artifact_name == 'list' or artifact_name == 'all':
		target_file = os.path.join(artifact_dir, '%srequirement-list' % short_name)
		list_report = GenRequirementList.GenRequirementList()
		list_report.generate(target_file)

	if artifact_name == 'planner' or artifact_name == 'all':
		target_file = os.path.join(artifact_dir, '%sexport.planner' % short_name)
		export = GenPlannerExport.GenPlannerExport()
		export.generate(target_file)

	if artifact_name != 'all' and artifact_name != 'graph' and artifact_name != 'rtm' and artifact_name != 'list' and artifact_name != 'estimate' and artifact_name != 'planner':
		report_error(1, 'Unknown artifact type "%s"' % artifact_name)


def filter_requirements_by_status(not_equals, status):
	valid_status = ['approved', 'elaboration', 'implementation', 'postponed', 'rejected']
	is_valid_status = False
	# Check status is valid
	for vs in valid_status:
		if vs == status:
			is_valid_status = True

	if is_valid_status == False:
		report_error(1, 'Unknown status "%s", must be either approved, elaboration, implementation, rejected or postponed' % status)

	from requirements import RequirementTree
	from requirements import Requirement
	from requirements import RequirementPackage

	repo_dir = get_repo_dir()
	rt = RequirementTree.RequirementTree()
	rt.load_repository(repo_dir)

	item_list = rt.get_tree_items()

	for item in item_list:
		if isinstance(item, Requirement.Requirement) or isinstance(item, RequirementPackage.RequirementPackage):
			if not_equals == False:
				if item.status != status:
					print "%s (%s)" % (item._pretty_name, item.status.capitalize())
			else:
				if item.status == status:
					print item._pretty_name


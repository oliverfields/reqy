from requirements import Requirement
from requirements.Utility import get_repo_dir
from requirements.Utility import report_error
from requirements.Utility import report_notice
from shutil import copyfile
import os

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

	# Set target path. Path must be relative (i.e. not starting with '/').
	# If not starts with type directory (e.g. requierments or documents) this
	# will be added to the item path. Item name will be suffixed with
	# appropriate file extension is none present.
	if item_path.startswith(os.sep):
		report_error(1, 'Cannot specify absolute path to new item, must be relative to repository root directory')

	if item_path.endswith(os.sep):
		report_error(1, 'Cannot specify directory as new item (trailing "/"')

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

	parent_directory = os.path.join(repo_dir, item_settings[item_type]['directory'])
	abs_path = os.path.join(parent_directory, item_path)

	# Package is is a directory/attributes.pkg so check differently
	if item_type == 'package':
		if os.path.isdir(parent_directory):
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

	# Check item exists in tree
	if rt.is_item(item_file_path) == False:
		report_error(1, 'The item "%s" was not found in the repository' % item_file_path)
	# List direct traces to the item
	# Make function list_traces_from and list_traces_to in tree class and use them here

	# List direct traces from the item
#	print 'item_path: %s' % item_file_path
#	print 'item_file_path abs path: %s' % os.path.join(repo_dir, item_file_path)

	# Loop over and pick out the ones matching the dependency criteria
	#for item in item_list:
	#	print item

def build_artifacts(artifact_name):
	from requirements.artifact import GenDotGraph

	artifact_dir = os.path.join(get_repo_dir(), 'artifacts')

	if artifact_name == 'graph':
		target_file = os.path.join(artifact_dir, 'overview_graph.dot')
		graph = GenDotGraph.GenDotGraph()
		graph.generate(target_file)


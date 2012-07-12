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

	if item_path.startswith(item_settings[item_type]['directory']) == False:
		item_path = os.path.join(item_settings[item_type]['directory'], item_path)

	# If package add package attribute.pkg
	if item_type == 'package':
		if item_path.endswith('attributes.pkg') == False:
			item_path = os.path.join(item_path, 'attributes.pkg')
	elif item_path.endswith(item_settings[item_type]['file_ext']) == False:
		item_path += item_settings[item_type]['file_ext']

	parent_directory = os.path.join(repo_dir, os.path.dirname(item_path))
	abs_path = os.path.join(parent_directory, file_name)

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

def list_dependencies(dependency_direction, item_name):
	"""
	For each requirement or requirement package, check if dependency to target
	requirement, requirement package or document is either to, from or none 
	"""

	'''
to:
each req that has a dependency to item, in addition all dependencies to the req

from:
earch item that the item links to

none:
each item that does not link to item

Basically to and none are opposites and from is easy to do
'''

	from requirements import RequirementTree

	repo_dir = get_repo_dir()
	rt = RequirementTree.RequirementTree()
	rt.load_repository(repo_dir)
	item_list = rt.get_tree_items()
	matched_items = []

	print 'item_name: %s' % item_name
	print 'item_name abs path: %s' % os.path.join(repo_dir, item_name)
	print 'dependency direction: %s' % dependency_direction

	# Loop over and pick out the ones matchin the dependency criteria
	for item in item_list:
		print item

def build_artifacts(repository_directory):
	print repository_directory

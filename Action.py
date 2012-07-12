from requirements import Requirement
from requirements.Utility import get_repo_dir
from requirements.Utility import report_error
from requirements.Utility import report_notice
import os

def new_item(item_type, item_path):
	repo_dir = get_repo_dir()
	item_settings = {
		'glossary': { 'directory': 'glossary', 'file_ext': '.def' },
		'requirement': { 'directory': 'requirements', 'file_ext': '.req' },
		'package': { 'directory': 'requirements', 'file_ext': '.pkg' },
	}

	# Set target path. Path must be relative (i.e. not starting with '/').
	# If not starts with type directory (e.g. requierments or documents) this
	# will be added to the item path. Item name will be suffixed with
	# appropriate file extension is none present.
	if item_path.startswith(os.sep):
		report_error(1, 'Cannot specify absolute path to new item, must be relative to repository root directory')

	if item_path.startswith(item_settings[item_type]['directory']) == False:
		item_path = os.path.join(item_settings[item_type]['directory'], item_path)

	if item_path.endswith(item_settings[item_type]['file_ext']) == False:
		item_path = item_path.join(item_settings[item_type]['file_ext'])

	print item_type
	print item_settings[item_type]
	print item_path

def list_dependency(dependency_direction, item_name):
	print dependency_direction
	print item_name

def build_artifacts(repository_directory):
	print repository_directory

def run_report(report_name):
	print report_name
	req = Requirement.Requirement()

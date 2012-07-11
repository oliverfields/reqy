from requirements import Requirement

def new_item(item_type, item_name):
	print item_type
	print item_name

def list_dependency(dependency_direction, item_name):
	print dependency_direction
	print item_name

def build_artifacts(repository_directory):
	print repository_directory

def run_report(report_name):
	print report_name
	req = Requirement.Requirement()

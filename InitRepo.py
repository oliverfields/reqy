import sys
import os

def report_error(code, message):
	sys.stderr.write('Error: %s\n' % message)
	sys.exit(code)

def get_repo_dir():
	"""
	!!! Ugly Ugly, this function is verbatim copy almost of one in requirements/Utility !!!

	Find the repository root directory. If not the current dir, search
	parent directories until find project.conf. If can't determine repository
	root directory then fail.
	"""
	cwd = os.getcwd()
	dirs = cwd.split(os.sep)
	# Remove first item (the root directory)
	dirs.pop(0)

	while len(dirs) > 0:
		check_dir = ''
		for a_dir in dirs:
			check_dir += os.sep + a_dir
		for a_file in os.listdir(check_dir):
			if a_file == 'project.conf':
				return check_dir
		dirs.pop()

	# Didn't find any repository so failing
	return False

def init_repo():
	# Check if already a repo here
	existing_repo_dir = get_repo_dir()
	if existing_repo_dir:
		report_error(1, 'Current directory already is a repository (root is %s)' % existing_repo_dir)

	if os.listdir(os.getcwd()) != []:
		report_error(1, 'Current directory must be empty before initializing repository')

	dirs = ['documents', 'documents%sdesign' % os.sep, 'documents%suse-case' % os.sep, 'documents%stest-case' % os.sep, 'documents%sacceptance-test' % os.sep, 'glossary', 'requirements', 'stakeholders', 'templates']

	files = [
		['templates', 'attributes.pkg', ''],
		['templates', 'glossary.def', ''],
		['templates', 'requirement.req', ''],
		['templates', 'stakeholder.sth', ''],
		['', 'project.conf', 'Name: Requirements for project X'],
	]

	try:
		# Make directories
		for a_dir in dirs:
			os.mkdir(a_dir)

		# Make files
		for a_file in files:
			with open(os.path.join(a_file[0], a_file[1]), 'w') as f:
				f.writelines(a_file[2])

	except Exception:
		cwd = os.getcwd()
		report_error(1, 'Failed to create files and directories in "%s"' % cwd)

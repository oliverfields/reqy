''' General utility library '''

import sys

def get_repo_dir():
	"""
	Find the repository root directory. If not the current dir, search
	parent directories until find .reqy. If can't determine directory then fail.
	"""
	return "/home/oliver/Documents/projects/reqy/lab/reqy/requirements/unittests/test_data/sample-repository"

def report_error(code, message):
	sys.stderr.write('Error: %s\n' % message)
	sys.exit(code)

def report_warning(message):
	print 'Warning: %s' % message

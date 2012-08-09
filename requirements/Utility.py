''' General utility library '''
import sys
import os

def get_repo_dir():
	"""
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
	report_error(1, 'Not a repository directory (or any of the parent directories)')

def find_repository_root_dir(directory):
	repo_dir = False

	try:
		# project.conf not found and not in root check parent directory
		if repo_dir == False:
			if os.path.realpath(directory) == '/':
				return False
			else:
				find_repository_root_dir(os.path.abspath(os.path.join(directory, os.path.pardir)))
		else:
			return repo_dir

	except Exception as e:
		print sys.exc_info()
		report_error(1, 'Failure reading "%s"' % directory)

def report_error(code, message):
	sys.stderr.write('Error: %s\n' % message)
	sys.exit(code)

def report_warning(message):
	print 'Warning: %s' % message

def report_notice(message):
	print 'Notice: %s' % message

def wrap_line(line, wrap_on_word=7, wrap_string='\n' ,wrap_first=False):
	""" Replace every nth space with a newline, optoinally also wrap first space """
	wrapped_lines = ''

	if wrap_first:
		n = wrap_on_word
	else:
		n = 0

	words = line.split()
	for word in words:
		wrapped_lines += word
		if n == wrap_on_word:
			wrapped_lines += wrap_string
			n = 1
		else:
			wrapped_lines += ' '
			n += 1

	wrapped_lines = wrapped_lines.strip()

	return wrapped_lines


def write_file(file_name, file_content):
	try:
		f = open(file_name, 'w')
		try:
			f.write(file_content)
		finally:
			f.close()
	except IOError:
		report_error(1, 'Unable to write file "%s"' % file_name)


def documents_by_type(link_list, document_type):
	""" Returns all items from list that match the filter type """

	file_list = ''

	if link_list == None:
		return file_list 

	for document in link_list:
		if document._pretty_name.startswith(document_type):
			file_list += document._pretty_name + ','

	if file_list.endswith(','):
		file_list.rstrip(',')

	return file_list


def make_path_relative(path):
	""" Strip repo directories from path """
	repo_dir = get_repo_dir()

	if path == repo_dir:
		return 'root'
	else:
		path = path.replace(get_repo_dir()+'/', '')
		if path.endswith('attributes.pkg'):
			path = path.replace(os.sep+'attributes.pkg', '')
		return path

def xstr(s):
	""" Retrurn None as empty string """
	if s is None:
		return ''
	else:
		return str(s)


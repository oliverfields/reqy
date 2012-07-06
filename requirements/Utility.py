''' General utility library '''

import sys

def report_error(code, message):
	sys.stderr.write('Error: %s\n' % message)
	sys.exit(code)

def report_warning(message):
	print 'Warning: %s' % message

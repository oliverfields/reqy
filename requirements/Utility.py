''' General utility library '''

import sys

def report_error(code, message):
	print 'Error: %s' % message
	sys.exit(code)

def report_warning(message):
	print 'Warning: %s' % message

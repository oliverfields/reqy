from Requirement import *

cf = Requirement()
cf.load_config_from_file('unittests/test_data/requirement_config.req')

for setting in cf.valid_settings.keys():
	if hasattr(cf, str(setting)):
		print 'Setting "%s" has value "%s"' % (setting, getattr(cf, str(setting)))
print 'Todo "%s"' % cf.assigned_to
'''
if cf.assigned_on == '':
	print 'yay'

print cf.assigned_on
'''

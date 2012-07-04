from Requirement import *

cf = Requirement()
cf.load_config_from_file('unittests/test_data/invalid_requirement_config_1.req')

for setting in cf.valid_settings.keys():
	if hasattr(cf, str(setting)):
		print 'Setting "%s" has value "%s"' % (setting, getattr(cf, str(setting)))

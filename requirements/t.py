from Requirement import *

cf = Requirement()
cf.load_config_from_file('unittests/test_data/requirement_config.req')

for setting in vars(cf).keys():
	if hasattr(cf, setting):
		print 'Setting "%s" has value "%s"' % (setting, getattr(cf, setting))

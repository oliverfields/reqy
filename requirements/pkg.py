from RequirementPackage import *

rp = RequirementPackage()
rp.load_config_from_file('unittests/test_data/sample-repository/2_pkg/attributes.pkg')

for setting in vars(rp).keys():
	if hasattr(rp, setting):
		print 'Setting "%s" has value "%s"' % (setting, getattr(rp, setting))

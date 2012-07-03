from ConfigFile import *

cf = ConfigFile()
cf.load_config_from_file('test_data')
if cf.assigned_on == '':
	print 'yay'

print cf.assigned_on

from Requirement import *

cf = Requirement()
cf.load_config_from_file('unittests/test_data/sample-repository/3_r.req')
cf.dump_attributes()

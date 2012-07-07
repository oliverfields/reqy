from Requirement import *

cf = Requirement()
#cf.load_config_from_file('unittests/test_data/sample-repository/requirements/3_r.req')
#cf.load_config_from_file('unittests/test_data/invalid_requirement_config_4.req')
cf.load_config_from_file('unittests/test_data/requirement_config_11.req')
cf.dump_attributes()


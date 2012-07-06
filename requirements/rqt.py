from RequirementTree import *

rt = RequirementTree()
rt.load_repository('unittests/test_data/sample-repository')
#rt.dump_attributes()

rt.print_tree()

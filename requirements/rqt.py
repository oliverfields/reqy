from RequirementTree import *

rt = RequirementTree()
rt.load_repository('unittests/test_data/sample-repository')
rt.dump_attributes()

for item in rt.requirements:
	print '-------'
	item.dump_attributes()
	print
	print

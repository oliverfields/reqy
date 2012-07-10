from RequirementTree import *

rt = RequirementTree()
rt.load_repository('unittests/test_data/sample-repository')
#rt.dump_attributes()

#rt.print_tree()

#print rt._dependency_from_to
for item in rt._dependency_from_to:
	print '%s,%s' % (item[0], item[1])
#print rt._item_list

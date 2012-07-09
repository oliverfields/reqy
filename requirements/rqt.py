from RequirementTree import *

rt = RequirementTree()
rt.load_repository('unittests/test_data/sample-repository')
#rt.dump_attributes()

#rt.print_tree()

print rt._dependency_from_to
#print rt._item_list

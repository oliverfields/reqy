from RequirementTree import *

rt = RequirementTree()
rt.load_repository('unittests')
rt.dump_attributes()

#deps = rt.get_dependencies()

#for item in rt.get_tree_items():
#	print item

#print 'xxxxxxxxxxxxxxxxxxxxx'

#for item in rt.get_dependencies():
#	print item

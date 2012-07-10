from RequirementTree import *


repo = 'unittests/test_data/sample-repository'
rt = RequirementTree()
rt.load_repository(repo)
#rt.dump_attributes()

print 'digraph reqy {'
print 'root="%s"' % repo
print 'graph [ fontname=Verdana, fontsize=12]'
print 'node [ fontname=Verdana, fontsize=10]'
print 'edge [ fontname=Verdana, fontsize=8, color="#666666"]'
print ''


for item in rt.get_tree_items():
	if isinstance(item, RequirementTree):
		print '"%s" [ label="Project: %s", shape="box", color="grey", style="filled", fillcolor="lightgrey"]' % (item._file_path, item._pretty_name)
	elif isinstance(item, RequirementPackage):
		print '"%s" [ label="Package: %s", color="grey", shape="box", style="rounded,filled", fillcolor="lightgrey"]' % (item._file_path, item._pretty_name)
	elif isinstance(item, Requirement):
		print '"%s" [ label="Requirement: %s", color="grey", style="filled", fillcolor="lightgrey"]' % (item._file_path, item._pretty_name)
	elif isinstance(item, Document):
		print '"%s" [ label="Reference: %s", color="lightgrey"]' % (item._file_path, item._pretty_name)
	else:
		report_error(1, 'Unknown item type "%s"' % item)

print ''

for item in rt.get_dependencies():
	print '"%s"->"%s" [dir="back"]' % (item[0]._file_path, item[1]._file_path)

print '}'

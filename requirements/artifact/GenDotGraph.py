from Artifact import *
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir
import os

class GenDotGraph(Artifact):
	"""
	Generate dot file format describing the repository graph, for use with dot command
	"""

	def __init__(self):
		self.name = 'graph'
		self.description = 'Generate a graph of the repository in dot file format'

	def generate(self, target_file):
		repo_dir = get_repo_dir()
		rt = RequirementTree()
		rt.load_repository(repo_dir)
		
		print 'digraph reqy {'
		print 'root="%s"' % repo_dir
		print 'graph [ fontname=Verdana, fontsize=8]'
		print 'node [ fontname=Verdana, fontsize=8]'
		print 'edge [ fontname=Verdana, fontsize=8, color="#707792"]'
		print ''
		
		for item in rt.get_tree_items():
			if isinstance(item, RequirementTree):
				print '"%s" [ label="%s", shape="box", color="#716eb1", style="filled", fillcolor="#9e9bd1"]' % (item._file_path, item._pretty_name)
			elif isinstance(item, RequirementPackage):
				print '"%s" [ label="%s", color="#6ca59c", shape="box", style="rounded,filled", fillcolor="#99c8c2"]' % (item._file_path, item._pretty_name)
			elif isinstance(item, Requirement):
				print '"%s" [ label="%s", color="#7dd396", style="filled", fillcolor="#a9e6bd"]' % (item._file_path, item._pretty_name)
			elif isinstance(item, Document):
				print '"%s" [ label="%s", color="#a9e6bd" ]' % (item._file_path, item._pretty_name)
			else:
				report_error(1, 'Unknown item type "%s"' % item)
		
		print ''
		
		for item in rt.get_dependencies():
			print '"%s"->"%s" [dir="back"]' % (item[0]._file_path, item[1]._file_path)
		print '}'

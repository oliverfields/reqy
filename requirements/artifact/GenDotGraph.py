from Artifact import *
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir
from ..Utility import wrap_line
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
		word_wrap_length = 3
		contents = ''

		contents = '''digraph reqy {
root="%s"
aspect=2
graph [fontname=Verdana, fontsize=8]
node [fontname=Verdana, fontsize=8]
edge [fontname=Verdana, fontsize=8, color="#707792"]

''' % (repo_dir)

		
		for item in rt.get_tree_items():
			if isinstance(item, RequirementTree):
				contents += '"%s" [label="%s", shape="box", color="#716eb1", style="filled", fillcolor="#9e9bd1"]\n' % (item._file_path, item._pretty_name)
			elif isinstance(item, RequirementPackage):
				contents += '"%s" [label="%s", color="#6ca59c", shape="box", style="rounded,filled", fillcolor="#99c8c2"]\n' % (item._file_path, wrap_line(item._pretty_name, word_wrap_length, r'\n', True))
			elif isinstance(item, Requirement):
				contents += '"%s" [label="%s", color="#7dd396", style="filled", fillcolor="#a9e6bd"]\n' % (item._file_path, wrap_line(item._pretty_name, word_wrap_length, r'\n', True))
			elif isinstance(item, Document):
				contents += '"%s" [label="%s", color="#a9e6bd"]\n' % (item._file_path, item._pretty_name)
			else:
				report_error(1, 'Unknown item type "%s"' % item)
		
		contents += '\n'
		
		for item in rt.get_dependencies():
			contents += '"%s"->"%s" [dir="back"]\n' % (item[0]._file_path, item[1]._file_path)
		contents += '}'

		write_file(target_file, contents)

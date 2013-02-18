# Copyright (c) 2012 - Oliver Fields, oliver@phnd.net
#
# This file is part of Reqy.
#
# Reqy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Reqy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Reqy.  If not, see <http://www.gnu.org/licenses/>.

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

"%s" [label="%s", shape="box", color="#716eb1", style="filled", fillcolor="#9e9bd1"]

''' % (repo_dir, rt._file_path, rt._pretty_name)

		
		for item in rt.get_tree_items():
			if isinstance(item, RequirementPackage):
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

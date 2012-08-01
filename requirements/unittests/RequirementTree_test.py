from ..RequirementTree import *
import pytest
import os

class TestRequirementTree():
	'''Unit tests'''

	def test_sample_repo_load(self):
		tree = RequirementTree()
		tree.load_repository('.')
		assert tree._pretty_name == 'Here for unit testing'

	def test_list_direct_traces(self):
		cwd = os.getcwd()
		tree = RequirementTree()
		tree.load_repository(cwd)

		assert tree.is_item(os.path.join(cwd, 'requirements/3_r.req')) == True
		assert tree.is_item(os.path.join(cwd, 'requirements/1_pkg')) == True 
		assert tree.is_item(os.path.join(cwd, 'requirements/1_pkg/')) == True 
		assert tree.is_item(os.path.join(cwd, 'requirements/1_pkg/attributes.pkg')) == True
		assert tree.is_item(os.path.join(cwd, 'requirements/not-exist')) == False

from ..RequirementTree import *
import pytest

class TestRequirementTree():
	'''Unit tests'''

	def test_sample_repo_load(self):
		tree = RequirementTree()
		tree.load_repository('requirements/unittests/test_data/sample-repository')


from ..RequirementPackage import *
import pytest

class TestRequirement():
	'''Unit tests'''

	def test_file_nameing(self):
		pkg = RequirementPackage()
		pkg.set_name_and_id('/a/directory/hiearachy/2_pkg/attributes.pkg')
		assert pkg._name == 'pkg'
		assert pkg._id == '2'
		assert pkg._pretty_name == '2 Pkg'

	def test_valid_pkg_config(self):
		pkg = RequirementPackage()
		pkg.load_config_from_file('requirements/unittests/test_data/test-package/attributes.pkg')
		assert pkg.assigned_on == '2012-07-04'
		assert len(pkg.assigned_to)== 1
		assert len(pkg.created_by) == 1
		assert pkg.created_on == '2012-07-04'
		assert pkg.description == 'Nice requirement for testing with'
		assert pkg.depends_on == None 
		assert pkg.documents == None
		assert pkg.estimated_effort == '400'
		assert pkg.estimated_cost == '15000'
		assert pkg.note == 'A quick note'
		assert pkg.rationale == 'The why is paramount'
		assert len(pkg.rejected_by) == 1
		assert pkg.status == 'implementation'
		assert pkg.status_reason == 'Not really'
		assert pkg.todo == '- Write tests'
		assert pkg._name == 'test-package'
		assert pkg._id == ''
		assert pkg._pretty_name == 'Test package'
		assert pkg._file_name == 'attributes.pkg'

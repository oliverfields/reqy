from ..RequirementPackage import *
import pytest

class TestRequirement():
	'''Unit tests'''

	def test_valid_pkg_config(self):
		pkg = RequirementPackage()
		pkg.load_config_from_file('unittests/test_data/test-package/attributes.pkg')
		assert pkg.assigned_on == '2012-07-04'
		assert pkg.assigned_to == 'testclient'
		assert pkg.created_by == 'testuser'
		assert pkg.created_on == '2012-07-04'
		assert pkg.description == 'Nice requirement for testing with'
		assert pkg.depends_on == 'none'
		assert pkg.documents == 'none'
		assert pkg.estimated_effort == '400'
		assert pkg.estimated_cost == '15000'
		assert pkg.note == 'A quick note'
		assert pkg.rationale == 'The why is paramount'
		assert pkg.rejected_by == 'testclient2'
		assert pkg.status == 'approved'
		assert pkg.status_reason == 'Not really'
		assert pkg.todo == '- Write tests'
		assert pkg._name == 'test-package'
		assert pkg._id == ''
		assert pkg._pretty_name == 'Test package'
		assert pkg._file_name == 'attributes.pkg'

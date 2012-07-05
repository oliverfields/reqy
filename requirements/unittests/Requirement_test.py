from ..Requirement import *
import pytest

class TestRequirement():
	'''Unit tests'''

	def test_file_nameing(self):
		req = Requirement()
		req.set_name_and_id('1-1_some-amazing-requirement.req')
		assert req._name == 'some-amazing-requirement'
		assert req._id == '1-1'
		assert req._pretty_name == '1-1 Some amazing requirement'

	def test_file_nameing_1(self):
		req = Requirement()
		req.set_name_and_id('some-amazing-requirement.req')
		assert req._name == 'some-amazing-requirement'
#		assert req._id == ''
		assert req._pretty_name == 'Some amazing requirement'

	def test_file_nameing_2(self):
		""" Check invalid file name """
		req = Requirement()
		with pytest.raises(SystemExit):
			req.set_name_and_id('_afs.req')

	def test_file_nameing_3(self):
		req = Requirement()
		req.set_name_and_id('/a/directory/hiearachy/some-amazing-requirement.req')
		assert req._name == 'some-amazing-requirement'
		assert req._pretty_name == 'Some amazing requirement'

	def test_file_nameing_4(self):
		req = Requirement()
		req.set_name_and_id('/a/directory/hiearachy/22-21-11_some-amazing-requirement.req')
		assert req._name == 'some-amazing-requirement'
		assert req._id == '22-21-11'
		assert req._pretty_name == '22-21-11 Some amazing requirement'

	def test_valid_req_config(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config.req')

		assert req.assigned_on == '2012-07-04'
		assert req.assigned_to == 'testclient'
		assert req.created_by == 'testuser'
		assert req.created_on == '2012-07-04'
		assert req.description == 'Nice requirement for testing with'
		assert req.depends_on == 'none'
		assert req.documents == 'none'
		assert req.estimated_effort == '400'
		assert req.estimated_cost == '15000'
		assert req.note == 'A quick note'
		assert req.rationale == 'The why is paramount'
		assert req.rejected_by == 'testclient2'
		assert req.status == 'approved'
		assert req.status_reason == 'Not really'
		assert req.todo == '- Write tests'

	def test_valid_req_config_1(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config_1.req')

		assert req.description == 'Nice requirement for testing with'
		assert req.rationale == 'The why is paramount'

	def test_valid_req_config_2(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config_2.req')

		assert req.assigned_on == '2012-07-04'
		assert req.assigned_to == 'testclient'
		assert req.description == 'Nice requirement for testing with\nAnd more text # this is not a comment'
		assert req.depends_on == 'none'
		assert req.estimated_effort == '400'
		assert req.rationale == 'The why is paramount # this is not a comment'
		assert req.status == 'approved'
		assert req.status_reason == 'Not really'

	def test_valid_req_config_3(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config_3.req')

		assert req.description == 'Nice requirement for testing with'
		assert req.rationale == 'The why is paramount\nThe why is paramount2'
		assert req.status == 'elaboration'
		assert req.todo == '- test multi lines'

	def test_valid_req_config_4(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config_4.req')

		assert req.assigned_on == '2012-07-04 is a bad date'
		assert req.assigned_to == 'testclientnot is not a client'
		assert req.description == 'Nice requirement for testing with'
		assert req.depends_on == 'none nothing is not allowed setting'
		assert req.documents == 'none'
		assert req.estimated_effort == '4.00'
		assert req.estimated_cost == '15, 000'
		assert req.note == 'A quick note'
		assert req.rationale == 'The why is paramount'
		assert req.status == 'elaboration'

	def test_file_missing_extension(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/file_missing_extension')

	def test_invalid_req_config(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config.req')

	def test_invalid_req_config_1(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_1.req')

	def test_invalid_req_config_2(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_2.req')

	def test_invalid_req_config_3(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_3.req')

	def test_invalid_req_config_4(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_4.req')

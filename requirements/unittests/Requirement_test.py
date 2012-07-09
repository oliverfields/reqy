from ..Requirement import *
import pytest


class TestRequirement():
	'''Unit tests'''

	def test_valid_req_config(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config.req')

		assert req.assigned_on == '2012-07-04'
		assert len(req.assigned_to) == 1
		assert len(req.created_by) == 1
		assert req.created_on == '2012-07-04'
		assert req.description == 'Nice requirement for testing with'
		assert req.depends_on == None
		assert req.documents == None
		assert req.estimated_effort == '400'
		assert req.estimated_cost == '15000'
		assert req.note == 'A quick note'
		assert req.rationale == 'The why is paramount'
		assert len(req.rejected_by) == 1
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
		assert len(req.assigned_to) == 1
		assert req.description == 'Nice requirement for testing with\nAnd more text # this is not a comment'
		assert req.depends_on == None
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

		assert req.assigned_on == '2012-07-04'
		assert req.description == 'Nice requirement for testing with'
		assert req.depends_on == None
		assert req.documents == None
		assert req.estimated_effort == '400'
		assert req.estimated_cost == '15000'
		assert req.note == 'A quick note'
		assert req.rationale == 'The why is paramount'
		assert req.status == 'elaboration'

	def test_valid_req_config_5(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config_5.req')

		assert req.description == 'This does not fail because status is rejected and there is a rejected by'
		assert req.rationale == 'To test'
		assert req.status == 'rejected'
		assert req.status_reason == 'Something'
		assert len(req.rejected_by) == 1

	def test_valid_req_config_6_to_10(self):
		""" all of these are just trying different things that should not cause exceptions """
		for i in range(6, 10):
			req = Requirement()
			req.load_config_from_file('unittests/test_data/requirement_config_%s.req' % i)

	def test_valid_req_config_11(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config_11.req')

		assert len(req.documents) == 2

	def test_valid_req_config_12(self):
		req = Requirement()
		req.load_config_from_file('unittests/test_data/requirement_config_12.req')
		assert len(req.documents) == 2
		assert req.created_by[0].endswith('estuser.sth')

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

	def test_invalid_req_config_5(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_5.req')

	def test_invalid_req_config_6(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_6.req')

	def test_invalid_req_config_7(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_7.req')

	def test_invalid_req_config_8(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_8.req')

	def test_invalid_req_config_9(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_9.req')

	def test_invalid_req_config_10(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('unittests/test_data/invalid_requirement_config_10.req')

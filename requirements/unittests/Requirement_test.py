from ..Requirement import *
import pytest


class TestRequirement():
	'''Unit tests'''

	def test_valid_req_config(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config.req')

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
		assert req.status == 'rejected'
		assert req.status_reason == 'Not really'
		assert req.todo == '- Write tests'

	def test_valid_req_config_1(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_1.req')

		assert req.description == 'Nice requirement for testing with'
		assert req.rationale == 'The why is paramount'

	def test_valid_req_config_2(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_2.req')

		assert req.assigned_on == '2012-07-04'
		assert len(req.assigned_to) == 1
		assert req.description == 'Nice requirement for testing with\nAnd more text # this is not a comment'
		assert req.depends_on == None
		assert req.estimated_effort == '400'
		assert req.rationale == 'The why is paramount # this is not a comment'
		assert req.status == 'implementation'
		assert req.status_reason == 'Not really'

	def test_valid_req_config_3(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_3.req')

		assert req.description == 'Nice requirement for testing with'
		assert req.rationale == 'The why is paramount\nThe why is paramount2'
		assert req.status == 'elaboration'
		assert req.todo == '- test multi lines'

	def test_valid_req_config_4(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_4.req')

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
		req.load_config_from_file('test_data/requirement_config_5.req')

		assert req.description == 'This does not fail because status is rejected and there is a rejected by'
		assert req.rationale == 'To test'
		assert req.status == 'rejected'
		assert req.status_reason == 'Something'
		assert len(req.rejected_by) == 1

	def test_valid_req_config_6_to_10(self):
		""" all of these are just trying different things that should not cause exceptions """
		for i in range(6, 10):
			req = Requirement()
			req.load_config_from_file('test_data/requirement_config_%s.req' % i)

	def test_valid_req_config_11(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_11.req')

		assert len(req.documents) == 2

	def test_valid_req_config_12(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_12.req')
		assert len(req.documents) == 2
		assert req.created_by[0].endswith('estuser.sth')

	def test_valid_req_config_13(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_13.req')
		assert req.status == 'approved'
		assert req.approved_by[0].endswith('testuser.sth')

	def test_valid_req_config_14(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_14.req')
		assert req.status == 'approved'
		assert req.approved_by[0].endswith('testuser.sth')

	def test_valid_req_config_15(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_15.req')
		assert req.priority == 'must'

	def test_valid_req_config_16(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_16.req')
		assert req.change_log[0]['date'] == '2012-05-11'
		assert req.change_log[0]['pretty_name'] == 'requirement Config_16'
		assert req.change_log[0]['message'] == 'afe'
		assert req.change_log[0]['stakeholder'] == 'oliver'
		assert req.change_log[1]['date'] == '2012-05-10'
		assert req.change_log[1]['pretty_name'] == 'requirement Config_16'
		assert req.change_log[1]['message'] == 'afe'
		assert req.change_log[1]['stakeholder'] == 'oliver'

	def test_valid_req_config_17(self):
		req = Requirement()
		req.load_config_from_file('test_data/requirement_config_17.req')
		assert req.estimated_effort == '10/20/30'

	def test_title_attribute(self):
		req = Requirement()
		req.load_config_from_file('test_data/1.1.2_requirement_title.req')
		assert req.title == '1.1.2 The title'

	def test_file_missing_extension(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/file_missing_extension')

	def test_invalid_req_config(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config.req')

	def test_invalid_req_config_1(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_1.req')

	def test_invalid_req_config_2(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_2.req')

	def test_invalid_req_config_3(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_3.req')

	def test_invalid_req_config_4(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_4.req')

	def test_invalid_req_config_5(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_5.req')

	def test_invalid_req_config_6(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_6.req')

	def test_invalid_req_config_7(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_7.req')

	def test_invalid_req_config_8(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_8.req')

	def test_invalid_req_config_9(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_9.req')

	def test_invalid_req_config_10(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_10.req')

	def test_invalid_req_config_14(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_14.req')

	def test_invalid_req_config_12(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_12.req')

	def test_invalid_req_config_15(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_15.req')

	def test_invalid_req_config_11(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_11.req')

	def test_invalid_req_config_16(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_16.req')
	
	def test_invalid_req_config_17(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_17.req')
	
	def test_invalid_req_config_18(self):
		req = Requirement()
		with pytest.raises(SystemExit):
			req.load_config_from_file('test_data/invalid_requirement_config_18.req')

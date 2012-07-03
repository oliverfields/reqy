from .. import ConfigFile 

class TestConfigFile():
	'''Unit tests'''

	def test_valid_req_config(self):
		cf = ConfigFile()
		cf.load_config_from_file('test_data/valid_config.req')

		assert cf.assigned_on == '2000-05-11'
		assert cf.assigned_to == 'her'
		assert cf.created_by == 'him'
		assert cf.created_on == '2000-06-26'
		assert cf.description == 'The discription must contain\nline\nbreaks\nelse is does not count'
		assert cf.depends_on == 'an array'
		assert cf.documents == 'an array'
		assert cf.estimated_effort == 10
		assert cf.estimated_cost == 2000
		assert cf.note == 'A digital post-it'
		assert cf.rationale == 'A rationale that also contains\nline\breaks'
		assert cf.rejected_by == 'stakeholder'
		assert cf.status == 'rejected'
		assert cf.status_reason == 'Just because'
		assert cf.todo == 'an array of todos'

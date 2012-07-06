from ..GlossaryTermDefinition import *
import pytest

class TestGlossaryTermDefinition():
	'''Unit tests'''

	def test_valid_gtd_config(self):
		gtd = GlossaryTermDefinition()
		gtd.load_config_from_file('unittests/test_data/term_definition_1.def')
		assert gtd.created_by == 'testuser'
		assert gtd.created_on == '2012-07-06'
		assert gtd.definition == 'A round fruit'
		assert gtd.note == 'Need to find latin description'
		assert gtd.rejected_by == 'testuser'
		assert gtd.rejected_on == '2012-07-06'
		assert gtd.replaced_by == 'Banana'
		assert gtd.status == 'replaced'
		assert gtd.status_reason == 'Prefer yellow oblong fruits'
		assert gtd.term == 'Apple'
		assert gtd.todo == 'Make a smoothie'

	def test_valid_gtd_config(self):
		gtd = GlossaryTermDefinition()
		gtd.load_config_from_file('unittests/test_data/term_definition_2.def')
		assert gtd.definition == 'A round fruit'
		assert gtd.term == 'Apple'

	def test_invalid_gtd_config(self):
		gtd = GlossaryTermDefinition()
		with pytest.raises(SystemExit):
			gtd.load_config_from_file('unittests/test_data/invalid_term_definition.def')

	def test_invalid_gtd_config_1(self):
		gtd = GlossaryTermDefinition()
		with pytest.raises(SystemExit):
			gtd.load_config_from_file('unittests/test_data/invalid_term_definition_1.def')

	def test_invalid_gtd_config_2(self):
		gtd = GlossaryTermDefinition()
		with pytest.raises(SystemExit):
			gtd.load_config_from_file('unittests/test_data/invalid_term_definition_2.def')

	def test_invalid_gtd_config_3(self):
		gtd = GlossaryTermDefinition()
		with pytest.raises(SystemExit):
			gtd.load_config_from_file('unittests/test_data/invalid_term_definition_3.def')

	def test_invalid_gtd_config_4(self):
		gtd = GlossaryTermDefinition()
		with pytest.raises(SystemExit):
			gtd.load_config_from_file('unittests/test_data/invalid_term_definition_4.def')

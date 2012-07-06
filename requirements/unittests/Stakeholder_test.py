from ..Stakeholder import *
import pytest

class TestStakeholder():
	'''Unit tests'''

	def test_invalid_sth_config(self):
		sth = Stakeholder()
		with pytest.raises(SystemExit):
			sth.load_config_from_file('unittests/test_data/invalid_stakeholder_definition.sth')

	def test_invalid_sth_config_1(self):
		sth = Stakeholder()
		with pytest.raises(SystemExit):
			sth.load_config_from_file('unittests/test_data/invalid_stakeholder_definition_1.sth')

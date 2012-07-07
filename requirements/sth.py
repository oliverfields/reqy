from Stakeholder import *

st = Stakeholder()
st.load_config_from_file('unittests/test_data/sample-repository/stakeholders/testuser.sth')
st.dump_attributes()


from GlossaryTermDefinition import *

gdef = GlossaryTermDefinition()
gdef.load_config_from_file('unittests/test_data/sample-repository/glossary/apple.def')
gdef.dump_attributes()


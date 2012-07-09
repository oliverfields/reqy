import os
import Settings
from Requirement import *
from Document import *
from Stakeholder import *
from GlossaryTermDefinition import *

class LinkList:
	""" Parse link list strings and load respective config files """

	def load_link_targets(self, root_directory, link_list_string, file_extension):
		""" Load link list targets and return link list """
		link_list_string = self.parse_link_list_string(link_list_string)
		link_list = [] 
		if link_list_string:
			for link in link_list_string:
				file_path = os.path.join(Settings.repository_directory, os.path.join(root_directory, link)) + file_extension

				if os.path.isfile(file_path) == False:
					raise Exception('"%s" is broken' % file_path)

				if root_directory == 'documents':
					link_object = Document()
					link_object.load_document(file_path)
				elif root_directory == 'stakeholders':
					link_object = Stakeholder()
					link_object.load_config_from_file(file_path)
				elif root_directory == 'requirements':
					link_object = Requirement()
					link_object.load_config_from_file(file_path)
				elif root_directory == 'glossary':
					link_object = GlossartTermDefinition()
					link_object.load_config_from_file(file_path)
				else:
					raise Exception('unknown link list type "%s"' % root_directory)

				link_list.append(link_object)

			return link_list



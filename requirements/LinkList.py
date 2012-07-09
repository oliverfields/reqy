import os
import Settings
from Requirement import *
from Document import *
from Stakeholder import *
from GlossaryTermDefinition import *

class LinkList:
	""" Parse link list strings and load respective config files """
	def parse_link_list_string(self, link_list_string):
		""" Accepts comma seperated string (may include line breaks) and returns array of each element """
		link_list = []

		if link_list_string == None:
			return None

		link_list_string.replace('\n', '')

		for link in link_list_string.split(','):
			link = link.strip()
			if len(link) > 0:
				link_list.append(link)
		
		if len(link_list) > 0:
			return link_list
		else:
			return None

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

	def make_link_list(self, root_directory, nice_attribute_name, link_list_string, multiple_allowed = True):
		""" Returns list of appropriate objects and check that each link exists as a file on disk """

		# If value None, then we are done:)
		if link_list_string == None or link_list_string == 'none':
			return None

		link_list_string = link_list_string.strip()

		if root_directory == 'requirements':
			file_extension = '.req'
		elif root_directory == 'documents':
			# Any extension is permissable
			file_extension = ''
		elif root_directory == 'stakeholders':
			file_extension = '.sth'
		else:
			raise Exception('Field "%s" has unknown link list type "%s"' % (nice_attribute_name, root_directory))

		# If multiple links not allowed, but there are more than one (i.e. a comma)
		if multiple_allowed == False and link_list_string.find(',') > 0:
			raise Exception('Field "%s" may only contain one link (content "%s")' % (nice_attribute_name, link_list_string))

		try:
			return self.load_link_targets(root_directory, link_list_string, file_extension)
		except Exception, error_message:
			raise Exception('Field "%s" %s link %s' % (nice_attribute_name, root_directory, error_message))


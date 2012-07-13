import Utility
import os.path
import re

class ConfigFile:
	'''
	Load object attributes from configuration file
	'''
	def __init__(self):
		self._parent = None
		self._children = None 
		self._valid_file_extension = ''
		self._file_name = None
		self._file_path = None
		self._id = None
		self._name = None
		self._pretty_name = None

	def is_integer(self, string):
		""" If string is not empty, check if it is an integer """
		if string != None:
			try:
				int(string)
				return True
			except:
				return False

	def is_string_date(self, string):
		""" Check if date is acceptable date YYYY-MM-DD, or None """
		if string == None:
			return True 
		else:
			match = re.search(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$', string)
			if match:
				return True
			else:
				return False

	def validate_settings(self):
		""" Stub function, needs to be implemented by sub class """
		pass

	def set_name_and_id(self, file_name):
		""" Extract from file name the an optional id prefix and a short name, discarding the file extension """
		file_name = os.path.basename(file_name)
		if file_name.startswith('_'):
				Utility.report_error(1, '%s: File name cannot start with underscore, valid format is "[id_]a-nice-name.%s"' % (self._file_path, self._valid_file_extension))
		file_name = file_name.rstrip(''.join(self._valid_file_extension))
		file_name = file_name.rstrip('.')
		file_strings = file_name.partition('_')
		# If two last elements are empty the underscore wasn't there
		if file_strings[1] == '' and file_strings[2] == '':
			self._name = file_strings[0]
			self._id = ''
			self._pretty_name = self._name.replace('-', ' ').capitalize()
		else:
			self._name = file_strings[2]
			self._id = file_strings[0]
			self._pretty_name = '%s %s' % (self._id, self._name.replace('-', ' ').capitalize())

	def assign_attribute(self, key, value):
		""" Check valid key and is so assign to object attribute """
		is_valid_key = False
		# Get all object attributes, valid keys are the ones not
		# starting with underscore, then check the setting is valid
		for attribute in vars(self).keys():
			if attribute.startswith('_') == False:
				if key.lower() == attribute.lower():
					is_valid_key = True
		if is_valid_key:
			setattr(self, key, value)
		else:
			Utility.report_error(1, '%s: Key "%s" is not valid' % (self._file_path, key))

	def load_config_from_file(self, file_name):
		""" Read config file and pass key values on for assignment """
		self._file_name = os.path.basename(file_name)
		self._file_path = os.path.abspath(file_name)

		if file_name.endswith(self._valid_file_extension) == False:
			Utility.report_error(1, '%s: Invalid file extension, must be ".%s"' % (self._file_path, self._valid_file_extension))
			return

		self.set_name_and_id(file_name)

		try:
			conf_file = open(file_name, "r")
			try:
				lines = conf_file.readlines()
				i = 0
				max_lines = len(lines) - 1

				# Process file line by line and extract key value pairs, note
				# that values may span multiple lines if preceeded by '^[key]:$' and
				# indented by two spaces
				while True:
					key = ''
					value = ''

					# Break if no lines left
					if i > max_lines:
						break

					# Skip comments
					if lines[i].lstrip().startswith('#'):
						i += 1
						continue
					# Skip lines that only contain whitespace
					elif lines[i].strip() == '':
						i += 1
						continue
					# Multi line settings
					elif lines[i].strip().endswith(':'):
						key = lines[i]
						key = key.strip()
						key = key.rstrip(':')
						n = i + 1
						multi_line_value = ''
						# Collect following lines that start with double space
						while True:
							if n == max_lines and lines[n].startswith('  '):
								value = multi_line_value + lines[n].lstrip('  ')
								i = max_lines + 1 # this was last line, so next loop will abort
								break
							elif n > max_lines:
								i = n
								break
							elif lines[n].startswith('  '):
								multi_line_value += lines[n].lstrip('  ')
								n += 1
							# If no longer multi line set index one back and continue loop
							else:
								value = multi_line_value
								i = n 
								break
					else:
						setting = lines[i].partition(':')
						if setting[0] != '' and setting[1] != '' and setting[2] != '':
								key = setting[0]
								value = setting[2]
								i += 1
						else:
								# Something strange happend, reset counter 1 and exit with error
								error_line_number = i + 1
								Utility.report_error(1, '%s: Unable to parse line %s "%s"' % (self._file_path, error_line_number, lines[i]))

					# Tidy the key and values
					key = key.strip()
					key = key.lower()
					key = key.replace(' ', '_')
					value = value.strip()

					#print 'i: %s, Key: "%s", Value: "%s"' % (i, key, value)

					self.assign_attribute(key, value)

			finally:
				conf_file.close()
		except IOError:
			Utility.report_error(1, '%s: Unable to read file' % self._file_path)
		self.validate_settings()

	def dump_attributes(self, prefix = ''):
		""" Print all attribute values """
		print "%sAttribute values:" % prefix
		for setting in vars(self).keys():
			if hasattr(self, setting):
				print '%s"%s": "%s"' % (prefix, setting, getattr(self, setting))

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

	def make_link_list(self, root_directory, nice_attribute_name, link_list_string, multiple_allowed = True):
		""" Returns list(array) of link list string and checks that each link exists as a file on disk """

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
		elif root_directory == 'glossary':
			file_extension = '.def'
		else:
			Utility.report_error(1, '%s: Field "%s" has unknown link list type "%s"' % (self._file_path, nice_attribute_name, root_directory))

		# If multiple links not allowed, but there are more than one (i.e. a comma)
		if multiple_allowed == False and link_list_string.find(',') > 0:
			Utility.report_error(1, '%s: Field "%s" may only contain one link (content "%s")' % (self._file_path, nice_attribute_name, link_list_string))

		link_list_string = self.parse_link_list_string(link_list_string)
		link_list = []
		if link_list_string:
			for link in link_list_string:
				full_file_path = os.path.join(Utility.get_repo_dir(), os.path.join(root_directory, link))
				
				if os.path.isdir(full_file_path) == False:
					full_file_path += file_extension

				if os.path.isfile(full_file_path) == False and os.path.isdir(full_file_path) == False:
					Utility.report_error(1, '%s: "%s" link "%s" is broken (%s)' % (self._file_path, nice_attribute_name, link, full_file_path))

				link_list.append(full_file_path)

			return link_list

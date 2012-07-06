from Utility import *
import os.path

class ConfigFile:
	'''
	Load object attributes from configuration file
	'''
	def __init__(self):
		self._parent = ''
		self._children = []
		self._valid_file_extension = ''
		self._file_name = ''
		self._file_path = ''
		self._id = ''
		self._name = ''
		self._pretty_name = ''

	def validate_settings(self):
		""" Stub function, needs to be implemented by sub class """
		pass

	def set_name_and_id(self, file_name):
		""" Extract from file name the an optional id prefix and a short name, discarding the file extension """
		file_name = os.path.basename(file_name)
		if file_name.startswith('_'):
				report_error(1, '%s: File name cannot start with underscore, valid format is "[id_]a-nice-name.%s"' % (self._file_path, self._valid_file_extension))
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
			report_error(1, '%s: Key "%s" is not valid' % (self._file_name, key))

	def load_config_from_file(self, file_name):
		""" Read config file and pass key values on for assignment """
		self._file_name = os.path.basename(file_name)
		self._file_path = file_name

		if file_name.endswith(self._valid_file_extension) == False:
			report_error(1, '%s: Invalid file extension, must be ".%s"' % (self._file_path, self._valid_file_extension))
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
					elif lines[i].rstrip().endswith(':'):
						key = lines[i].rstrip(':\n')
						n = i + 1
						multi_line_value = ''
						# Collect following lines that start with double space
						while True:
							if n == max_lines:
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
								report_error(1, '%s: Unable to parse line %s "%s"' % (self._file_path, error_line_number, lines[i]))

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
			report_error(1, '%s: Unable to read file' % self._file_path)
		self.validate_settings()

	def dump_attributes(self):
		""" Print all attribute values """
		print "Attribute values:"
		for setting in vars(self).keys():
			if hasattr(self, setting):
				print '"%s": "%s"' % (setting, getattr(self, setting))

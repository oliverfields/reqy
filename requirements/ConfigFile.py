from Utility import *

class ConfigFile:
	'''
	Load object attributes from configuration file
	'''

	_file_name = ''
	
	# Must be populated to allow appropriate config settings
	# in sub classes, must contain key value pairs where key is
	# setting name and value is default value
	valid_settings = {}
	
	valid_file_extension = ''

	def validate_settings(self):
		""" Stub function, needs to be implemented by sub class """
		pass

	def assign_attribute(self, key, value):
		""" Check valid key and is so assign to object attribute """
		is_valid_key = False
		for valid_key in self.valid_settings.keys():
			if key == valid_key:
				is_valid_key = True
		if is_valid_key:
			setattr(self, str(key), value)
		else:
			report_error(1, '%s: Key "%s" is not valid' % (self._file_name, key))

	def parse_config_setting(self, setting):
		""" Parse each setting and remove comments, pass on for assignment """
		print '%s' % setting
		parsed_setting = setting.partition(':')
		key = parsed_setting[0].strip()
		key = key.lower()
		value = parsed_setting[2].strip()

                self.assign_attribute(key, value) 

	def load_config_from_file(self, file_name):
		if file_name.endswith(self.valid_file_extension) == False:
			report_error(1, '%s: Invalid file extension, must be ".%s"' % (file_name, self.valid_file_extension))
			return

		self._file_name = file_name
		try:
			conf_file = open(file_name, "r")
			try:
				line = conf_file.readline()
 
				while line:
					# If comment then jump to next
					if line.startswith('#'):
						line = conf_file.readline()

					# If multiline setting, continue reading
					# lines whilst they start with white space
					if line.endswith(':'):
						while line.startswith('  '):
							line += conf_file.readline()
							
									
					print 'Line ""%s""' % line
					#self.parse_config_setting(line)
					line = conf_file.readline()
			finally:
				conf_file.close()
		except IOError:
			report_error(1, '%s: Unable to read file' % file_name)
		self.validate_settings()

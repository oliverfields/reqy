class ConfigFile:
	'''
	Load object attributes from configuration file
	'''

	_file_name = ''
	assigned_on = ''


	def load_config_from_file(self, file_name):
		self._file_name = file_name
		self.assigned_on = '2000-05-11'
#		try:
# fileIN = open(sys.argv[1], "r")
# line = fileIN.readline()
 
# while line:
# [some bit of analysis here]
# line = fileIN.readline()
#		finally:
#			fsock.close()
#		pass

import Settings
from Requirement import *

class RequirementPackage(Requirement):
	""" Essentially same as Requirement, but a package is a directory and stores attributes in attributes.pkg file in itself """

	def __init__(self):
		Requirement.__init__(self)
		self._children = []
		self._valid_file_extension = 'pkg'

	def set_name_and_id(self, file_name):
		""" Extract from file name the parent folder name and an optional id prefix and a short name, slightly different from Requirements.set_name_and_id """
		file_name = os.path.basename(os.path.dirname(file_name))
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

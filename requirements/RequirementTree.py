import os
from Utility import *
from Requirement import *
from RequirementPackage import *

class RequirementTree:
	""" The requirements repository model """

	def __init__(self):
		self.requirements = [] 
#		self.stakeholder = 
#		self.document = Toot()
#		self.glossary = Toot()

	def load_repository(self, root_directory):
		self.load_package(root_directory, False)

	def load_package(self, package_directory, parent_package):
		""" Recursively read package directory and create and link objects """

		for name in os.listdir(package_directory):
			package_path = os.path.join(package_directory, name)
			if os.path.isdir(package_path):
				package_attributes = os.path.join(os.path.join(package_directory, name), 'attributes.pkg')
				print "Package: %s" % package_attributes
				package = RequirementPackage()
				package.load_config_from_file(package_attributes)
				package.parent = parent_package
				self.requirements.append(package)
				self.load_package(package_path, package)
			elif os.path.isfile(package_path):
				if package_path.endswith('.req'):
					print "Requirement: %s" % name
					requirement = Requirement()
					requirement.load_config_from_file(os.path.join(package_directory, name))
					requirement.parent = parent_package
					self.requirements.append(requirement)

			else:
				report_error(1,'Unidentified file system object "%s", could be a symbolic link?' % name)

	def dump_attributes(self):
		""" Print all attribute values """
		print "Attribute values:"
		for setting in vars(self).keys():
			if hasattr(self, setting):
				print '"%s": "%s"' % (setting, getattr(self, setting))

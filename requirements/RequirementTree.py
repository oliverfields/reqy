import os
import Settings
from Utility import *
from Requirement import *
from RequirementPackage import *
from Stakeholder import *
from Document import *
from GlossaryTermDefinition import *

class RequirementTree:
	""" The requirements repository model """

	def __init__(self):
		self._children = [] 
		self._name = 'root'
		self._pretty_name = 'Root'

	def load_repository(self, root_directory):
		self.load_package(os.path.join(root_directory, 'requirements'), self)

	def load_package(self, package_directory, parent_package):
		""" Recursively read package directory and create and link objects """

		for name in os.listdir(package_directory):
			package_path = os.path.join(package_directory, name)
			if os.path.isdir(package_path):
				package_attributes = os.path.join(os.path.join(package_directory, name), 'attributes.pkg')
				package = RequirementPackage()
				package.load_config_from_file(package_attributes)
				parent_package._children.append(package) 
				package._parent = parent_package
				self.load_package(package_path, package)
				self.load_link_list_objects(package)
			elif os.path.isfile(package_path):
				if package_path.endswith('.req'):
					requirement = Requirement()
					requirement.load_config_from_file(os.path.join(package_directory, name))
					self.load_link_list_objects(requirement)
					parent_package._children.append(requirement) 
					requirement._parent = parent_package

			else:
				report_error(1,'Unidentified file system object "%s", could be a symbolic link?' % name)

	def load_link_list_objects(self, object):
		""" Replace link list attribute string list elements with appropriate objects """

		link_lists = [ 'assigned_to', 'created_by', 'depends_on', 'documents', 'rejected_by' ] 

		
		if isinstance(object.documents, list):
			print 'is a list'
			new_object_documents = []
			for file_path in object.documents:
				print "daf" + file_path
				doc = Document()
				new_object_documents.append(doc.load_document(file_path))
				print 'aaaaaaaaaa' + doc.name
			
			object.documents = new_object_documents

			for d in new_object_documents:
				print d.name


		else:
			print 'awer'

	def print_tree(self):
		print self._pretty_name
		self.print_package(self, indent='  ')

	def print_package(self, parent_package, indent):
		for package in parent_package._children:
			print '%s%s' % (indent, package._pretty_name)
			if package._children:
				indent += indent
				self.print_package(package, indent)

	def dump_attributes(self):
		""" Print all attribute values """
		print "Attribute values:"
		for setting in vars(self).keys():
			if hasattr(self, setting):
				print '"%s": "%s"' % (setting, getattr(self, setting))

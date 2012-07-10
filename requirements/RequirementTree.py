import os
import Settings
from Utility import *
from Requirement import *
from RequirementPackage import *
from Stakeholder import *
from Document import *
from GlossaryTermDefinition import *

from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search

class RequirementTree:
	""" The requirements repository model """

	def __init__(self):
		self._children = [] 
		self._file_name = 'root'
		self._pretty_name = 'Root'
		self._file_path = None
		self._item_list = {} # Dictionary of all items in tree
		self._dependency_from_to = [] # List of all dependencies tuples in tree

	def load_repository(self, root_directory):
		self._file_path = os.path.abspath(root_directory)
		self.load_package(os.path.join(root_directory, 'requirements'), self)

	def load_package(self, package_directory, parent_package):
		""" Recursively read package directory and create and link objects """

		for name in os.listdir(package_directory):
			package_path = os.path.join(package_directory, name)
			if os.path.isdir(package_path):
				package_attributes = os.path.join(os.path.join(package_directory, name), 'attributes.pkg')
				package = RequirementPackage()
				package.load_config_from_file(package_attributes)
				self.add_to_item_list(package)
				parent_package._children.append(package) 
				package._parent = parent_package
				self.add_dependency_from_to(package._file_path, parent_package._file_path)
				self.load_package(package_path, package)
				package.assigned_to = self.get_link_list_objects(package, 'stakeholder', package.assigned_to)
				package.created_by = self.get_link_list_objects(package, 'stakeholder', package.created_by)
				package.documents = self.get_link_list_objects(package, 'documents', package.documents)
				package.rejected_by = self.get_link_list_objects(package, 'stakeholder', package.rejected_by)
				package.depends_on = self.get_link_list_objects(package, 'requirement', package.depends_on)
			elif os.path.isfile(package_path):
				if package_path.endswith('.req'):
					requirement = Requirement()
					requirement.load_config_from_file(os.path.join(package_directory, name))
					requirement.assigned_to = self.get_link_list_objects(requirement, 'stakeholder', requirement.assigned_to)
					requirement.created_by = self.get_link_list_objects(requirement, 'stakeholder', requirement.created_by)
					requirement.documents = self.get_link_list_objects(requirement, 'documents', requirement.documents)
					requirement.rejected_by = self.get_link_list_objects(requirement, 'stakeholder', requirement.rejected_by)
					requirement.depends_on = self.get_link_list_objects(requirement, 'requirement', requirement.depends_on)

					parent_package._children.append(requirement) 
					requirement._parent = parent_package
					self.add_to_item_list(requirement)
					self.add_dependency_from_to(requirement._file_path, parent_package._file_path)

			else:
				report_error(1,'Unidentified file system object "%s", could be a symbolic link?' % name)

	def get_link_list_objects(self, parent, link_list_type, link_list):
		""" Return list of objects based on passed link list """
		if link_list == None:
			return None
		else:
			list_objects = []

		if link_list_type == 'documents':
			for link in link_list:
				doc = Document()
				doc.load_document(link)
				self.add_dependency_from_to(doc._file_path, parent._file_path)
				list_objects.append(doc)
		elif link_list_type == 'assigned_to' or link_list_type == 'created_by' or link_list_type == 'rejected_by':
			for link in link_list:
				sth = Stakeholder()
				sth.load_config_from_file(link)
				self.add_dependency_from_to(sth._file_path, parent._file_path)
				list_objects.append(sth)
		elif link_list_type == 'requirement':
			for link in link_list:
				if link.endswith('.req'):
					req = Requirement()
					req.load_config_from_file(link)
					self.add_dependency_from_to(req._file_path, parent._file_path)
					list_objects.append(req)
				elif link.endswith('attributes.pkg'):
					pkg = RequirementPackage()
					pkg.load_config_from_file(link)
					self.add_dependency_from_to(pkg._file_path, parent._file_path)
					list_objects.append(pkg)

		return list_objects

	def add_to_item_list(self, item):
		self._item_list[item._file_path] = item._file_name

	def add_dependency_from_to(self, dep_from_file_path, dep_to_file_path):
		self._dependency_from_to.append([dep_from_file_path, dep_to_file_path])

	def print_tree(self):
		print self._pretty_name
		self.print_package(self, indent='  ')

	def print_package(self, parent_package, indent):
		for package in parent_package._children:
			print '%s----- %s -----' % (indent, package._pretty_name)
			print '%s%s' % (indent, package._pretty_name)
			package.dump_attributes(indent + indent)
			if package._children:
				indent += indent
				self.print_package(package, indent)
			print '%s----- /%s -----' % (indent, package._pretty_name)

	def dump_attributes(self):
		""" Print all attribute values """
		print "Attribute values:"
		for setting in vars(self).keys():
			if hasattr(self, setting):
				print '"%s": "%s"' % (setting, getattr(self, setting))

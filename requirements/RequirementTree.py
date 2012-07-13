import os
from Requirement import *
from RequirementPackage import *
from Stakeholder import *
from Document import *
from GlossaryTermDefinition import *
from ProjectConfig import ProjectConfig
from Utility import get_repo_dir

#from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search

class RequirementTree:
	""" The requirements repository model """

	def __init__(self):
		project = ProjectConfig()
		project.load_config_from_file(os.path.join(get_repo_dir(), 'project.conf'))

		self._children = [] 
		self._file_name = 'root'
		self._pretty_name = project.name
		self._file_path = None
		self._dependencies_from_to = None
		self._node_list = None

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
				parent_package._children.append(package) 
				package._parent = parent_package
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
				list_objects.append(doc)
		elif link_list_type == 'assigned_to' or link_list_type == 'created_by' or link_list_type == 'rejected_by':
			for link in link_list:
				sth = Stakeholder()
				sth.load_config_from_file(link)
				list_objects.append(sth)
		elif link_list_type == 'requirement':
			for link in link_list:
				if link.endswith('.req'):
					req = Requirement()
					req.load_config_from_file(link)
					list_objects.append(req)
				elif link.endswith('attributes.pkg'):
					pkg = RequirementPackage()
					pkg.load_config_from_file(link)
					list_objects.append(pkg)

		return list_objects

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

	def get_dependencies(self):
		"""
		Public function to return list of dependencies between objects in tree.

		Note that if function has been run, then it just returns cached list.
		"""
		if self._dependencies_from_to == None:
			self._dependencies_from_to = []
			self._get_dependencies(self)
		
		return self._dependencies_from_to

	def _get_dependencies(self, parent_package):
		"""
		Private recursive method to find all dependencies in tree
		"""
		for package in parent_package._children:
			# Add parent child dependency
			self._dependencies_from_to.append([parent_package, package])

			# Check if package has other dependecies
			if package.depends_on != None:
				for item in package.depends_on:
					self._dependencies_from_to.append([package, item])

			if package.documents != None:
				for item in package.documents:
					self._dependencies_from_to.append([package, item])

			if package._children:
				self._get_dependencies(package)

		return self._dependencies_from_to

	def get_tree_items(self):
		""" Get list of each item in tree """
		# Make sure dependencies are loaded
		tree_items = self.get_dependencies()

		if self._node_list == None:
			self._node_list = []
		# Make a list of all items 
			for item in tree_items:
				self._node_list.append(item[0])
				self._node_list.append(item[1])

		# Make a set of the list and then make the result a list and all duplicates
		# are bye bye
			self._node_list = list(set(self._node_list))

		return self._node_list	

	def dump_attributes(self):
		""" Print all attribute values """
		print "Attribute values:"
		for setting in vars(self).keys():
			if hasattr(self, setting):
				print '"%s": "%s"' % (setting, getattr(self, setting))

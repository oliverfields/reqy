# Copyright (c) 2012 - Oliver Fields, oliver@phnd.net
#
# This file is part of Reqy.
#
# Reqy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Reqy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Reqy.  If not, see <http://www.gnu.org/licenses/>.

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
		self._short_name = project.short_name
		self._file_path = None
		self._dependencies_from_to = None
		self._node_list = None


	def load_repository(self, root_directory):
		self._file_path = os.path.abspath(root_directory)
		self.load_package(os.path.join(root_directory, 'requirements'), self)


	def is_item(self, item_file_path):
		""" Check if the item file name exists in repository """
		item_exists = False

		# Add attributes.pkg if dir
		if os.path.isdir(item_file_path):
			item_file_path = os.path.join(item_file_path, 'attributes.pkg')

		# Load dependencies and items
		items = self.get_tree_items()
		for item in items:
			if item._file_path == item_file_path:
				item_exists = True
				break

		return item_exists


	def load_package(self, package_directory, parent_package):
		""" Recursively read package directory and create and link objects """

		file_listing = os.listdir(package_directory)
		file_listing.sort()
		for name in file_listing:
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
				package.approved_by = self.get_link_list_objects(package, 'stakeholder', package.approved_by)
				package.postponed_by = self.get_link_list_objects(package, 'stakeholder', package.postponed_by)
				package.depends_on = self.get_link_list_objects(package, 'requirement', package.depends_on)
			elif os.path.isfile(package_path):
				if package_path.endswith('.req'):
					requirement = Requirement()
					requirement.load_config_from_file(os.path.join(package_directory, name))
					requirement.assigned_to = self.get_link_list_objects(requirement, 'stakeholder', requirement.assigned_to)
					requirement.created_by = self.get_link_list_objects(requirement, 'stakeholder', requirement.created_by)
					requirement.documents = self.get_link_list_objects(requirement, 'documents', requirement.documents)
					requirement.rejected_by = self.get_link_list_objects(requirement, 'stakeholder', requirement.rejected_by)
					requirement.approved_by = self.get_link_list_objects(requirement, 'stakeholder', requirement.approved_by)
					requirement.postponed_by = self.get_link_list_objects(requirement, 'stakeholder', requirement.postponed_by)
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
		elif link_list_type == 'stakeholder':
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


	def get_package_items(self, parent_package):
		for package in parent_package._children:
			self._node_list.append(package)
		
			if package.documents:
				for doc in package.documents:
					self._node_list.append(doc)

			if package._children:
				self.get_package_items(package)


	def get_tree_items(self):
		""" Get list of each item in tree """

		if self._node_list == None:
			self._node_list = []
		# Make a list of all items 
			for item in self._children:
				self._node_list.append(item)
				if item.documents:
					for doc in item.documents:
						self._node_list.append(doc)
				if item._children:
					self.get_package_items(item)

		return self._node_list	


	def dump_attributes(self):
		""" Print all attribute values """
		print "Attribute values:"
		for setting in vars(self).keys():
			if hasattr(self, setting):
				print '"%s": "%s"' % (setting, getattr(self, setting))


	def list_direct_traces(self, item_file_path):
		"""
		For item, return direct traces to and from (i.e. indirect traces are not shown)
		"""
		repo_dir = get_repo_dir()
		traces = None

		# If not absolute path, add repo dir
		if item_file_path.startswith(os.sep) == False:
			item_file_path = os.path.join(repo_dir, item_file_path)

		# If package, add attributes.pkg
		if os.path.isdir(item_file_path):
			item_file_path = os.path.join(item_file_path, 'attributes.pkg')

		# Check item exists in tree
		if self.is_item(item_file_path) == False:
			report_error(1, 'The item "%s" was not found in the repository' % item_file_path)

		# Loop over dependencies and compile list of dependencies to and from item
		# List direct traces to the item
		traces = { 'to': [], 'from': [] }
		for item in self.get_dependencies():
			if item[0]._file_path == item_file_path:
				traces['to'].append(item[1])
			elif item[1]._file_path == item_file_path:
				traces['from'].append(item[0])

		return traces

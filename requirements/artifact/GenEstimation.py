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

from Artifact import *
from ..ProjectConfig import ProjectConfig
from ..RequirementTree import RequirementTree
from ..Requirement import Requirement
from ..RequirementPackage import RequirementPackage
from ..Document import Document
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr, report_error
import odf.opendocument
import odf.meta
import odf.dc
#from odf.style import Style, TextProperties, TableColumnProperties, ParagraphProperties
from odf.text import P
from odf.table import Table, TableCell, TableRow
import os

class GenEstimation(Artifact):
	"""
	Generate ods file with detailed listing of the requirements for use when estimating
	"""

	def __init__(self):
		self.name = 'estimation'
		self.description = 'Generate ods file with detailed listing of the requirements for use when estimating'


	def make_row(self, row):
		""" For each item in array add a cell to a row """
		tr = TableRow()
		for cell_text in row:
			try:
				#i = int(cell_text)
				tc = TableCell(formula=cell_text)
			except:
				tc = TableCell()
				txt = P(text=cell_text)
				tc.addElement(txt)

			tr.addElement(tc)

		return tr


	def make_formula_row(self, text, formula):
		tr = TableRow()
		tc = TableCell()
		txt = P(text=text)
		tc.addElement(txt)
		tr.addElement(tc)
		tc = TableCell(formula=formula)
		tr.addElement(tc)

		return tr


	def generate(self, target_file):
		""" List each requirement and it's details """

		repo_dir = get_repo_dir()

		rt = RequirementTree()
		rt.load_repository(repo_dir)
		template_file = 'project-estimation-template.ods'

		ods = odf.opendocument.OpenDocumentSpreadsheet()

		if rt._pretty_name:
			ods.meta.addElement(odf.dc.Title(text=rt._pretty_name))
		else:
			ods.meta.addElement(odf.dc.Title(text='[Set name in project.conf]'))

		# Add sheet with formulas
		formula_tbl = Table(name="Estimation")

		# Add sheet with data
		data_tbl = Table(name="Data")

		# Data header row
		data_tbl.addElement(self.make_row(['Name', 'Hours', 'Cost']))

		items = 1
		for item in rt.get_tree_items():
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				items += 1
				data_tbl.addElement(self.make_row([item._pretty_name, item.estimated_effort, item.estimated_cost]))

		# Formulas
		formula_tbl.addElement(self.make_row(['Settings']))
		formula_tbl.addElement(self.make_formula_row('Hourly rate', '1000'))
		formula_tbl.addElement(self.make_formula_row('Effective hours per day', '5'))
		formula_tbl.addElement(TableRow())
		formula_tbl.addElement(self.make_row(['Calculations']))
		formula_tbl.addElement(self.make_formula_row('Total estimated hours', '=SUM(Data.B2:Data.B%s' % items))
		formula_tbl.addElement(self.make_formula_row('Total estimated cost', '=SUM(Data.C2:Data.C%s' % items))
		formula_tbl.addElement(self.make_formula_row('Calculated cost', '=SUM(B7*B2)'))
		formula_tbl.addElement(self.make_formula_row('Estimated work weeks', '=SUM((B3*B7)/5)'))

		ods.spreadsheet.addElement(formula_tbl)
		ods.spreadsheet.addElement(data_tbl)

		try:
			ods.save(target_file, True)
		except:
			report_error(1, 'Unable to write to "%s", is file open?' % target_file)

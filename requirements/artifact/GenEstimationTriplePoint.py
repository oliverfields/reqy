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
from ..Utility import get_repo_dir, documents_by_type, make_path_relative, xstr, report_error, report_notice
import odf.opendocument
import odf.meta
import odf.dc
#from odf.style import Style, TextProperties, TableColumnProperties, ParagraphProperties
from odf.text import P
from odf.table import Table, TableCell, TableRow
import os
import sys
from math import sqrt

class GenEstimationTriplePoint(Artifact):
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
			cell_text = str(cell_text)
			try:
				#i = int(cell_text)
				tc = TableCell(formula=cell_text)
			except:
				tc = TableCell()
				txt = P(text=cell_text)
				tc.addElement(txt)

			tr.addElement(tc)

		return tr


	def generate(self, target_file):
		""" List each requirement and it's details """

		repo_dir = get_repo_dir()

		rt = RequirementTree()
		rt.load_repository(repo_dir)

		template_file = 'project-estimation-triple-point-template.ods'

		ods = odf.opendocument.OpenDocumentSpreadsheet()

		if rt._pretty_name:
			ods.meta.addElement(odf.dc.Title(text=rt._pretty_name))
		else:
			ods.meta.addElement(odf.dc.Title(text='[Set name in project.conf]'))

		data_tbl = Table(name="Data")

		# Data header row
		data_tbl.addElement(self.make_row(['Name', 'Best case', 'Likely', 'Worst case', 'Varience', 'Uncertaincy']))

		items = 1
		mean = 0
		sum_varience = 0
		est_data = []

		for item in rt.get_tree_items():
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):
				if item.is_triple_point_estimate(item.estimated_effort) == False:
					report_error(1, '%s: Estimated effort "%s" is not a valid triple point estimate (best case/likely/worst case).' % (item._file_path, item.estimated_effort))
				items += 1
				triple_points = item.estimated_effort.split('/')
				best_case = float(triple_points[0])
				likely_case = float(triple_points[1])
				worst_case = float(triple_points[2])
				varience = float(pow((worst_case-best_case)/5,2))
				sum_varience += varience
				mean += float((best_case+3*likely_case+worst_case)/5)

				est_data.append({'name': item._pretty_name, 'best_case': best_case, 'likely': likely_case, 'worst_case': worst_case, 'varience': varience}) 
				#print("%s - %s/%s/%s - %s" % (item._pretty_name, best_case, likely_case, worst_case, varience)) 

		stddiv = float(sqrt(sum_varience))
		stddiv_mean = float(stddiv/mean)

		# Work out % varience of total
		n = 1
		for i in est_data:
			n += 1
			i['varience_of_total'] = float(i['varience']/sum_varience)
			data_tbl.addElement(self.make_row([i['name'], i['best_case'],i['likely'],i['worst_case'],i['varience'],i['varience_of_total']]))

		# Sort by uncertaincy

		# Distribution
		distribution_data = [
      ['-3SD',float(mean-3*stddiv),1],
      ['-2SD',float(mean-2*stddiv),3],
      ['-1SD',float(mean-stddiv),16],
      ['Mean',float(mean),50],
      ['+1SD',float(mean+stddiv),85],
      ['+2SD',float(mean+2*stddiv),97],
      ['+3SD',float(mean+3*stddiv),99]
    ]

#		print est_data
#		print "Stddiv: %s" % stddiv
#		print "Stddiv mean: %s" % stddiv_mean
#		print "Sum varience: %s" % sum_varience

#		print distribution_data
				#data_tbl.addElement(self.make_row([item._pretty_name, triple_points[0], triple_points[1], triple_points[2], item.estimated_cost]))

		if items == 1:
			sys.exit(0)


		#calc_tbl.insertBefore(self.make_row(['Total estimated hours', '=SUM(Data.B2:Data.B%s' % items]), calc_2nd_row)
		#calc_tbl.insertBefore(self.make_row(['Total estimated cost', '=SUM(Data.C2:Data.C%s' % items]), calc_2nd_row)

		summary_tbl = Table(name="Summary")

		summary_tbl.addElement(self.make_row(['Mean', mean]))
		summary_tbl.addElement(self.make_row(['StnDiv', stddiv]))
		summary_tbl.addElement(self.make_row(['StdDiv % of Mean', stddiv_mean]))
		summary_tbl.addElement(self.make_row(['Sum varience', sum_varience]))

		summary_tbl.addElement(self.make_row([]))

		summary_tbl.addElement(self.make_row(['Name', 'Probability of completion','Effort']))

		for p in distribution_data:
			summary_tbl.addElement(self.make_row(p))

		ods.spreadsheet.addElement(summary_tbl)

		ods.spreadsheet.addElement(data_tbl)



		try:
			ods.save(target_file, True)
		except:
			report_error(1, 'Unable to write to "%s", is file open?' % target_file)

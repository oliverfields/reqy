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
from operator import itemgetter
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
		data_tbl.addElement(self.make_row(['Name', 'Best case', 'Likely', 'Worst case', 'Varience', 'Uncertaincy','Mean', 'Delineation']))

		items = 1
		mean = 0
		sum_varience = 0
		est_data = []

		for item in rt.get_tree_items():
			if isinstance(item, Requirement) or isinstance(item, RequirementPackage):

				if item.is_triple_point_estimate(item.estimated_effort):
					items += 1
					triple_points = item.estimated_effort.split('/')
					best_case = float(triple_points[0])
					likely_case = float(triple_points[1])
					worst_case = float(triple_points[2])
				else:
					try:
						report_notice('%s: Estimated effort "%s" is a single point, not triple point estimate (best case/likely/worst case).' % (item._file_path, item.estimated_effort))
						items += 1
						best_case = float(item.estimated_effort)
						likely_case = float(item.estimated_effort)
						worst_case = float(item.estimated_effort)
					except:
						report_error(1, '%s: Estimated effort "%s" is not a valid triple point estimate (best case/likely/worst case).' % (item._file_path, item.estimated_effort))

				varience = float(pow((worst_case-best_case)/6,2))
				sum_varience += varience
				item_mean = float((best_case+4*likely_case+worst_case)/6)
				mean += item_mean

				est_data.append({'name': item._pretty_name, 'best_case': best_case, 'likely': likely_case, 'worst_case': worst_case, 'varience': varience,'mean': item_mean, 'delineation': item.delineation}) 
				#print("%s - %s/%s/%s - %s - %s" % (item._pretty_name, best_case, likely_case, worst_case, varience, item.delineation)) 

		stddiv = float(sqrt(sum_varience))
		stddiv_mean = float(stddiv/mean)

		# Work out % varience of total
		for i in est_data:
			i['varience_of_total'] = float(i['varience']/sum_varience)

		# Sort by uncertaincy
		n = 1
		for i in sorted(est_data, key=itemgetter('varience_of_total'), reverse=True):
			n += 1
			data_tbl.addElement(self.make_row([i['name'], i['best_case'],i['likely'],i['worst_case'],'=((D%s-B%s)/6)^2' % (n,n),"=E%s/'Summary'.$B$4" % n,"=(B%s+4*C%s+D%s)/6" % (n,n,n), i['delineation']]))

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

		# Generate CSV and plot files
		csv_file ='%s.csv' % target_file
		csv = open(csv_file,'w')
		for p in distribution_data:
			csv.write('%s,%s\n' % (p[1],p[2]))

		plot_file ='%s.plot' % target_file
		plot = open(plot_file,'w')
		plot.write("set title 'Project estimated effort at complete'\n")
		plot.write("set xlabel 'Estimated effort'\n")
		plot.write("set ylabel 'Probability of completion %'\n")
		plot.write("set datafile separator ','\n")
		plot.write("set nokey\n")
		plot.write("plot '%s' using 1:2:(1.0) smooth acsplines" % csv_file)

#		print est_data
#		print "Stddiv: %s" % stddiv
#		print "Stddiv mean: %s" % stddiv_mean
#		print "Sum varience: %s" % sum_varience

#		print distribution_data
				#data_tbl.addElement(self.make_row([item._pretty_name, triple_points[0], triple_points[1], triple_points[2], item.estimated_cost]))

		if items == 1:
			sys.exit(0)

		summary_tbl = Table(name="Summary")

		summary_tbl.addElement(self.make_row(['Mean', "=SUM(('Data'.G2:'Data'.G301)"]))
		summary_tbl.addElement(self.make_row(['StnDiv', "=SQRT(B4)"]))
		summary_tbl.addElement(self.make_row(['StdDiv % of Mean', '=B2/B1']))
		summary_tbl.addElement(self.make_row(['Sum varience', "=SUM('Data'.E2:'Data'.E201)"]))

		summary_tbl.addElement(self.make_row([]))

		summary_tbl.addElement(self.make_row(['Name','Effort','Probability of completion']))

		summary_tbl.addElement(self.make_row(['-3SD','=B1-3*B2','1']))
		summary_tbl.addElement(self.make_row(['-2SD','=B1-2*B2','3']))
		summary_tbl.addElement(self.make_row(['-1SD','=B1-B2','16']))
		summary_tbl.addElement(self.make_row(['Mean','=B1','50']))
		summary_tbl.addElement(self.make_row(['+1SD','=B1+B2','85']))
		summary_tbl.addElement(self.make_row(['+2SD','=B1+2*B2','97']))
		summary_tbl.addElement(self.make_row(['+3SD','=B1+3*B2','99']))

		#summary_tbl.addElement(self.make_row([]))
		#summary_tbl.addElement(self.make_row([mean,'effort >>>',"=NORMDIST(A15,B1,B2,1)",'probability project complete']))

		ods.spreadsheet.addElement(summary_tbl)

		ods.spreadsheet.addElement(data_tbl)

		try:
			ods.save(target_file, True)
		except:
			report_error(1, 'Unable to write to "%s", is file open?' % target_file)

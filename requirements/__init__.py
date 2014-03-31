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

import Utility
from ProjectConfig import *
import os
import gettext
import locale
import sys

def init_localization():
	'''prepare l10n'''
	locale_str = locale.getdefaultlocale()[0]
	l10n_file = "%s/requirements/l10n/%s.mo" % (sys.path[0], locale_str)

	try:
		trans = gettext.GNUTranslations(open( l10n_file, "rb" ) )
	except IOError:
		if locale_str != 'en_US':
			Utility.report_warning('Unable to find translation for %s, using default (en_US)' % (locale_str))
		trans = gettext.NullTranslations()

	trans.install(unicode=1)

init_localization()

project = ProjectConfig()
project.load_config_from_file(os.path.join(Utility.get_repo_dir(), 'project.conf'))



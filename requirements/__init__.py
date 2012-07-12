import Utility
from ProjectConfig import *
import os

project = ProjectConfig()
project.load_config_from_file(os.path.join(Utility.get_repo_dir(), 'project.conf'))

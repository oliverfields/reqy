====
reqy
====

----------------------------
Project requirements manager
----------------------------

:Author: Oliver Fields <oliver@phnd.net>
:Date:   2013-02-10
:Version: 0.5
:Manual section: 1
:Manual group: USER COMMANDS 


Synopsis
========

*reqy* [mode] <options>

Must be run from the parent or children repository directories.


Description
===========

Requirements management tool for maintaining a requirements
repository, including traces(links between items), stakeholders
and project documentation. The repository can be visualized via
generated artifacts, such as reports, Requirements Traceability
Matrix or Dependency graphs.

Requirements describe what the done project looks like. Requirements management
is ensuring everyone on the project is working towards the same
done. Reqy allows project requirements to be managed and communicated.


Modes
=====

*check*

  Verify repository is valid.

*new* [glossary|package|requirement(req)|stakeholder] <name>

  Create new repository item based on template.

*init*

  Create new repository in current directory.

*artifact* [all|estimate|graph|list|basiclist|planner|rtm]

  Generate specified artifact in 'artifacts' directory. Option 'all' generates all artifacts.

*trace* [requirement|package|document]

  For the specified item, show traces to and from other repository items.


Files
=====

For description of requirements repository and files, please see reqy(5)


Environment
===========

The following environment variables are used.

*LANG*

  Set generated artifact language


Examples
========

Remember reqy command must be run from within the repository directory or child directories.

Initialize repository:

  reqy init

Generate all requirements:

  reqy artifact all

Generate Norwegian artifacts:

  LANG=nb_NO.UTF-8 reqy artifact all


Bugs and support
================

Please see http://reqy.phnd.net or https://github.com/oliverfields/reqy

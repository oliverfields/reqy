.TH reqy 1  "March 1, 2013" "version 0.5" "FILES"
.SH NAME
reqy \- project requirements manager
.SH FILES
.po files
.TP
.B project.conf
Project configuration file, in root directory of repository.
.TP
.B *.req
Requirement attribute files, located in [repository]/requirements.
.TP
.B attribute.pkg
Requirement package attribute files. Each requirement package consists of a directory that contains an attribute.pkg file. Located in [repository]/requirements.
.TP
.B *.sth
Stakeholder attribute files, located in [repository]/stakeholders.
.TP
.B *.def
Glossary definition files, located in [repository]/glossary.
.TP
.B Templates
Various templates are found in [repository]/templates.

.SH SYNOPSIS
.B reqy
[check|new|init|filter|artifact|trace] <actions>

Must be run from the parent or children repository directories.
.SH DESCRIPTION
Requirements management tool for maintaining a requirements
repository, including traces(links between items), stakeholders
and project documentation. The repository can be visualized via
generated artifacts, such as reports, Requirements Traceability
Matrix or Dependency graphs.
.PP
Requirements describe what the done project looks like. Requirements management
is ensuring everyone on the project is working towards the same
done. Reqy allows project requirements to be managed and communicated.
.SH MODES 
.TP
.B check
Verify repository is valid.
.TP
.B new
[glossary|package|requirement(req)|stakeholder] <name>

Create new repository item based on template.
.TP
.B init
Create new repository in current directory.
.TP
.B filter status
<not> [approved|elaboration|implementation|rejected|postponed]

Filter requirements by status. Use 'not' to invert filter.
.TP
.B artifact
[all|estimate|graph|list|basiclist|planner|rtm]

Generate specified artifact in 'artifacts' directory. Option 'all' generates all artifacts.
.TP
.B  trace
[requirement|package|document]

For the specified item, show traces to and from other repository items.
.SH FILES
.TP
.B project.conf
Project configuration file, in root directory of repository.
.TP
.B *.req
Requirement files. See man 5 reqy
.SH EXAMPLES
.TP
Set the maximum speed to 8 speed cdrom:
.B cdspeed
\-s 8
.PP
.TP
Restore maximum speed:
.B cdspeed
\-s 0
.PP
.SH EXIT STATUS
reqy returns a zero exist status if it succeeds, all non zero returns are failure.
.SH AUTHOR
Oliver Fields <oliver@phnd.net>

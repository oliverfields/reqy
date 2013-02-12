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
:Manual group: CONFIG FILES

Requirement repository
======================

The repository is designed to be portable between operating systems and be human understandable without any tools, whilst lending itself to version control. To achieve these goals, it consists of plain text files, regular directories and optionally any type of file for aiding desciption of the requirement. The following describe the directories.

artifacts
  Contains generated documentation derived from the repository contents
documents
  Documentation required for supporting requirements. The files can be any appropriate file type for describing the design (.doc, .png, .pdf etc). May contain sub folders
glossary
  Definitions of all relevant terms used.
requirements
  Requirement files (.req) or packages (a directory and 'attribute.pkg' file). Requirement packages and requirements. May contain packages (sub folders with attributes.pkg file describing package attributes) or requirements (plain text files with extension .req). See requirement_format.odt package and requirements specification. The requirements link to user, design, acceptance-criteria, test-cases and/or use-cases files.
stakeholders
  Defined stakeholders of the project. Each stakeholder is defined in a single file.



Configuration files
===================

The repository consists of different types of items, each item type has its own configuration file. The types are as follows.
* Project
* Requirement
* Requirement package
* Stakeholder
* Document
* Glossary

All the files consists of key value pairs for setting attributes. White space between the key, colon and value is ignored. Keys are case insensitive. A key value pair can either be single line or multi line. All configuration files share the same syntax.

Single line key values.

  |
  | [key]: [value]

Multi line key values (note that the value lines have double space at start of line).

  |
  | [key]:
  |   [value line 1]
  |   [value line 2]
  |   [value line 3]


Files are named as[id]_[short name].[extension], where [id]_ is an optional reference and [short name] is best thought of as a terse description of the requirement. The file name may contain letters (upper- or lowercase), numbers, underscores(_), hyphens(-) and periods(.).

The prefix [id]_ is optional, but can be handy for reference purposes and describing what package the requirement belongs to, e.g. 1.1 or 2.4.21.


Project
=======

Project attributes.

|
| File name: project.conf
| Directory: [repository]

Name
  Project name
Short name
  Short code/reference for project
Description
  Short description


Requirement - attributes
========================

Requirements describe what is is to be created, implementation details, test cases and detailed design documentation meant to be referenced in other documents.

|
| File extension: .req
| Directory:      [repository]/requirements

Approved by - Mandatory, if status approved
  Can only be set if status is approved. The person that approved the requirement as met
Approved on
  Can only be set if status is approved
Assigned on
  The date format is not configurable
Assigned to
  The person that is responsible for the requirement, must be a valid stakeholder defined in the configuration
Created by
  The person that created the requirement, must be a valid stakeholder  defined in the configuration
Created on
  The date format is not configurable
Description - Mandatory
  Describe what is required, but not intended for describing how the requirement will be met, that is to be done in a separate design document
Depends on
  See below for explanation of link lists
Documents
  See below for explanation of  link lists
Estimated effort
  Estimated duration of work for one person to complete in hours
Estimated cost
  Estimated cost to complete requirement
Note
  Supplemental information
Postponed by
  Can only be set if status is postponed. Person who decided to postpone requirement
Postponed on
  Can only be set if status is postponed
Priority
  Indicate how important the requirement is, see below
Rationale - Mandatory
  Reason for requirement
Rejected by - Mandatory, if status rejected
  Can only be set if status is rejected. Person that rejected requirement, must be valid stakeholder defined in the configuration
Rejected on
  Can only be set if status is rejected. The date format is not configurable
Scope - Mandatory
  Describe how the requirement is deliniated/limited
Status
  See below for list of status codes
Status reason - Mandatory, except if status approved or elaboration
  Explanation why requirement has a given status
Title
  Optional title for requirement, if set will be used instead of generated title
Todo
  List of items that need doing


Requirement - status codes
==========================

elaboration
  Not fully specified/missing information, needs more work
implementation
  Requirement ready for implementation
rejected
  Will not be implemented, if set Rejected by must be set
approved
  Requirement signed off by client, if set Approved by must be set
postponed
  May be implemented at later date, if set Postponed by must be set


Requirement - priority codes
============================

must
  Describes a requirement that must be satisfied in the final solution for the solution to be considered a success
should
  Represents a high-priority item that should be included in the solution if it is possible. This is often a critical requirement but one which can be satisfied in other ways if strictly necessary
could
  Describes a requirement which is considered desirable but not necessary. This will be included if time and resources permit

Requirement - Link list
=======================
The attributes Assigned to, Created by, Depends on, Documents and Rejected by accept a comma separated list of links to the respective files, alternatively the value none may be used to explicitly state that there are no links.

The Documents attribute links to the [repository]/documents directory, whilst the others link to [repository]/stakeholder. The documents directory may be organized by creating additional directories.

The directory separator is always forward slash(/) regardless of host operating system.


Requirement package
===================

Requirement packages consist of a directory containing a attributes.pkg file containing the attributes. The config file is identical to the requirement config files, please see above for details.

|
| File extension: attributes.pkg
| Directory:      [repository]/requirements 


Stakeholder
===========

The stakeholder is intended to be record information about involved people for use recording who decided what and when.

|
| File extension: .sth
| Directory:      [repository]/stakeholders

Email
  Email address
Name
  Stakeholder name
Note
  Notes
Organization
  Employer, group etc
Phone
  Contact number
Role
  Project/stakeholder role


Glossary
========

Glossary definition files for maintaining common project terms/language.

|
| File extension: .def
| Directory:      [repository]/glossary.

Created by
  The person that created the term, must be a valid stakeholder defined in the configuration
Created on
  The date format is not configurable
Definition - Mandatory
  Explanation of term
Note
  Supplemental information
Rejected by - Mandatory if status is rejected
  User that rejected the term, must be valid user defined in the configuration
Rejected on
  The date format is not configurable
Replaced by - Mandatory if status is replaced
  If status is replaced, then replaced by indicates which term or terms have replaced it
Status
  See below for list of status codes
Status reason - Mandatory, except if status approved or elaboration
  Explanation why requirement has a given status
Term - Mandatory
  The term
Todo
  List of items that need doing


Glossary - status codes
=======================

elaboration
  Not fully specified/missing information, needs more work
rejected
  No longer relevant to project
approved
  Term is relevant/in use
replaced
  Term has been replaced by another


Templates
=========

Various templates are found in [repository]/templates. The templates are simply copied verbatim as basis for new configuration files or when generating some artifacts. Basically theses files may be customized to the project.

.. pys3viewer documentation master file, created by
   sphinx-quickstart on Fri Feb 23 00:37:26 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pys3viewer's documentation!
======================================


This project is a module for analyzing files from s3 bucket.


Structure
----------

Directories:

| \docs          | contains documentation generated via sphinx         |
| \tests         | contains tests                                      |
| \venv          | virtual environment                                 |
| \pys3viewer\*  | The actual module for analyzing s3 data             |
| \pys3viewercli | Command line tool to run the module                 |
| \pys3viewerapi | flask rest api for the module                 |
| \pys3viewerui  | Angular4 frontend for pys3viewer                    |
| \jenkins       | helper groovy wrappers for jenkins pipeline as code |
| \ansible       | Ansible playbooks for continuous delivery           |

Files:
| Makefile    | Make commands                 |
| Jenkinsfile | Continuous delivery pipelines |


Tools used
-----------

| Click     | Command line parser             |
| Sphinx    | Documentation                   |
| Flask     | Flask and flask_restful for api |
| Angular 4 | Front End                       |
| Boto3     | For interfacing with AWS        |
| Pylint    | Linting and code quality        |
| Pytest    | Testing                         |


In Consideration:
-----------------

| s3stat              | Amazon log file analyzer                              |
| goaccess            | real time viewing of server logs in different formats |
| aws cognito         | Authentication against external identity providers    |
| aws emr/hadoop      | Map reduce to speed up indexing                       |
| mrjob               | to interface with elastic map reduce                  |



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

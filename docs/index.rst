:github_url: https://github.com/healthbadge/episimmer/tree/master

.. |Test Status| image:: https://github.com/healthbadge/episimmer/actions/workflows/test.yml/badge.svg?branch=master
   :target: https://github.com/healthbadge/episimmer/actions/workflows/test.yml

.. |Documentation Status| image:: https://readthedocs.org/projects/episimmer/badge/?version=latest
   :target: https://episimmer.readthedocs.io/en/latest/?badge=latest

.. |Coverage Status| image:: https://codecov.io/gh/healthbadge/episimmer/branch/additional_se/graph/badge.svg?token=F0BR661MG5
  :target: https://codecov.io/gh/healthbadge/episimmer

.. |License| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
  :target: https://github.com/healthbadge/episimmer/blob/master/LICENSE

.. |PyPI| image:: https://img.shields.io/pypi/v/episimmer
  :target: https://pypi.org/project/episimmer/


|Test Status| |Documentation Status| |Coverage Status| |License| |PyPI|

Episimmer documentation
=====================================

Episimmer is an Epidemic Simulation Platform that aims to provide Decision and Recommendation Support to help answer your questions related
to policies and restrictions during an epidemic. Using simulation techniques widely applied to other fields, we can help schools and colleges
discover and hone the opportunities and optimizations they could make to their COVID-19 strategy.

From the most simple decisions (Which days to be online or offline) to more complex strategies (What restrictions should I put on library use?,
How many times should I test?, Whom do I test?) Episimmer is the tool for the job.

Contents
=====================================

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   userguide/installation
   userguide/quickstart
   userguide/environment
   userguide/diseasemodel
   userguide/policy
   userguide/vulnerability_detection
   userguide/misc


.. toctree::
  :maxdepth: 1
  :caption: Modules

  modules/agent
  modules/location
  modules/read_file
  modules/simulate
  modules/world
  modules/model
  modules/policy
  modules/vulnerability_detection
  modules/utils



.. toctree::
   :maxdepth: 1
   :caption: Useful links


   episimmer @ PyPI <https://pypi.org/project/episimmer/>
   UI <https://episimmer.herokuapp.com/>

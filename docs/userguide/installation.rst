
Installation
=====================================

Prerequisites
---------------

Episimmer requires python 3.7+.

Install using pip
-------------------

If you are using Linux or macOS you can install episimmer from PyPI with pip:

.. code-block:: bash

    pip install episimmer

Install from source
--------------------

Or you can install from source

1. First clone this repository:

  .. code-block:: bash

      git clone https://github.com/healthbadge/episimmer.git

2. Then, to install the package, run the following command inside the episimmer directory:

  .. code-block:: bash

      pip install -e .


3. If you do not have pip you can instead use:

  .. code-block:: bash

      python setup.py install

If you do not have root access, you should add the ``--user`` option to the above lines.


Documentation
---------------

.. include:: ../README.md
    :parser: myst_parser.sphinx_
    :start-line: 2

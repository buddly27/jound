.. _installing:

**********
Installing
**********

.. highlight:: bash

.. note::

    Using :term:`Virtualenv` is recommended when evaluating or running locally.

Installation is simple with `pip <http://www.pip-installer.org/>`_::

    pip install jound

Installing from source
======================

You can also install manually from the source for more control. First obtain a
copy of the source by either downloading the
`zipball <https://github.com/buddly27/jound/archive/master.zip>`_ or
cloning the public repository::

    git clone http://github.com/buddly27/jound.git

Then you can build and install the package into your current Python
environment::

    pip install .

If actively developing, you can perform an editable install that will link to
the project source and reflect any local changes made instantly::

    pip install -e .

.. note::

    If you plan on building documentation and running tests, run the following
    command instead to install required extra packages for development::

        pip install -e .[dev]

Alternatively, just build locally and manage yourself::

    python setup.py build

Building documentation from source
----------------------------------

Ensure you have installed the 'extra' packages required for building the
documentation::

    pip install -e .[doc]

Then you can build the documentation with the command::

    python setup.py build_sphinx

View the result in your browser at::

    file:///path/to/jound/build/doc/html/index.html

Running tests against the source
--------------------------------

Ensure you have installed the 'extra' packages required for running the tests::

    pip install .[test]

Then run the tests as follows::

    python setup.py -q test

You can also generate a coverage report when running tests::

    python setup.py -q test --addopts "--cov --cov-report=html"

View the generated report at::

    file:///path/to/jound/htmlcov/index.html


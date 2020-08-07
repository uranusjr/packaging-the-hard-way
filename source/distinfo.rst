=========================
Describe a Python Package
=========================

The import system is easy to satisfy, but the approach has problems.

* Can't upgrade (there is no version!)
* Manual intervention needed to install/uninstall

To automate the process, we need to provide *metadata* for tools (e.g. pip) to
recognise the package. This is specified in `PEP 376`_.

.. _`PEP 376`: https://www.python.org/dev/peps/pep-0376/

* A ``{name}-{version}.dist-info`` directory to describe an installation.
* ``METADATA`` describes the installed distribution for tools to recognise.
* ``RECORD`` records installed files, so tools can uninstall them later. Note
  that we always use ``/`` in paths.
* ``INSTALLER`` identifies what tool was used to install the distribution, so
  tools don't step on each others' files.

Let's write some code to automate the process.

.. literalinclude:: /../example-project/packager/distinfo.py
    :caption: packager/distinfo.py
    :language: python

Now if we install our package with this script::

    $ py -m packager.distinfo ./my_package /path/to/site-packages

pip would magically recognise our package!

.. code-block:: console

    $ py -m pip list
    Package    Version
    ---------- -------
    my-package 0
    pip        20.2.1
    setuptools 46.0.0
    wheel      0.34.2

.. code-block:: console

    $ py -m pip show my-package
    Name: my-package
    Version: 0
    Summary: None
    Home-page: None
    Author: None
    Author-email: None
    License: None
    Location: /path/to/site-packages
    Requires:
    Required-by:

Note how pip shows our example as ``my-package``, although we defined
``DIST_NAME`` as ``my_package``. The two are actually equivalent according to
`PEP 503`_, and the dash form is called the "normalised" name form. In
practice, you should be able to refer your project anyhow you like---just
remember that pip will conflate the different notation.

.. _`PEP 503`: https://www.python.org/dev/peps/pep-0503/

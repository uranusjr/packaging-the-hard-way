=================================
What is Python Packaging, Anyway?
=================================

1. You have some code that you ``import`` in a Python project.
2. You want other projects to also be able to ``import`` them.

Python packaging helps you to go from 1. to 2.


How does ``import`` work?
=========================

To make code *importable*, the module needs to be in a searchable location
in ``sys.path``:

.. code-block:: pycon

    >>> import os, sys
    >>> for p in sys.path: print(os.path.normpath(p))
    .
    C:\Users\uranusjr\AppData\Local\Programs\Python\Python39\python39.zip
    C:\Users\uranusjr\AppData\Local\Programs\Python\Python39\DLLs
    C:\Users\uranusjr\AppData\Local\Programs\Python\Python39\lib
    C:\Users\uranusjr\AppData\Local\Programs\Python\Python39
    C:\Users\uranusjr\AppData\Local\Programs\Python\Python39\lib\site-packages

The first ``.`` (dot) means the current working directory, which is why you
can directly import other files within a project. Otherwise, The next four
paths contain standard libraries.

The last one, ``site-packages``, is the one third-party libraries are
generally put into.

Let's try that!


Prepare the demo project to distribute
--------------------------------------

::

    example-project/
        my_package/
            __init__.py

.. literalinclude:: /../example-project/my_package/__init__.py
    :caption: my_package/__init__.py
    :language: python

.. code-block:: console

    $ cd /path/to/example-project
    $ py
    >>> import my_package
    >>> my_package.hello()
    Greeting from my package!


Use ``my_package`` in another project
-------------------------------------

::

    other-project/
        main.py

.. code-block:: py
    :caption: main.py

    import my_package
    my_package.hello()

Now try running ``main.py``:

.. code-block:: console

    $ cd /path/to/other-project
    $ py main.py
    Traceback (most recent call last):
      File "main.py", line 1, in <module>
        import my_package
    ModuleNotFoundError: No module named 'my_package'

It does not work. This is expected, since ``my_package`` is not available
anywhere in ``other-project`` and its empty virtual environment.

**The "fix" can be simple: just copy the ``my_package`` directory into
one of the directories in ``sys.path``.**

Generally, third-party packages (i.e. packages that are not a part of the
standard library, and does not belong specifically to a project) are copied
into the ``site-packages`` directory.

We can correctly import the package once it's copied into the environment:

.. code-block:: console

    $ cd /path/to/other-project
    $ py main.py
    Greetings from my package!


Describe the installation
=========================

The import system is easy to satisfy, but the approach has problems.

* Can't upgrade (there is not version!)
* Need manual intervention to be installed/uninstalled

To automate the process, we need to provide *metadata* for tools (e.g. pip) to
recognise the package.

`PEP 376`_ --- Database of Installed Python Distributions
---------------------------------------------------------

* A `{name}-{version}.dist-info` directory to describe an installation.
* `METADATA` describes the installed distribution, so tools can recognise them.
* `RECORD` records installed files, so tools can uninstall them later.
* `INSTALLER` identifies what tool was used to install the distribution, so
  tools don't step on each others' files.

.. _`PEP 376`: https://www.python.org/dev/peps/pep-0376/

Let's write some code to automate the process.

.. literalinclude:: /../home-grown-packager/direct-install.py
    :caption: direct-install.py
    :language: python

Now if we install our package with this script:

.. code-block:: console

    $ py direct-install.py /path/to/example-project /path/to/site-packages

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


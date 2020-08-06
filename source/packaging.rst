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

    $ cd /path/to/my-project
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

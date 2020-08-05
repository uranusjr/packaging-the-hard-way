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

    >>> import sys
    >>> for p in sys.path:
    ...  print(repr(p))

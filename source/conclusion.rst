========================
How Do All These Matter?
========================

In the end, we end up developing a simple `PEP 517`_ backend that can be called
to generate source and wheel distributions. The tool contains code to build

* Wheel
    * Walk the package to include into the wheel
    * ``.dist-info`` to store metadata
        * ``RECORD`` to list files in the include package
        * ``METADATA`` to describe the distribution
        * ``WHEEL`` to describe the wheel itself
* Sdist
    * Walk the package to include into the sdist
    * ``pyproject.toml``

.. _`PEP 517`: https://www.python.org/dev/peps/pep-0517/


The ``packager`` thing we built is practically useless, and you are very
unlikely to ever need it, unless you are either into building very complicated
distributions that require custom packaging and compilation, or are intereted
in developing packaging tools yourself (like myself). The things we walked
through along the way, on the other hand, should be useful for everyone that
distributes Python packages, or aspire to do so.

Python packaging is commonly considered a mess and difficult because the
traditional tool for it, setuptools, is notoriously difficult to understand.
Many people end up copying a bunch of configurations from somewhere, and have
no idea how to change them when something does not work.

It does not need to be like this. setuptools is difficult because it both
contains both a lot of history baggage, and needs to cover many niche functionalities for very complex usages. The modern Python packaging concepts
underneath, however, is relatively simple to understand, and even simpler to
implement.

Open source software often suffers from suboptimal user interaction, and
in a lot of times fails to translate its technologic soundness into ease to
use. Python packaging is very much a victim to this. I hope to help people
understand where the problems lie for Python packaging (and where *not*!) so
we can all spend more focused time to improve them.


Why do tools do what they do?
=============================

Case studies:

* `setup.py`_
* `setup.cfg`_
* `[tool.flit]`_ in pyproject.toml (`example <flit-example_>`_)
* `[tool.poetry]`_ in pyproject.toml (`example <poetry-example_>`_)

.. _`setup.py`:
    https://setuptools.readthedocs.io/en/latest/setuptools.html
    #basic-use
.. _`setup.cfg`:
    https://setuptools.readthedocs.io/en/latest/setuptools.html
    #configuring-setup-using-setup-cfg-files
.. _`[tool.flit]`:
    https://flit.readthedocs.io/en/latest/pyproject_toml.html
.. _flit-example:
    https://github.com/takluyver/flit/blob/master/pyproject.toml
.. _`[tool.poetry]`:
    https://python-poetry.org/docs/pyproject/
.. _poetry-example:
    https://github.com/python-poetry/poetry/blob/master/pyproject.toml


Looking into the future
=======================

* A setuptools wrapper to help the simple use cases?
* More love to existing `PEP 517`_ backends like Poetry and Flit.
    * Binary compilation support is currently lacking.
* More alternative `PEP 517`_ backends.
* Better developer tooling to support `PEP 517`_ backends.

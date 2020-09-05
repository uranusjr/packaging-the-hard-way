================================
Package Python Code the Hard Way
================================

You have Python code to publish. First, create ``setup.py``, and ``setup.cfg``,
``MANIFEST.in``, ``pyproject.toml``… What are all these stuff? Python packaging
is so confusing! In this talk, we are going to throw all them away, and build a
package from the ground up.

Python packaging is not hard. Shocking, I know, but it’s true. An installable
Python package distribution consists of three parts:

1. Things you want to distribute (you already have them).
2. “Core metadata” that describe what you want to distribute.
3. A file format to bundle the above.

This excercise walks through the process of making a Python package
distribution. By doing this, we can have a better idea not only *how* things
are, but more importantly, *why* they are, and understand why different
packaging tools need you to set up certain configurations, and learn to draw
analogies when you need to make changes.

.. toctree::
   :maxdepth: 1

   packaging
   distinfo
   wheel
   pep517
   conclusion


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

=====================================
Turn Your Package into a Distribution
=====================================

What we came up with in ``direct-install.py`` is what package installers like
pip does essentially, if you strip off all its bells and whistles. The
difference is that, pip requires distributions to be a single-file archive,
and structured in a certain way, so it knows exactly what to download and extract, and where to.

The modern format pip uses to install, called "wheels", is specified in
`PEP 427`_. A wheel is a ZIP archive, and is unarchived into ``site-packages``
on installation. (Again, ignoring many bells and whistles that comes along.)
Since Python has built-in ZIP support, we can easily extend our installer
to do this.

.. _`PEP 427`: https://www.python.org/dev/peps/pep-0427/

.. literalinclude:: /../home-grown-packager/wheel.py
    :caption: wheel.py
    :language: python


Anatomy of a wheel
==================

In the above example, the wheel is installed by simply extracted into the
``site-packages`` directory. So the archive contains exactly the same two
components copied by our script in the previous section: *code*, and
*dist-info*.

* Code is exactly the same.
* ``.dist-info`` is named the same.
* ``METADATA`` is exactly the same.
* ``RECORD`` is exactly the same.
* ``INSTALLER`` is not present, since the wheel is not yet installed anywhere.
  pip automatically writes the ``INSTALLER`` value in the installed
  ``.dist-info`` directory when it installs.

There is a new file ``WHEEL`` that contains metadata that describes the 
currently used wheel format itself. We're not getting into this too deep
here since "real" distribution tools handle these automatically for you. Read
the PEP for more information if you're into these stuff.

* The only valid ``Wheel-Version`` value at the current time is ``1.0``.
* ``Generator`` marks the tools that generates the wheel.
* ``Root-Is-Purelib`` describes where the package is installed. This does not
  matter in most situations, but for some Python installations that distinguish
  pure-Python and platform-dependent packages, setting this to ``false`` would
  cause the wheel to be installed under ``dist-packages`` instead.
* ``Tag`` describes what platforms the wheel can be installed. For most
  pure-Python packages, this is always ``py3-none-any`` (or ``py2-`` if it's
  for Python 2), indicating the major Python version, ABI, and platform
  information.

The wheel named as ``{name}-{version}-{tag}.whl``. This helps tools identify
the wheel's compatibility without extracting it, which is useful in network
contexts.

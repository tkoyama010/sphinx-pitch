.. sphinx-pitch documentation master file

sphinx-pitch Documentation
==========================

Welcome to sphinx-pitch's documentation! This extension allows you to create
beautiful slide presentations using Sphinx with GitPitch-compatible syntax.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   syntax
   examples
   api


Live Demo
---------

See a **live presentation** created with sphinx-pitch:

.. toctree::
   :maxdepth: 1

   demo_presentation

:doc:`Click here to view the live demo presentation <demo_presentation>`


Quick Start
-----------

Install the extension:

.. code-block:: bash

   pip install sphinx-pitch

Add it to your Sphinx ``conf.py``:

.. code-block:: python

   extensions = ['sphinx_pitch']

Create your first presentation:

.. code-block:: rst

   .. pitch::

      # Welcome to My Presentation
      [drag=100, drop=center, fit=2.5]

      ---

      # Code Example
      @code[python]
      def hello():
          print("Hello, World!")


Features
--------

- **GitPitch-Compatible Syntax** - Use familiar PITCHME.md-style syntax
- **Grid Layouts** - Position content with pixel-perfect drag/drop syntax
- **Code Presenting** - Highlight and present code with syntax highlighting
- **List Widgets** - Create styled lists with animations
- **Math Formulas** - Display mathematical notation with LaTeX support
- **Speaker Notes** - Add private notes for presenters
- **Responsive Design** - Works on desktop and mobile devices


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Examples
========

This page provides complete working examples of sphinx-pitch presentations.

Live Demo Presentation
----------------------

View a **live, working presentation** created with sphinx-pitch:

:doc:`View Live Demo <demo_presentation>`

This demo showcases all major features including slides, grid layouts,
code widgets, list widgets, math formulas, and speaker notes.

Basic Presentation
------------------

A simple presentation showing core features:

.. code-block:: rst

   .. pitch::
      :theme: default

      # Welcome
      [drag=100, drop=center, fit=2.5]

      ---

      # About
      [drag=50 80, drop=left]

      ## Sphinx-Pitch
      A Sphinx extension for presentations

      [drag=50 80, drop=right]

      ## Features
      - GitPitch compatible
      - Easy to use
      - Powerful

      ---

      # Code
      @code[python, drag=80, drop=center]
      print("Hello, World!")

      ---

      # The End
      [drag=100, drop=center, fit=3.0]

Two-Column Layout
-----------------

Example of side-by-side content:

.. code-block:: rst

   .. pitch::

      # Comparison
      [drag=45 80, drop=left, bg=#f0f0f0]

      ## Before
      - Manual configuration
      - Complex setup
      - Limited options

      [drag=45 80, drop=right, bg=#e0f0e0]

      ## After
      - Simple directives
      - Easy setup
      - Full control

Code Presentation
-----------------

Presenting code with step-by-step highlighting:

.. code-block:: rst

   .. pitch::

      # Algorithm
      [drag=99, drop=center, fit=1.49]

      @code[python]
      def fibonacci(n):
          if n <= 1:
              return n
          return fibonacci(n-1) + fibonacci(n-2)

      @[1](Base case definition)
      @[3-4](Recursive calculation)

      Note:
      - Explain the base case first
      - Then show the recursive step
      - Mention time complexity

Styled Lists
------------

Using different list styles:

.. code-block:: rst

   .. pitch::

      # Features

      @ul[list-spaced-bullets list-fade-bullets, drag=80, drop=center, fit=1.2]
      - **Grid Layouts**: Pixel-perfect positioning
      - **Code Widgets**: Syntax highlighting
      - **Math Support**: LaTeX formulas
      - **Speaker Notes**: Presenter hints
      @ul

Math Formulas
-------------

Displaying mathematical content:

.. code-block:: rst

   .. pitch::

      # Pythagorean Theorem
      [drag=100, drop=center, fit=2.0]

      @math[drag=60, drop=center]
      `\[a^2 + b^2 = c^2\]`
      @math

      ---

      # Quadratic Formula
      [drag=100, drop=center, fit=1.8]

      @math[drag=80, drop=center]
      `\[x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\]`
      @math

Complete Demo Presentation
--------------------------

Below is the source code for the :doc:`live demo presentation <demo_presentation>`:

.. literalinclude:: demo_presentation.rst
   :language: rst

View the :doc:`live presentation here <demo_presentation>`.

Syntax Reference
================

This page provides detailed documentation for all sphinx-pitch syntax features.

Slides
------

Slides are separated by three dashes (``---``):

.. code-block:: rst

   # First Slide
   Content for the first slide

   ---

   # Second Slide
   Content for the second slide


Grid Layouts
------------

Grid layouts allow precise positioning of content using GitPitch-compatible syntax.

Basic Syntax
~~~~~~~~~~~~

.. code-block:: rst

   [drag=WIDTH HEIGHT, drop=X Y, fit=SCALE]

   Your content here

**Attributes:**

- ``drag=WIDTH HEIGHT`` - Block dimensions (percentage like ``50 80`` or pixels like ``500px 400px``)
- ``drop=X Y`` - Position coordinates (percentage or pixels)
- ``drop=POSITION`` - Named positions: ``center``, ``left``, ``right``, ``top``, ``bottom``, ``topleft``, ``topright``, ``bottomleft``, ``bottomright``
- ``fit=SCALE`` - Content scaling (1.0 = normal, 2.0 = double size)
- ``flow=TYPE`` - Layout direction: ``col`` (column), ``row`` (row), ``stack`` (stacked)
- ``bg=COLOR`` - Background color (CSS color value)

Examples
~~~~~~~~

Centered content with 100% width:

.. code-block:: rst

   [drag=100, drop=center, fit=2.5]

   # Big Centered Title

Two-column layout:

.. code-block:: rst

   [drag=50 80, drop=left]

   ## Left Column
   Content on the left

   [drag=50 80, drop=right]

   ## Right Column
   Content on the right

Background color:

.. code-block:: rst

   [drag=60, drop=center, bg=#232B2B]

   ## Dark Themed Content


Code Widgets
------------

Display syntax-highlighted code with the ``@code`` widget.

Syntax
~~~~~~

.. code-block:: rst

   @code[LANGUAGE, drag=WIDTH, drop=POSITION, fit=SCALE]

   your code here

Or reference an external file:

.. code-block:: rst

   @code[python, drag=80, drop=center](path/to/file.py)

Examples
~~~~~~~~

Inline code:

.. code-block:: rst

   @code[python, drag=90, drop=center, fit=1.2]
   def fibonacci(n):
       if n <= 1:
           return n
       return fibonacci(n-1) + fibonacci(n-2)

From file:

.. code-block:: rst

   @code[javascript, drag=80, drop=center](src/app.js)

With line filters:

.. code-block:: rst

   @code[python, drag=80, drop=center](src/example.py?lines=1-10,25-30)


List Widgets
------------

Create styled lists with ``@ul`` (unordered) or ``@ol`` (ordered) widgets.

Syntax
~~~~~~

.. code-block:: rst

   @ul[CLASSES, drag=WIDTH, drop=POSITION, fit=SCALE]
   - Item 1
   - Item 2
   - Item 3
   @ul

**Classes:**

- ``list-spaced-bullets`` - Add spacing between items
- ``list-fade-bullets`` - Apply fade effect to items
- ``list-square-bullets`` - Use square bullets

Examples
~~~~~~~~

Basic unordered list:

.. code-block:: rst

   @ul[list-spaced-bullets]
   - First feature
   - Second feature
   - Third feature
   @ul

Styled ordered list:

.. code-block:: rst

   @ol[list-square-bullets list-spaced-sm-bullets, drag=60, drop=center]
   1. Step one
   2. Step two
   3. Step three
   @ol


Math Widgets
------------

Display mathematical formulas using LaTeX syntax.

Syntax
~~~~~~

.. code-block:: rst

   @math[drag=WIDTH, drop=POSITION, fit=SCALE]

   `\[YOUR LATEX FORMULA\]`

   @math

Examples
~~~~~~~~

Einstein's famous equation:

.. code-block:: rst

   @math[drag=60, drop=center, fit=2.0]
   `\[E = mc^2\]`
   @math

Complex formula:

.. code-block:: rst

   @math[drag=80, drop=center, pad=30px]
   `\[
   \left( \sum_{k=1}^n a_k b_k \right)^{\!\!2} \leq
   \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
   \]`
   @math


Speaker Notes
-------------

Add private notes for presenters that are not visible to the audience.

Syntax
~~~~~~

.. code-block:: rst

   # Slide Title
   Content visible to audience

   Note:
   - This note is only visible to the presenter
   - Remind yourself of key talking points
   - Add timing reminders

The notes section starts with ``Note:`` and continues until the next slide or special element.


Complete Example
----------------

Here's a complete presentation example:

.. code-block:: rst

   .. pitch::
      :theme: default
      :transition: slide

      # Welcome to Sphinx-Pitch
      [drag=100, drop=center, fit=2.5]

      ---

      # Features
      [drag=40 80, drop=left, fit=1.2]

      @ul[list-spaced-bullets list-fade-bullets]
      - GitPitch-compatible syntax
      - Grid layouts with drag/drop
      - Code presenting
      - Speaker notes
      @ul

      [drag=60 80, drop=right]

      ## Perfect for developers!

      ---

      # Code Example
      [drag=99, drop=center, fit=1.5]

      @code[python, drag=80, drop=center]
      def hello_world():
          print("Hello from Sphinx-Pitch!")
          return True

      Note:
      - Mention the syntax highlighting
      - Point out the grid positioning
      - Demo the live code presenting

      ---

      # Thank You!
      [drag=100, drop=center, fit=3.0]

      ## Questions?

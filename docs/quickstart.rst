Quick Start
===========

Installation
------------

Install sphinx-pitch using pip:

.. code-block:: bash

   pip install sphinx-pitch

Or install from source:

.. code-block:: bash

   git clone https://github.com/tetsuo-koyama/sphinx-pitch.git
   cd sphinx-pitch
   pip install -e .


Configuration
-------------

Add ``sphinx_pitch`` to your Sphinx ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinx_pitch',
       # ... other extensions
   ]

   # Optional: Configure pitch settings
   pitch_theme = 'default'
   pitch_transition = 'slide'


Your First Presentation
-----------------------

Create a presentation using the ``pitch`` directive:

.. code-block:: rst

   .. pitch::
      :theme: default
      :transition: slide

      # Welcome to My Presentation
      [drag=100, drop=center, fit=2.5]

      ---

      # Code Example
      [drag=99, drop=center, fit=1.5]

      @code[python]
      def hello():
          print("Hello, World!")

      ---

      # Thank You!
      [drag=100, drop=center, fit=3.0]

Build your documentation:

.. code-block:: bash

   make html

View your presentation by opening ``_build/html/index.html`` in a web browser.


Next Steps
----------

- Learn about :doc:`syntax` for detailed syntax reference
- See :doc:`examples` for complete working examples
- Check :doc:`api` for API documentation

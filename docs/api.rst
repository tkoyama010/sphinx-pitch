API Reference
=============

This page documents the sphinx-pitch API for developers.

Extension Module
----------------

.. automodule:: sphinx_pitch
   :members:
   :undoc-members:
   :show-inheritance:

Directives
----------

PitchDirective
~~~~~~~~~~~~~~

.. autoclass:: sphinx_pitch.PitchDirective
   :members:
   :undoc-members:
   :show-inheritance:

Nodes
-----

PitchNode
~~~~~~~~~

.. autoclass:: sphinx_pitch.PitchNode
   :members:
   :undoc-members:
   :show-inheritance:

SlideNode
~~~~~~~~~

.. autoclass:: sphinx_pitch.SlideNode
   :members:
   :undoc-members:
   :show-inheritance:

GridBlockNode
~~~~~~~~~~~~~

.. autoclass:: sphinx_pitch.GridBlockNode
   :members:
   :undoc-members:
   :show-inheritance:

CodeWidgetNode
~~~~~~~~~~~~~~

.. autoclass:: sphinx_pitch.CodeWidgetNode
   :members:
   :undoc-members:
   :show-inheritance:

ListWidgetNode
~~~~~~~~~~~~~~

.. autoclass:: sphinx_pitch.ListWidgetNode
   :members:
   :undoc-members:
   :show-inheritance:

MathWidgetNode
~~~~~~~~~~~~~~

.. autoclass:: sphinx_pitch.MathWidgetNode
   :members:
   :undoc-members:
   :show-inheritance:

NoteNode
~~~~~~~~

.. autoclass:: sphinx_pitch.NoteNode
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
-------------

The following configuration values can be set in your Sphinx ``conf.py``:

.. list-table::
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``pitch_theme``
     - ``'default'``
     - Theme for presentations
   * - ``pitch_transition``
     - ``'slide'``
     - Slide transition type

Functions
---------

setup
~~~~~

.. autofunction:: sphinx_pitch.setup

Visitor Functions
~~~~~~~~~~~~~~~~~

.. autofunction:: sphinx_pitch.visit_pitch_node

.. autofunction:: sphinx_pitch.depart_pitch_node

.. autofunction:: sphinx_pitch.visit_slide_node

.. autofunction:: sphinx_pitch.depart_slide_node

.. autofunction:: sphinx_pitch.visit_grid_block_node

.. autofunction:: sphinx_pitch.depart_grid_block_node

.. autofunction:: sphinx_pitch.visit_code_widget_node

.. autofunction:: sphinx_pitch.depart_code_widget_node

.. autofunction:: sphinx_pitch.visit_list_widget_node

.. autofunction:: sphinx_pitch.depart_list_widget_node

.. autofunction:: sphinx_pitch.visit_math_widget_node

.. autofunction:: sphinx_pitch.depart_math_widget_node

.. autofunction:: sphinx_pitch.visit_note_node

.. autofunction:: sphinx_pitch.depart_note_node

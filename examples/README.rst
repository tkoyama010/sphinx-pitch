Sphinx Pitch Example
====================

This directory contains example presentations created with sphinx-pitch.

Files
-----

- ``basic_presentation.rst`` - A basic presentation showing all features

Usage
-----

To build the example documentation:

1. Install sphinx-pitch::

    pip install -e ..

2. Create a Sphinx documentation project::

    sphinx-quickstart docs

3. Add ``sphinx_pitch`` to your ``conf.py`` extensions::

    extensions = ['sphinx_pitch']

4. Copy the example files to your docs directory and build::

    make html

Features Demonstrated
---------------------

The basic_presentation.rst example shows:

- Slide delimiters (---)
- Grid layout blocks with [drag=X, drop=Y, fit=Z] syntax
- Title and subtitle formatting
- Code widgets (@code)
- List widgets with styles (@ul, @ol)
- Math formulas (@math)
- Speaker notes (Note:)

GitPitch Compatibility
----------------------

This extension supports the following GitPitch features:

- PITCHME.md-style slide decks
- Grid layouts (drag, drop, fit, flow)
- Code presenting widgets
- List widgets with styling
- Math widgets for formulas
- Speaker notes

For more information, see the main README.md file.

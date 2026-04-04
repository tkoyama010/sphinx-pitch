# Minimal Sphinx configuration
import os

project = "sphinx-pitch"
extensions = ["sphinx_revealjs", "sphinx_pitch"]
master_doc = "index"
exclude_patterns = ["_build"]

# Static path for custom CSS files
# Add sphinx_pitch static files explicitly
import sphinx_pitch

html_static_path = [os.path.join(os.path.dirname(sphinx_pitch.__file__), "static")]

# Grid size for pitch presentations (in pixels)
pitch_grid_size = 20

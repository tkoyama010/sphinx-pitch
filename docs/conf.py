# Minimal Sphinx configuration
import os

project = "sphinx-pitch"
extensions = ["sphinx_revealjs", "sphinx_pitch"]
master_doc = "index"
exclude_patterns = ["_build"]

# Static path for custom CSS files (html builder)
# Add sphinx_pitch static files explicitly
import sphinx_pitch

html_static_path = [os.path.join(os.path.dirname(sphinx_pitch.__file__), "static")]

# Static path for revealjs builder (sphinx-revealjs uses this instead of html_static_path)
revealjs_static_path = html_static_path.copy()

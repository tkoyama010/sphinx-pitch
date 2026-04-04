# sphinx-pitch

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Sphinx 3.0+](https://img.shields.io/badge/sphinx-3.0+-green.svg)](https://www.sphinx-doc.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)

A Sphinx extension for creating presentations with **GitPitch-compatible syntax**.

sphinx-pitch allows you to create beautiful slide presentations using Sphinx and reStructuredText with **GitPitch-compatible markdown syntax**. It brings the power of GitPitch's presentation features to the Sphinx ecosystem.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Examples](#examples)
- [GitPitch Compatibility](#gitpitch-compatibility)
- [Acknowledgments](#acknowledgments)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)

## Install

```bash
pip install sphinx-pitch
```

Or install from source:

```bash
git clone https://github.com/tetsuo-koyama/sphinx-pitch.git
cd sphinx-pitch
pip install -e .
```

## Usage

1. Add `sphinx_pitch` to your Sphinx `conf.py`:

```python
extensions = [
    'sphinx_pitch',
    # ... other extensions
]
```

2. Create a presentation using the `pitch` directive:

```rst
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
```

3. Build your documentation:

```bash
make html
```

## Features

- **GitPitch-Compatible Syntax** - Use familiar PITCHME.md-style syntax
- **Grid Layouts** - Position content with pixel-perfect drag/drop syntax
- **Code Presenting** - Highlight and present code with syntax highlighting
- **List Widgets** - Create styled lists with animations
- **Math Formulas** - Display mathematical notation with LaTeX support
- **Speaker Notes** - Add private notes for presenters
- **Responsive Design** - Works on desktop and mobile devices

## Configuration

Add these settings to your `conf.py`:

```python
# Theme selection
pitch_theme = 'default'

# Slide transition type
pitch_transition = 'slide'
```

## Examples

See the [documentation](https://sphinx-pitch.readthedocs.io/) for complete working examples:

- [Live Demo](https://sphinx-pitch.readthedocs.io/en/latest/demo_presentation.html) - Complete feature demonstration
- [Examples Page](https://sphinx-pitch.readthedocs.io/en/latest/examples.html) - More code examples

## GitPitch Compatibility

This extension supports the following GitPitch features:

- Slide delimiters (`---`)
- Grid layouts (`[drag=, drop=, fit=, flow=]`)
- Named positions (center, left, right, top, bottom, etc.)
- Code widgets (`@code[language]`)
- List widgets (`@ul`, `@ol`)
- Math widgets (`@math`)
- Speaker notes (`Note:`)
- Background colors (`bg=`)
- Pixel and percentage units

## Acknowledgments

- Inspired by [GitPitch](https://github.com/gitpitch/gitpitch) - The original markdown presentation service
- Built for [Sphinx](https://www.sphinx-doc.org/) - Python documentation generator
- Thanks to all contributors!

## Support

- Issues: [GitHub Issues](https://github.com/tetsuo-koyama/sphinx-pitch/issues)
- Discussions: [GitHub Discussions](https://github.com/tetsuo-koyama/sphinx-pitch/discussions)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with for the Sphinx and GitPitch communities.

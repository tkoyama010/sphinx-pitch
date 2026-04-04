# sphinx-pitch

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Sphinx 3.0+](https://img.shields.io/badge/sphinx-3.0+-green.svg)](https://www.sphinx-doc.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Sphinx extension for creating presentations with **GitPitch-compatible syntax**.

sphinx-pitch allows you to create beautiful slide presentations using Sphinx and reStructuredText with **GitPitch-compatible markdown syntax**. It brings the power of GitPitch's presentation features to the Sphinx ecosystem.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Features](#features)
- [Syntax Reference](#syntax-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [GitPitch Compatibility](#gitpitch-compatibility)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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

## Syntax Reference

### Slides

Slides are separated by `---` (three dashes):

```rst
# First Slide
Content here

---

# Second Slide
More content
```

### Grid Layouts

Position content with GitPitch-style grid syntax:

```rst
[drag=50 80, drop=left, fit=1.2]

## Left Column
Content positioned on the left

[drag=50 80, drop=right]

## Right Column
Content positioned on the right
```

**Attributes:**
- `drag=WIDTH HEIGHT` - Set block dimensions (percentage or pixels)
- `drop=X Y` or `drop=POSITION` - Set position (center, left, right, top, bottom, etc.)
- `fit=SCALE` - Scale content (1.0 = normal, 2.0 = double, etc.)
- `flow=col|row|stack` - Layout direction
- `bg=COLOR` - Background color

### Code Widgets

Display syntax-highlighted code:

```rst
@code[python, drag=80, drop=center, fit=1.2](path/to/file.py)
```

Or inline:

```rst
@code[python]
def example():
    return True
```

### List Widgets

Create styled lists:

```rst
@ul[list-spaced-bullets list-fade-bullets]
- First item
- Second item
- Third item
@ul
```

**List Styles:**
- `list-spaced-bullets` - Add spacing between items
- `list-fade-bullets` - Fade effect on items
- `list-square-bullets` - Use square bullets

For ordered lists, use `@ol` instead of `@ul`.

### Math Formulas

Display mathematical notation:

```rst
@math[drag=60, drop=center, fit=2.0]
`\[E = mc^2\]`
@math
```

### Speaker Notes

Add notes for presenters:

```rst
# Slide Title
Content visible to audience

Note:
- This note is only visible to the presenter
- Remind them of key points
```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by [GitPitch](https://github.com/gitpitch/gitpitch) - The original markdown presentation service
- Built for [Sphinx](https://www.sphinx-doc.org/) - Python documentation generator
- Thanks to all contributors!

## Support

- Issues: [GitHub Issues](https://github.com/tetsuo-koyama/sphinx-pitch/issues)
- Discussions: [GitHub Discussions](https://github.com/tetsuo-koyama/sphinx-pitch/discussions)

---

Made with for the Sphinx and GitPitch communities.

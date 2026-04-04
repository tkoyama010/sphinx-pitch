# sphinx-pitch

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Sphinx 3.0+](https://img.shields.io/badge/sphinx-3.0+-green.svg)](https://www.sphinx-doc.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)

A Sphinx extension for creating presentations with **[GitPitch](https://github.com/gitpitch/gitpitch)-compatible syntax**.

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

Add `sphinx_pitch` to your Sphinx `conf.py`:

```python
extensions = [
    'sphinx_pitch',
]
```

Then create presentations using the `pitch` directive.

See the [documentation](https://sphinx-pitch.readthedocs.io/) for complete usage examples.

## Contributing

PRs accepted.

## License

MIT © Tetsuo Koyama

[![Python Versions][python-shield]][python-url]
<!-- [![PyPi][pypi-shield]][pypi-url] -->
[![Tests][tests-shield]][tests-url]
[![License][license-shield]][license-url]
[![Contributors][contributors-shield]][contributors-url]
[![Code Style][codestyle-shield]][codestyle-url]
[![Homepage][homepage-shield]][homepage-url]


# PTE-XDF - Python tools for electrophysiology

PTE-XDF is a python package for working with XDF files in electrophysiology.

It provides an interface to load and work with XDF files in [MNE](https://mne.tools/).

Currently, it is only tested with files that were recorded with TMSi amplifiers.

## Documentation

See the full documentation [here](https://richardkoehler.github.io/pte-xdf/).

For a quick start continue reading.

## Installing pte-xdf


### Stable release

To install the latest stable release, simply type:

```bash
$ pip install pte-xdf
```

### <a name="dev"></a>Development version

To install the latest development version, first clone this repository:

```bash
$ git clone https://github.com/richardkoehler/pte-xdf
```

Then install with the command:

```bash
$ pip install .
```

## Usage

```python
import pte_xdf

fname = "my_recording.xdf"
```

Load a recording and use only the stream with 'stream_id' = 1.

```python
raw = pte_xdf.read_raw_xdf(fname=fname, stream_picks=1, verbose=False)
```

Load a recording and use only the stream with 'name' = 'SAGA'.

```python
raw = pte_xdf.read_raw_xdf(fname, stream_picks='SAGA', verbose=False)
```

## Contributing

Please feel free to contribute yourselves or to open an [issue](issues-url) when you encounter a bug or to request a new feature.

For any major changes, make sure to open an [issue][issues-url] first. 

For any minor additions or bugfixes, you may simply create a **pull request**. 

When you then create a pull request, be sure to **link the pull request** to the open issue in order to close the issue automatically after merging.

### How to contribute
To contribute yourselves, create a fork of this repository and run `git clone https://github_link_to_fork` as described [above](#dev).

Then create a development branch from your fork.

Navigate to the folder where the repository was cloned. 

From your development branch run the command:

```bash
$ pip install -e .[dev]
```

This will additionally install packages for development, such as black, pylint, mypy and isort.

When you have finished working on your changes, you can then create a pull request to this repository.

## License
PTE Stats is licensed under the [MIT license](license-url).

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/static/v1?label=Python&message=3.10&logoColor=black&labelColor=grey&color=blue
[python-url]: https://pypi.org/project/pte-xdf/
[pypi-shield]: https://img.shields.io/static/v1?label=PyPi&message=v0.1.0&logoColor=black&labelColor=grey&color=blue
[pypi-url]: https://pypi.org/project/pte-xdf/
[tests-shield]: https://github.com/richardkoehler/pte-xdf/actions/workflows/tests.yml/badge.svg
[tests-url]: https://github.com/richardkoehler/pte-xdf/actions/workflows/tests.yml
[homepage-shield]: https://img.shields.io/static/v1?label=Homepage&message=ICN&logoColor=black&labelColor=grey&color=9cf
[homepage-url]: https://www.icneuromodulation.org/
[contributors-shield]: https://img.shields.io/github/contributors/richardkoehler/pte-xdf.svg
[contributors-url]: https://github.com/richardkoehler/pte-xdf/graphs/contributors
[license-shield]: https://img.shields.io/static/v1?label=License&message=MIT&logoColor=black&labelColor=grey&color=yellow
[license-url]: https://github.com/richardkoehler/pte-xdf/blob/main/LICENSE/
[codestyle-shield]: https://img.shields.io/static/v1?label=CodeStyle&message=black&logoColor=black&labelColor=grey&color=black
[codestyle-url]: https://github.com/psf/black
[issues-url]: https://github.com/richardkoehler/pte-xdf/issues

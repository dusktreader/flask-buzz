[![Latest Version](https://img.shields.io/pypi/v/flask-buzz?label=pypi-version&logo=python&style=plastic)](https://pypi.org/project/flask-buzz/)
[![Python Versions](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fdusktreader%2Fflask-buzz%2Fmain%2Fpyproject.toml&style=plastic&logo=python&label=python-versions)](https://www.python.org/)
[![Build Status](https://github.com/dusktreader/flask-buzz/actions/workflows/main.yaml/badge.svg)](https://github.com/dusktreader/flask-buzz/actions/workflows/main.yaml)
[![Documentation Status](https://github.com/dusktreader/flask-buzz/actions/workflows/docs.yml/badge.svg)](https://dusktreader.github.io/flask-buzz/)

# flask-buzz

_py-buzz bindings specifically for flask applications_

This is an extension of the [py-buzz](https://github.com/dusktreader/py-buzz) package.

It adds extra functionality especially for flask. Predominately, it adds the ability to register an error handler with
Flask that will automatically package any handled `FlaskBuzz` exceptions in a nicely formatted JSON response with the
appropriate `status_code` and message. There is also a method to explicitly `jsonify` a FlaskBuzz error with some
control over what is included in the error body.

## Super-quick Start

Requires: Python 3.10 to 3.13

Install through pip:

```bash
pip install flask-buzz
```

Minimal usage example: [examples/basic.py](https://github.com/dusktreader/flask-buzz/tree/master/examples/basic.py)


## Documentation

The complete documentation can be found at the
[flask-buzz home page](https://github.dusktreader.io/flask-buzz)

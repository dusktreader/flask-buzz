# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## v4.0.0 - 2025-03-28
- Handled errors do not include full messages that might expose internal info (unless debug mode is activated)
- Handled errors do not include the error or headers (unless debug mode is activated)
- Default status code changed to 500
- Dropped support for Flask-Restx -- This may re-appear as a new project `flask-restx-buzz`
- Migration to uv for package management instead of Poetry
- Migration to MakedocsMaterial instead of Sphinx
- Documentation moved to Github pages


## v3.1.0 - 2024-03-08
- Updated to allow Flask 3.0

## v3.0.0 - 2023-11-28
- Dropped support for python 3.6 and 3.7
- Updated py-buzz dependency to 3.0 or greater.

## v2.0.1 - 2021-11-23
- Added flask 2.0 support
- Removed explicit werkzeug dependency

## v2.0.0 - 2021-06-17
- Removed support for flask-restplus and moved to flask-restx

## v1.0.0 - 2021-01-26
- Updated dependency to py-buzz 2.0
- Dropped support for python 3.5
- Added black and isort pre-commit hooks
- Pinned werkzeug dependency to 0.16.1

## v0.1.14 - 2019-04-12
- Fixed documentation building on readthedocs

## v0.1.10 - 2019-04-12
- Fixed travis secrets

## v0.1.9 - 2019-04-12
- Added a new 'features' page to documentation
- Added several new examples
- Converted project to use poetry
- Dropped support for python 3.4

## v0.1.8 - 2019-03-21
- Patched error handling for flask-restplus
- Added example for flask-restplus

## v0.1.7 - 2018-05-18
- A release number got lost in here somehow
- Made error handler helpers class methods of FlaskBuzz

## v0.1.5 - 2018-05-18
- Added helper methods for flask-restplus
- Deprecated error_handler
- Added build_error_handler

## v0.1.4 - 2018-05-09
- Fixed badges on README
- Fixed long description on pypi
- Added support for python 3.4 - 3.7

## v0.1.4 - 2018-05-02
- Fixed issue with flask1.0 and jsonify overriding headers

## v0.1.3 - 2017-10-04
- Fixed __str__ again

## v0.1.2 - 2017-10-04
- Fixed MANIFEST.in

## v0.1.1 - 2017-10-04
- fixed __str__ method

## v0.1.0 - 2017-10-04
- First release of flask-buzz
- Added this CHANGELOG
- README providing a brief overview of the project
- Docs for basic usage
- Basic example

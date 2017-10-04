Quickstart
==========

Requirements
------------

* Python 3

Note on Requirements
....................

There are not currently plans to support python 2. It might be a nice-to-have,
but there are enough other features to work on at the moment.
Additionally, the original author is a proponent of python 3 adoption.

Installation
------------

Install from pypi
.................
This will install the latest release of py-buzz from pypi via pip::

$ pip install flask-buzz

Install latest version from github
..................................
If you would like a version other than the latest published on pypi, you may
do so by cloning the git repostiory::

$ git clone https://github.com/dusktreader/flask-buzz.git

Next, checkout the branch or tag that you wish to use::

$ cd flask-buzz
$ git checkout integration

Finally, use pip to install from the local directory::

$ pip install .

.. note::

   flask-buzz setup is not tested with distutils or setuptools. pip is a really
   complete package manager and has become the de-facto standard for installing
   python packages from remote locations. Compatability with pip is of primary
   importance, and since pip is such a great tool, it makes the most sense to
   the original author to use pip for local installs as well.

Using
-----
See `examples/basic.py
<https://github.com/dusktreader/flask-buzz/tree/master/examples/basic.py>`_
for an example of how to use this exception package.

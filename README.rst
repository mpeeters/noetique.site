=============
noetique.site
=============

Plone Product for http://www.noetique.eu web site.

Development
-----------

::

    git clone https://github.com/sverbois/noetique.site.git
    cd noetique.site
    virtualenv-2.7 .
    ./bin/pip install -U setuptools
    ./bin/pip install -U pip
    ./bin/pip install zc.buildout
    ./bin/buildout -c development
    ./bin/instance fg

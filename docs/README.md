# Docs

Hosted on [readthedocs](https://notflix.readthedocs.io/en/latest/index.html).

Build it with:

``` bash
make clean;
sphinx-apidoc ../src -o source;
sphinx-build source build;
```
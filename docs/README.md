# Docs


``` bash
make clean;
SPHINX_APIDOC_OPTIONS=members sphinx-apidoc ../src -o source;
sphinx-build source build
```
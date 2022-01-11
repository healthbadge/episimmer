# Building Documentation

To build the documentation:

1. Install episimmer with command -

```
pip install -e .[test]
```

Note: Some shells such as Zsh require quotation marks around brackets, i.e. pip install 'stable-baselines3[extra]'

2. Generate the documentation file via:

```
cd docs
make html
```

The documentation is now available to view by opening `docs/_build/html/index.html`.

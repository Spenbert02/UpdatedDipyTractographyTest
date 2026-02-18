# steps to use the forked version of dipy
1) install python 3.10.x (release is [here](https://www.python.org/downloads/release/python-31019/))
2) download this repository
```
git clone https://github.com/Spenbert02/UpdatedDipyTractographyTest.git
```
3) clone the spenbert02/dipy repo [here](https://github.com/Spenbert02/dipy)
4) run the following commands:
```
cd dipy
pip install -r requirements.txt
pip install wheel setuptools
pip install . --no-build-isolation
```

Notes:
1) if any errors of the form `No module named <module_name>` pop up, run `pip install <module_name>` to install them
2) any dipy imports might be "unrecognized" by vscode (ie, "import dipy" would be underlined in yellow), but you should still be able to import and use dipy. It just doesn't like using the python package this way.

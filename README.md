# steps to use the forked version of dipy
1) uninstall any existing versions of dipy
2) clone the forked dipy repo [here](https://github.com/Spenbert02/dipy) into main directory of project
3) run "pip install -r requirements.txt" in the dipy directory (not the dipy/dipy subfolder)
4) run "./setup.py install" in the dipy directory
5) add the full path of the dipy/dipy subfolder to the system PATH variable
    - "<full_path>...dipy/dipy"
6) you can now refer to dipy in external code

note 1: if any errors of the form

    No module named '<module_name>'

pop up, just run "pip install <module_name>" to install them

note 2: any dipy imports might be "unrecognized" by vscode (ie, "import dipy" would be underlined in yellow), but you should still be able to import and use dipy. It just doesn't like using the python package this way.

# Lab 3: Caesar and RSA desktop apps

Both desktop apps use interfaces generated from the Qt Designer forms in `ui/`.
After editing a `.ui` form in Qt Designer, save it and regenerate its Python
interface from the repository root:

```powershell
C:\Users\khaik\anaconda3\Scripts\pyuic5.exe -x .\lab-03\ui\caesar.ui -o .\lab-03\ui\caesar.py
C:\Users\khaik\anaconda3\Scripts\pyuic5.exe -x .\lab-03\ui\rsa.ui -o .\lab-03\ui\rsa.py
```

## Run from the `ui` directory

Open three terminals in `lab-03\ui` and run one command in each:

```powershell
.\run_api.bat
```

```powershell
.\run_caesar.bat
```

```powershell
.\run_rsa.bat
```

The same launchers can be run from another directory by specifying their path.
For example, from the repository root:

```powershell
.\lab-03\ui\run_api.bat
.\lab-03\ui\run_caesar.bat
.\lab-03\ui\run_rsa.bat
```

The launchers prefer the active Conda environment, then Anaconda or Miniconda
installed under the current user's profile, and finally `python` on `PATH`.
Install the packages in `requirements.txt` in the selected environment before
running.

Generate RSA keys from the RSA app before using its encryption or signature
features.

Run the tests from `lab-03`:

```powershell
python -m unittest discover -s .\tests -v
```

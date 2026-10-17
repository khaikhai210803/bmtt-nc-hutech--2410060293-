# Lab 3: Caesar and RSA desktop apps

Both desktop apps use interfaces generated from the Qt Designer forms in `ui/`.
After editing a `.ui` form in Qt Designer, save it and regenerate its Python
interface from the repository root:

```powershell
C:\Users\khaik\anaconda3\Scripts\pyuic5.exe -x .\lab-03\ui\caesar.ui -o .\lab-03\ui\caesar.py
C:\Users\khaik\anaconda3\Scripts\pyuic5.exe -x .\lab-03\ui\rsa.ui -o .\lab-03\ui\rsa.py
```

## Run the Caesar exercise (Lab 2 API + Lab 3 desktop)

Open two terminals in `lab-03\ui`:

```powershell
.\run_caesar_api.bat
```

```powershell
.\run_caesar.bat
```

The Caesar desktop calls the API implemented in `lab-02/api.py`, reusing the
Caesar cipher from Lab 2.

## Run the RSA exercise (Lab 3 API + Lab 3 desktop)

Open two terminals in `lab-03\ui`:

```powershell
.\run_api.bat
```

```powershell
.\run_rsa.bat
```

Both APIs use port 5000. Stop the API for one exercise before starting the API
for the other exercise.

The launchers can also be run from the repository root:

```powershell
.\lab-03\ui\run_caesar_api.bat
.\lab-03\ui\run_caesar.bat
.\lab-03\ui\run_api.bat
.\lab-03\ui\run_rsa.bat
```

The launchers prefer the active Conda environment, then Anaconda or Miniconda
installed under the current user's profile, and finally `python` on `PATH`.
Install the packages in the corresponding `requirements.txt` before running.

Generate RSA keys from the RSA app before using its encryption or signature
features.

Run the API tests from each lab directory:

```powershell
cd .\lab-02
python -m unittest discover -s .\tests -v
cd ..\lab-03
python -m unittest discover -s .\tests -v
```

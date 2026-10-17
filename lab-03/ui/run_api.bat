@echo off
setlocal
set "LAB_DIR=%~dp0.."
set "PYTHON="

if defined CONDA_PREFIX if exist "%CONDA_PREFIX%\python.exe" set "PYTHON=%CONDA_PREFIX%\python.exe"
if not defined PYTHON if exist "%USERPROFILE%\anaconda3\python.exe" set "PYTHON=%USERPROFILE%\anaconda3\python.exe"
if not defined PYTHON if exist "%USERPROFILE%\miniconda3\python.exe" set "PYTHON=%USERPROFILE%\miniconda3\python.exe"
if not defined PYTHON set "PYTHON=python"

pushd "%LAB_DIR%"
"%PYTHON%" "%LAB_DIR%\api.py"
set "EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %EXIT_CODE%

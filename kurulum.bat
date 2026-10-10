@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
set "NICKSCAN_MODE=install"
set "NICKSCAN_PY="
set "NICKSCAN_ARGS="
set "PYTHONHOME="
set "PYTHONPATH="
set "PYTHONSTARTUP="
set "PYLAUNCHER_ALLOW_INSTALL="
set "PYLAUNCHER_ALWAYS_INSTALL="
pushd "%~dp0"
if errorlevel 1 goto folder_error
if not exist "nickscan.py" goto missing_files
if not exist "kurulum.py" goto missing_files

py -3.12 -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
if not errorlevel 1 goto py312
py -3.11 -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
if not errorlevel 1 goto py311
py -3 -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
if not errorlevel 1 goto py3

for %%V in (312 311) do (
    for %%P in ("%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" "%ProgramFiles%\Python%%V\python.exe" "%ProgramW6432%\Python%%V\python.exe") do (
        if exist "%%~P" (
            "%%~P" -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
            if not errorlevel 1 set "NICKSCAN_PY=%%~P"
        )
    )
)
if defined NICKSCAN_PY goto execute

for %%N in (python.exe python3.exe) do (
    for /f "delims=" %%P in ('where %%N 2^>nul') do (
        if /i not "%%~dpP"=="%LOCALAPPDATA%\Microsoft\WindowsApps\" (
            "%%~P" -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
            if not errorlevel 1 set "NICKSCAN_PY=%%~P"
        )
    )
)
if defined NICKSCAN_PY goto execute

for %%K in ("HKCU\Software\Python" "HKLM\Software\Python" "HKLM\Software\WOW6432Node\Python") do (
    for /f "tokens=2,*" %%A in ('reg query "%%~K" /s /v ExecutablePath 2^>nul') do (
        if /i "%%A"=="REG_SZ" if exist "%%B" (
            "%%B" -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
            if not errorlevel 1 set "NICKSCAN_PY=%%B"
        )
    )
)
if defined NICKSCAN_PY goto execute

for %%K in ("HKCU\Software\Python" "HKLM\Software\Python" "HKLM\Software\WOW6432Node\Python") do (
    for /f "tokens=2,*" %%A in ('reg query "%%~K" /s /ve 2^>nul') do (
        if /i "%%A"=="REG_SZ" if exist "%%B\python.exe" (
            "%%B\python.exe" -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
            if not errorlevel 1 set "NICKSCAN_PY=%%B\python.exe"
        )
    )
)
if defined NICKSCAN_PY goto execute

if not exist ".venv\Scripts\python.exe" goto python_missing
".venv\Scripts\python.exe" -I -c "import sys;sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>&1
if errorlevel 1 goto python_missing
set "NICKSCAN_PY=%CD%\.venv\Scripts\python.exe"
goto execute

:py312
set "NICKSCAN_PY=py"
set "NICKSCAN_ARGS=-3.12"
goto execute
:py311
set "NICKSCAN_PY=py"
set "NICKSCAN_ARGS=-3.11"
goto execute
:py3
set "NICKSCAN_PY=py"
set "NICKSCAN_ARGS=-3"
goto execute

:execute
"%NICKSCAN_PY%" %NICKSCAN_ARGS% -I "kurulum.py" "%NICKSCAN_MODE%" -- %*
set "NICKSCAN_EXIT=%ERRORLEVEL%"
popd
pause
endlocal & exit /b %NICKSCAN_EXIT%

:missing_files
echo.
echo Gerekli dosyalar eksik: nickscan.py ve kurulum.py ayni klasorde olmali.
echo ZIP'in tamamini bir klasore cikart. BAT dosyasini ZIP icinden calistirma.
popd
pause
exit /b 1

:python_missing
echo.
echo Calisan Python bulunamadi. Kurulum basarili gibi devam ettirilmedi.
echo 64-bit Python 3.11 veya 3.12 kurup bu dosyayi tekrar ac.
echo https://www.python.org/downloads/windows/
echo Mevcut Python surumlerini veya raporlarini silmene gerek yok.
popd
pause
exit /b 1

:folder_error
echo.
echo Program klasorune erisilemiyor. ZIP'i yerel bir klasore tamamen cikart.
pause
exit /b 1

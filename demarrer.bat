@echo off
setlocal EnableExtensions
REM Lanceur Windows du site : double-cliquez ce fichier.
REM Messages volontairement sans accents : la console Windows ne lit pas
REM l'UTF-8 par defaut, elle les abimerait.
REM %~dp0 est le dossier de ce script : on s'y place, sinon le serveur
REM servirait le repertoire depuis lequel la console a ete ouverte.
cd /d "%~dp0"

REM Un Python 3 qui fonctionne VRAIMENT : chaque candidat est essaye avant
REM d'etre retenu. Le lanceur "py" peut viser une version supprimee depuis
REM (erreur "Unable to create process using ...") ; "python" peut n'etre que
REM l'alias du Microsoft Store, qui ouvrirait la boutique au lieu de repondre.
set "PYEXE="
call :essayer py -3
if not defined PYEXE for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYEXE call :essayer_chemin "%%P"
if not defined PYEXE for /f "delims=" %%P in ('where python3 2^>nul') do if not defined PYEXE call :essayer_chemin "%%P"
if not defined PYEXE for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*" "%ProgramFiles%\Python3*" "C:\Python3*") do if not defined PYEXE if exist "%%~D\python.exe" call :essayer_chemin "%%~D\python.exe"

if not defined PYEXE (
  echo.
  echo   Aucun Python 3 utilisable n'a ete trouve.
  echo   Installez-le depuis https://www.python.org/downloads/ puis relancez.
  echo.
  pause
  exit /b 1
)

echo   Python retenu : %PYEXE%
call %PYEXE% demarrer.py %*

REM Sans ce garde-fou, une erreur au demarrage fermerait la fenetre aussitot
REM et l'utilisateur ne verrait jamais le message qui l'explique.
if errorlevel 1 (
  echo.
  echo   Le lanceur s'est arrete sur une erreur ^(voir ci-dessus^).
  echo.
  pause
)
exit /b

:essayer
REM "call" : si le candidat est lui-meme un fichier .bat, la main revient ici.
REM "<nul" : un lanceur qui poserait une question ne bloque pas la fenetre.
call %* -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)" <nul >nul 2>&1
if not errorlevel 1 set "PYEXE=%*"
exit /b

:essayer_chemin
set "CAND=%~1"
if /i not "%CAND:\WindowsApps\=%"=="%CAND%" exit /b
"%CAND%" -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)" <nul >nul 2>&1
if not errorlevel 1 set "PYEXE="%CAND%""
exit /b

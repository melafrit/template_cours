@echo off
REM Lanceur Windows du site du cours. Messages volontairement sans accents :
REM la console Windows ne lit pas l'UTF-8 par defaut, elle les abimerait — double-cliquez ce fichier.
REM %~dp0 est le dossier de ce script : on s'y place, sinon le serveur
REM servirait le repertoire depuis lequel la console a ete ouverte.
cd /d "%~dp0"

set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if not defined PYEXE (
  where python >nul 2>&1 && set "PYEXE=python"
)

if not defined PYEXE (
  echo.
  echo   Python 3 est introuvable.
  echo   Installez-le depuis https://www.python.org/downloads/ puis relancez.
  echo.
  pause
  exit /b 1
)

%PYEXE% demarrer.py %*

REM Sans ce garde-fou, une erreur au demarrage fermerait la fenetre aussitot
REM et l'utilisateur ne verrait jamais le message qui l'explique.
if errorlevel 1 (
  echo.
  echo   Le lanceur s'est arrete sur une erreur ^(voir ci-dessus^).
  echo.
  pause
)

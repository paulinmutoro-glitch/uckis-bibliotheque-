@echo off
REM Construit Bibliotheque_UCKIS.exe a partir des sources.
REM A executer sur un PC Windows avec Python 3.10+ installe (https://python.org).

echo === Installation des dependances ===
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

echo === Construction de l'executable ===
pyinstaller --onefile --windowed --name Bibliotheque_UCKIS ^
  --icon icon.ico ^
  --add-data "app.py;." ^
  --add-data "catalogue.csv;." ^
  --add-data "plan_acquisition.json;." ^
  --add-data "icon.png;." ^
  --collect-all streamlit ^
  --collect-all altair ^
  --hidden-import streamlit.web.cli ^
  launcher.py

echo.
echo Termine ! L'executable se trouve dans le dossier "dist".
echo Copiez tout le dossier "dist\Bibliotheque_UCKIS" (onedir) ou le fichier
echo "dist\Bibliotheque_UCKIS.exe" (onefile) la ou vous voulez l'utiliser.
pause

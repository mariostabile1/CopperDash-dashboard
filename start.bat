@echo off
REM Attiva modalità "fail fast"
setlocal enabledelayedexpansion
echo Running setup...
REM Controlla se la cartella venv NON esiste
if not exist venv (
    python -m venv venv
)

REM Attiva l'ambiente virtuale
call venv\Scripts\activate.bat

REM Installa le dipendenze
pip install -r requirements.txt

REM Esegui lo script Python
python src\app\app.py

REM Disattiva il virtual environment
deactivate

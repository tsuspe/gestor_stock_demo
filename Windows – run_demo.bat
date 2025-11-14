@echo off
REM Activar entorno virtual si existe
IF EXIST .venv\Scripts\activate.bat (
    CALL .venv\Scripts\activate.bat
)

streamlit run src/st_app.py
pause

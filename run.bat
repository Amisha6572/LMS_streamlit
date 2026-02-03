@echo off
REM Quick Start Script for Library Management System

echo.
echo ====================================
echo Library Management System - Quick Start
echo ====================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the app
echo.
echo ====================================
echo Starting Streamlit application...
echo Open your browser at: http://localhost:8501
echo ====================================
echo.

streamlit run app.py

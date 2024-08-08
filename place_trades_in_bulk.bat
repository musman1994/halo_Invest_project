@echo off

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run the curl command to trigger the import
curl -X POST http://127.0.0.1:8000/api/place_trades_in_bulk/

REM Deactivate the virtual environment
deactivate

REM Exit the script
exit
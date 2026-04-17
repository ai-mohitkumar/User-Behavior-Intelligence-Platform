@echo off
echo Starting Backend...
call venv\Scripts\activate.bat
cd UserBehaviorApp\backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload


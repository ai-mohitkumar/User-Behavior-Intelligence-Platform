@echo off
echo Starting Backend (no auth)...
call venv\Scripts\activate.bat
uvicorn UserBehaviorApp.backend.main:app --host 127.0.0.1 --port 8000 --reload


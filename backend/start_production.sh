#!/bin/bash
cd /home/surajpatel/Desktop/mainVideoGenerate/backend
source ../.venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

#!/bin/bash

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build

# Move built files to backend static directory
echo "Moving frontend build to backend..."
cd ..
mkdir -p backend/static
cp -r frontend/dist/* backend/static/

# Start backend server
echo "Starting server..."
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT

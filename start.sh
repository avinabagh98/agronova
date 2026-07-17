#!/bin/bash
set -e

echo "Starting FastAPI backend..."
cd /app/backend/api
# Start FastAPI in the background
# It needs to bind to 127.0.0.1 so it's accessible internally by Next.js
uvicorn main_api:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "Starting Next.js frontend..."
cd /app/frontend
# Railway provides the PORT environment variable.
# Next.js standalone server listens on PORT if it's set.
export PORT=${PORT:-3000}
export HOSTNAME="0.0.0.0"

# Start the standalone server
node server.js &
FRONTEND_PID=$!

# Wait for any process to exit
wait -n

# If one process exits, exit the container
exit $?

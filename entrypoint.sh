#!/bin/bash
# run in bash

# create startup script that does multiple things in a specific order:
# 1. start ollama server and wait up to 30 seconds HTTP request to 11434 is succesful
# 2. download the required models
# 3. run the original main.py which imports vector.py

# exit immediately if any command fails
set -e

echo "🚀 Starting Ollama server..."
# start the Ollama server in the background
ollama serve &
# store the PID of the Ollama server process (in case you want to stop it later)
OLLAMA_PID=$!

echo "⏳ Waiting for Ollama to start..."
# try up to 30 times (with 2s delay between tries) to check if Ollama is up
for i in {1..30}; do
    if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    fi
    # inform the user which attempt we're on
    echo "   Attempt $i/30..."
    sleep 2
    # if we reached the final attempt and it's still not up, exit with error
    if [ "$i" -eq 30 ]; then
        echo "❌ Ollama did not start in time."
        exit 1
    fi
done

# pull the required models into the Ollama server
echo "📥 Pulling required models..."
ollama pull llama3.2
ollama pull mxbai-embed-large

echo "✅ Models ready!"
echo "🔧 Starting your application..."

python app.py
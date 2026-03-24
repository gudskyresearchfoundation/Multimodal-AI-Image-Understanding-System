#!/bin/bash

# Install Ollama if not present
if ! command -v ollama &> /dev/null
then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama already installed"
fi

# Start server in background
ollama serve &
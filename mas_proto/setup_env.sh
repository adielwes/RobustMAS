#!/bin/bash
# Script to create the virtual environment and to intall the project dependencies

# Environment name
VENV_NAME="venv_proto"

echo ">>> Creating virtual environment: $VENV_NAME"
python3 -m venv $VENV_NAME

echo ">>> Activating virtual environment"
# Detects shell
if [ -n "$ZSH_VERSION" ]; then
    source $VENV_NAME/bin/activate
elif [ -n "$BASH_VERSION" ]; then
    source $VENV_NAME/bin/activate
else
    echo "Activate manually: source $VENV_NAME/bin/activate"
fi

echo ">>> Updating pip"
pip install --upgrade pip

echo ">>> Installing dependencies"
# Mesa versão estável + libs auxiliares
pip install mesa==1.1.0 pandas numpy

echo ">>> Environment is ready!"
echo "Activate with: source $VENV_NAME/bin/activate"


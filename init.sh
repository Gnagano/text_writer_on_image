#!/bin/bash

# Constant
BASEDIR=$(dirname "$(realpath "$0")")
VENVDIR="venv_text_writer_on_image"

# Venv 
if [ ! -d "${BASEDIR}/${VENVDIR}" ]; then
  python3 -m venv "${BASEDIR}/${VENVDIR}"
fi

# Activate
if [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == CYGWIN* ]]; then
  # Windows (Git Bash, Cygwin) specific code
  source "${BASEDIR}/${VENVDIR}/Scripts/activate"
else
  # Linux/Mac specific code
  source "${BASEDIR}/${VENVDIR}/bin/activate"
fi

pip install --upgrade pip
pip install -r requirements.txt
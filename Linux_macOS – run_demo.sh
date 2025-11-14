#!/usr/bin/env bash
# Activar venv si existe
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

streamlit run src/st_app.py

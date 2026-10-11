#!/usr/bin/env bash
set -e
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
if [ ! -f models/lstm_autoencoder.pt ]; then
  python -m dl.train_model
fi
streamlit run app.py

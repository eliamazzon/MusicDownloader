#!/bin/bash
pkg update
pkg install python
pkg install libjpeg-turbo
pkg install ffmpeg
python -m pip install -r requirements.txt
chmod +x main.py

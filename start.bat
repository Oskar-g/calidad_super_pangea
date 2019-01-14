@echo off
pip install -r requirements.txt --no-index --find-links file:///tmp/packages
python cspangea/app/__main__.py

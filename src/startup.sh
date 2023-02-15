#!/bin/bash
uwsgi --http-socket :8000 --plugin python --wsgi-file app.py --callable app
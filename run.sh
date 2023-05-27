#!/bin/bash

cd backend && \
python -m gunicorn -w 2 -b 127.0.0.1:5000 app:app --timeout 60 & \

cd frontend && \
yarn dev

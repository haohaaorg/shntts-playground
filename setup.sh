#!/bin/bash

# Install frontend dependencies
cd frontend
yarn install

# Return to the project folder
cd ..

# Install backend dependencies
cd backend
pip install -r requirements.txt


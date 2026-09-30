#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
pip install -r ../ml-development/requirements.txt

# Run database migrations
alembic upgrade head

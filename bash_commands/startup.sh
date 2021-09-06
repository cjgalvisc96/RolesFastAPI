#!/bin/bash

# Let the DB start
python app/scripts/pre_start_app.py

# Init alembic
# alembic init alembic

# Make migrations
# alembic revision --autogenerate -m "Initial migration"

# Run Migrate
alembic upgrade head

# Create initial data in DB
python app/scripts/create_initial_data_in_db.py

#Start app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
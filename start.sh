#!/bin/sh

# Run database migrations:
flask db upgrade

# Run the application:
exec flask run --host=0.0.0.0 --port=5000

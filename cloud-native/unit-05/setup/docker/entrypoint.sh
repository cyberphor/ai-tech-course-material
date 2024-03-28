#!/bin/bash

# check if the PRIVATE_KEY environment variable is set
if [ -z "$PRIVATE_KEY" ]; then
  echo "PRIVATE_KEY environment variable is not set"
  exit 1
fi

# check if the PUBLIC_KEY environment variable is set
if [ -z "$PUBLIC_KEY" ]; then
  echo "PUBLIC_KEY environment variable is not set"
  exit 1
fi

# run the Django app
poetry run python manage.py runserver 0.0.0.0:8080
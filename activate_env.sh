#!/bin/bash

source venv/bin/activate
export APP_SETTINGS="config.LocalConfig"
export DATABASE_URL="postgresql://localhost/decks"
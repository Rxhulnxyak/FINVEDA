#!/bin/sh

# Move to backend directory
if [ -d "/app/backend" ]; then
    cd /app/backend
fi

# Wait for database to be ready (Only in local docker-compose)
if [ -n "$DATABASE_URL" ]; then
  echo "Using DATABASE_URL for connection"
else
  echo "Waiting for local postgres..."
  while ! nc -z db 5432; do
    sleep 0.1
  done
  echo "PostgreSQL started"
fi

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate

# Run data ingestion in the background to avoid healthcheck timeouts
(
    if [ "$(python manage.py shell -c 'from companies.models import Company; print(Company.objects.count())')" = "0" ]; then
        echo "Empty database detected. Running initial data ingestion in background..."
        # Run ETL pipeline
        python ../etl/01_extract_from_mysql.py
        python ../etl/02_clean_and_transform.py
        # Then load into DB
        python manage.py load_financials
        python manage.py seed_missing_data
        python manage.py update_logos
        python manage.py generate_ml_scores
        python manage.py analyze_companies
        python manage.py generate_pros_cons
        echo "Background data ingestion complete."
    fi
) &

# Start server
echo "Starting server on port ${PORT:-8000}..."
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    # Use gunicorn and bind to ALL interfaces (0.0.0.0)
    gunicorn finveda_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120
else
    python manage.py runserver 0.0.0.0:8000
fi

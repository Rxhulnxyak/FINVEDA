#!/bin/sh

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate

# Load initial data and generate intelligence if DB is empty
# Note: In production, you might want to do this manually
echo "Checking for existing data..."
if [ "$(python manage.py shell -c 'from companies.models import Company; print(Company.objects.count())')" = "0" ]; then
    echo "Empty database detected. Running initial data ingestion..."
    python manage.py load_financials
    python manage.py seed_missing_data
    python manage.py update_logos
    python manage.py generate_ml_scores
    python manage.py analyze_companies
    python manage.py generate_pros_cons
fi

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:${PORT:-8000}

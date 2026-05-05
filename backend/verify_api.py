import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finveda_backend.settings')
django.setup()

from companies.models import Company
from companies.serializers import CompanySerializer

company = Company.objects.filter(symbol='TCS').first()
if company:
    serializer = CompanySerializer(company)
    print(json.dumps(serializer.data, indent=2))
else:
    print("No companies found.")

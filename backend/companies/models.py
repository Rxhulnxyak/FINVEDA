from django.db import models

class Sector(models.Model):
    sector_name = models.CharField(max_length=100, unique=True)
    sector_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.sector_name

class Company(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    company_name = models.CharField(max_length=255)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, related_name='companies')
    sub_sector = models.CharField(max_length=100, blank=True, null=True)
    company_logo = models.URLField(max_length=500, blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    nse_url = models.URLField(max_length=500, blank=True, null=True)
    bse_url = models.URLField(max_length=500, blank=True, null=True)
    face_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    book_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    about_company = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.symbol})"

class FiscalYear(models.Model):
    year_label = models.CharField(max_length=20, unique=True) # e.g. "Mar 2024"
    fiscal_year = models.IntegerField() # e.g. 2024
    quarter = models.CharField(max_length=5, blank=True, null=True) # Q1, Q2, etc.
    is_ttm = models.BooleanField(default=False)
    is_half_year = models.BooleanField(default=False)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.year_label

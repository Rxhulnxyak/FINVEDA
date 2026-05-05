from django.db import models
from companies.models import Company, FiscalYear

class Analysis(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='analysis')
    period_label = models.CharField(max_length=20) # 10Y, 5Y, 3Y, TTM
    compounded_sales_growth_pct = models.FloatField(null=True, blank=True)
    compounded_profit_growth_pct = models.FloatField(null=True, blank=True)
    stock_price_cagr_pct = models.FloatField(null=True, blank=True)
    roe_pct = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Analysis"

class HealthLabel(models.Model):
    label_name = models.CharField(max_length=20) # EXCELLENT, GOOD, etc.
    min_score = models.FloatField()
    max_score = models.FloatField()
    color_hex = models.CharField(max_length=7)

    def __str__(self):
        return self.label_name

class MLScores(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ml_scores')
    computed_at = models.DateTimeField(auto_now_add=True)
    overall_score = models.FloatField()
    profitability_score = models.FloatField()
    growth_score = models.FloatField()
    leverage_score = models.FloatField()
    cashflow_score = models.FloatField()
    dividend_score = models.FloatField()
    trend_score = models.FloatField()
    health_label = models.ForeignKey(HealthLabel, on_delete=models.SET_NULL, null=True)

class ProsCons(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='pros_cons')
    is_pro = models.BooleanField()
    category = models.CharField(max_length=50)
    text = models.TextField()
    source = models.CharField(max_length=20, default='MANUAL') # MANUAL/ML
    confidence = models.FloatField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from companies.models import Company, FiscalYear

class ProfitLoss(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='profit_loss')
    year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    sales = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    expenses = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    operating_profit = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    opm_pct = models.FloatField(null=True, blank=True)
    other_income = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    interest = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    depreciation = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    profit_before_tax = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    tax_pct = models.FloatField(null=True, blank=True)
    net_profit = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_payout_pct = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('company', 'year')

class BalanceSheet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='balance_sheets')
    year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    equity_capital = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    reserves = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    borrowings = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    other_liabilities = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_liabilities = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    fixed_assets = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    cwip = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    investments = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    other_assets = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_assets = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    debt_to_equity = models.FloatField(null=True, blank=True) # Computed during ETL

    class Meta:
        unique_together = ('company', 'year')

class CashFlow(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cash_flows')
    year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    operating_activity = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    investing_activity = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    financing_activity = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    net_cash_flow = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    free_cash_flow = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True) # Computed

    class Meta:
        unique_together = ('company', 'year')

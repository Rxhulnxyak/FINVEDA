import os
import sys
import django
import pandas as pd
import numpy as np

# Set up Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finveda_backend.settings')
django.setup()

from companies.models import Company
from financials.models import ProfitLoss, BalanceSheet
from analytics.models import MLScores, HealthLabel

def calculate_scores():
    companies = Company.objects.all()
    
    # Get labels
    labels = list(HealthLabel.objects.all().order_by('min_score'))
    if not labels:
        # Create default labels if missing
        HealthLabel.objects.get_or_create(label_name="POOR", min_score=0, max_score=30, color_hex="#EF4444")
        HealthLabel.objects.get_or_create(label_name="WEAK", min_score=30, max_score=50, color_hex="#F59E0B")
        HealthLabel.objects.get_or_create(label_name="AVERAGE", min_score=50, max_score=70, color_hex="#3B82F6")
        HealthLabel.objects.get_or_create(label_name="GOOD", min_score=70, max_score=85, color_hex="#10B981")
        HealthLabel.objects.get_or_create(label_name="EXCELLENT", min_score=85, max_score=100, color_hex="#059669")
        labels = list(HealthLabel.objects.all().order_by('min_score'))

    for company in companies:
        # Fetch latest financials
        latest_pl = ProfitLoss.objects.filter(company=company).order_by('-year__fiscal_year').first()
        latest_bs = BalanceSheet.objects.filter(company=company).order_by('-year__fiscal_year').first()
        
        if not latest_pl or not latest_bs:
            continue
            
        # 1. Profitability Score (ROE, OPM)
        # Placeholder logic: normalize these to 0-100
        roe = float(latest_pl.net_profit / latest_bs.equity_capital) * 100 if latest_bs.equity_capital else 0
        opm = latest_pl.opm_pct or 0
        prof_score = min(100, (roe * 2 + opm) / 3 * 2) # Arbitrary normalization
        
        # 2. Leverage Score (Debt/Equity)
        d_e = latest_bs.debt_to_equity or 0
        lev_score = max(0, 100 - (d_e * 50)) # Lower debt is better
        
        # 3. Growth Score (Sales Growth)
        # (Simplified: just use last year's sales vs avg if available, or just placeholder)
        growth_score = 75 # Placeholder
        
        # Overall
        overall = (prof_score * 0.4 + lev_score * 0.3 + growth_score * 0.3)
        
        # Find label
        lbl = None
        for l in labels:
            if l.min_score <= overall <= l.max_score:
                lbl = l
                break
        
        MLScores.objects.update_or_create(
            company=company,
            defaults={
                'overall_score': overall,
                'profitability_score': prof_score,
                'leverage_score': lev_score,
                'growth_score': growth_score,
                'cashflow_score': 70,
                'dividend_score': 60,
                'trend_score': 80,
                'health_label': lbl
            }
        )
    print(f"Computed health scores for {len(companies)} companies.")

if __name__ == "__main__":
    calculate_scores()

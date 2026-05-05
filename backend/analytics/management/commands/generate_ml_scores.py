import random
from datetime import datetime
from django.core.management.base import BaseCommand
from companies.models import Company
from financials.models import ProfitLoss, BalanceSheet, CashFlow
from analytics.models import MLScores, HealthLabel

class Command(BaseCommand):
    help = 'Generates placeholder ML scores and health labels for companies'

    def handle(self, *args, **options):
        self.stdout.write("Initializing Health Labels...")
        labels = [
            {'name': 'EXCELLENT', 'min': 80, 'max': 100, 'color': '#10B981'},
            {'name': 'GOOD', 'min': 60, 'max': 79.9, 'color': '#3B82F6'},
            {'name': 'AVERAGE', 'min': 40, 'max': 59.9, 'color': '#F59E0B'},
            {'name': 'POOR', 'min': 0, 'max': 39.9, 'color': '#EF4444'},
        ]

        label_objs = {}
        for l in labels:
            obj, _ = HealthLabel.objects.update_or_create(
                label_name=l['name'],
                defaults={
                    'min_score': l['min'],
                    'max_score': l['max'],
                    'color_hex': l['color']
                }
            )
            label_objs[l['name']] = obj

        self.stdout.write("Generating Scores for Companies...")
        companies = Company.objects.all()
        
        for company in companies:
            # Simple logic: higher profitability -> higher score
            pl = ProfitLoss.objects.filter(company=company).order_by('-year__fiscal_year').first()
            bs = BalanceSheet.objects.filter(company=company).order_by('-year__fiscal_year').first()
            
            # Placeholder weights
            profitability = random.uniform(50, 95) if pl and pl.net_profit > 0 else random.uniform(10, 50)
            growth = random.uniform(40, 90)
            leverage = 100 - (min(bs.debt_to_equity if bs else 1, 2) * 40) # Higher D/E -> lower leverage score
            leverage = max(0, min(100, leverage))
            
            overall = (profitability * 0.4) + (growth * 0.3) + (leverage * 0.3)
            
            # Find health label
            assigned_label = label_objs['AVERAGE']
            for name, obj in label_objs.items():
                if obj.min_score <= overall <= obj.max_score:
                    assigned_label = obj
                    break

            MLScores.objects.create(
                company=company,
                overall_score=round(overall, 2),
                profitability_score=round(profitability, 2),
                growth_score=round(growth, 2),
                leverage_score=round(leverage, 2),
                cashflow_score=random.uniform(30, 85),
                dividend_score=random.uniform(20, 90),
                trend_score=random.uniform(40, 95),
                health_label=assigned_label
            )
            self.stdout.write(f"Generated score {overall:.2f} for {company.symbol} ({assigned_label.label_name})")

        self.stdout.write(self.style.SUCCESS('Successfully generated ML scores!'))

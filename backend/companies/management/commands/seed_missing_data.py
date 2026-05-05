import random
from django.core.management.base import BaseCommand
from companies.models import Company, FiscalYear
from financials.models import ProfitLoss, BalanceSheet, CashFlow

class Command(BaseCommand):
    help = 'Seeds realistic sample data for companies missing financial records'

    def handle(self, *args, **options):
        companies = Company.objects.all()
        years = ['Mar 2022', 'Mar 2023', 'Mar 2024']
        
        # Ensure fiscal years exist
        fy_objs = []
        for y in years:
            obj, _ = FiscalYear.objects.get_or_create(
                year_label=y,
                defaults={'fiscal_year': int(y.split()[-1]), 'sort_order': int(y.split()[-1])}
            )
            fy_objs.append(obj)

        seeded_count = 0
        for company in companies:
            if ProfitLoss.objects.filter(company=company).exists():
                continue
            
            # Generate base metrics
            base_sales = random.randint(5000, 50000)
            base_margin = random.uniform(0.1, 0.3)
            growth_rate = random.uniform(0.05, 0.15)
            
            for i, fy in enumerate(fy_objs):
                mult = (1 + growth_rate) ** i
                sales = int(base_sales * mult)
                op = int(sales * base_margin)
                other_inc = int(op * 0.1)
                interest = int(op * 0.05)
                dep = int(op * 0.08)
                pbt = op + other_inc - interest - dep
                tax = int(pbt * 0.25)
                net_profit = pbt - tax
                
                ProfitLoss.objects.get_or_create(
                    company=company,
                    year=fy,
                    defaults={
                        'sales': sales,
                        'expenses': sales - op,
                        'operating_profit': op,
                        'opm_pct': round(base_margin * 100, 2),
                        'other_income': other_inc,
                        'interest': interest,
                        'depreciation': dep,
                        'profit_before_tax': pbt,
                        'tax_pct': 25.0,
                        'net_profit': net_profit,
                        'eps': round(net_profit / 100, 2),
                        'dividend_payout_pct': 30.0
                    }
                )

            # Seed 1 Balance Sheet record
            BalanceSheet.objects.get_or_create(
                company=company,
                year=fy_objs[-1],
                defaults={
                    'equity_capital': 1000,
                    'reserves': 10000,
                    'borrowings': 2000,
                    'other_liabilities': 3000,
                    'total_liabilities': 16000,
                    'fixed_assets': 8000,
                    'cwip': 500,
                    'investments': 4000,
                    'other_assets': 3500,
                    'total_assets': 16000,
                    'debt_to_equity': 0.18
                }
            )

            # Seed 1 Cash Flow record
            CashFlow.objects.get_or_create(
                company=company,
                year=fy_objs[-1],
                defaults={
                    'operating_activity': int(net_profit * 1.2),
                    'investing_activity': -int(net_profit * 0.5),
                    'financing_activity': -int(net_profit * 0.3),
                    'net_cash_flow': int(net_profit * 0.4),
                    'free_cash_flow': int(net_profit * 0.7)
                }
            )
            
            seeded_count += 1
            if seeded_count % 10 == 0:
                self.stdout.write(f"Seeded {seeded_count} companies...")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {seeded_count} companies with demonstration data!"))

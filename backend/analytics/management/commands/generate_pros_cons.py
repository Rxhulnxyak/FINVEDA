from django.core.management.base import BaseCommand
from companies.models import Company
from financials.models import ProfitLoss, BalanceSheet, CashFlow
from analytics.models import MLScores, Analysis, ProsCons

class Command(BaseCommand):
    help = 'Generates Pros & Cons based on financial performance'

    def handle(self, *args, **options):
        companies = Company.objects.all()
        
        for company in companies:
            self.stdout.write(f"Generating Pros/Cons for {company.symbol}...")
            
            # Clear existing ML-generated pros/cons
            ProsCons.objects.filter(company=company, source='ML').delete()
            
            analysis = Analysis.objects.filter(company=company).first()
            pl = ProfitLoss.objects.filter(company=company).order_by('-year__fiscal_year').first()
            bs = BalanceSheet.objects.filter(company=company).order_by('-year__fiscal_year').first()
            cf = CashFlow.objects.filter(company=company).order_by('-year__fiscal_year').first()
            
            if not analysis: continue

            # --- PROS ---
            # 1. Good Profit Growth
            if analysis.compounded_profit_growth_pct > 15:
                ProsCons.objects.create(
                    company=company, is_pro=True, category='Growth', source='ML',
                    text=f"Company has delivered good profit growth of {analysis.compounded_profit_growth_pct}% CAGR over last few years."
                )
            
            # 2. Healthy ROE
            if analysis.roe_pct > 20:
                ProsCons.objects.create(
                    company=company, is_pro=True, category='Returns', source='ML',
                    text=f"Company has a healthy return on equity (ROE) of {analysis.roe_pct}%."
                )
            
            # 3. Low Debt
            if bs and bs.debt_to_equity < 0.5:
                ProsCons.objects.create(
                    company=company, is_pro=True, category='Solvency', source='ML',
                    text="Company is almost debt free or has a very healthy Debt-to-Equity ratio."
                )

            # 4. Positive Cash Flow
            if cf and cf.net_cash_flow > 0:
                ProsCons.objects.create(
                    company=company, is_pro=True, category='Cash Flow', source='ML',
                    text="Company has generated positive cash flow from operations."
                )

            # --- CONS ---
            # 1. High Valuation (Book Value comparison)
            # Placeholder: if book value is very low compared to some arbitrary "price"
            
            # 2. Low Sales Growth
            if analysis.compounded_sales_growth_pct < 5:
                ProsCons.objects.create(
                    company=company, is_pro=False, category='Growth', source='ML',
                    text=f"Company has delivered poor sales growth of {analysis.compounded_sales_growth_pct}% over last few years."
                )

            # 3. High Debt (if not already handled)
            if bs and bs.debt_to_equity > 1.5:
                ProsCons.objects.create(
                    company=company, is_pro=False, category='Solvency', source='ML',
                    text=f"Company has a high Debt-to-Equity ratio of {bs.debt_to_equity:.2f}."
                )

            # 4. Low Interest Coverage (if interest is high)
            if pl and float(pl.interest or 0) > float(pl.net_profit or 0) * 0.5:
                ProsCons.objects.create(
                    company=company, is_pro=False, category='Financials', source='ML',
                    text="Interest cost is significant compared to net profits."
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated Pros & Cons!'))

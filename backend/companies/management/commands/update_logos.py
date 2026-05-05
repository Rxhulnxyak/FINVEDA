from django.core.management.base import BaseCommand
from companies.models import Company

class Command(BaseCommand):
    help = 'Updates company logos using Clearbit and UI-Avatars for a premium look'

    def handle(self, *args, **options):
        # Common domain mapping for Nifty 100
        domain_map = {
            'TCS': 'tcs.com',
            'HDFCBANK': 'hdfcbank.com',
            'RELIANCE': 'ril.com',
            'INFY': 'infosys.com',
            'ICICIBANK': 'icicibank.com',
            'AXISBANK': 'axisbank.com',
            'SBIN': 'sbi.co.in',
            'KOTAKBANK': 'kotak.com',
            'LT': 'larsentoubro.com',
            'BHARTIARTL': 'airtel.in',
            'ITC': 'itcportal.com',
            'HINDUNILVR': 'hul.co.in',
            'ASIANPAINT': 'asianpaints.com',
            'MARUTI': 'marutisuzuki.com',
            'SUNPHARMA': 'sunpharma.com',
            'TITAN': 'titancompany.in',
            'ULTRACEMCO': 'ultratechcement.com',
            'WIPRO': 'wipro.com',
            'BAJFINANCE': 'bajajfinserv.in',
            'JSWSTEEL': 'jsw.in',
            'ADANIENT': 'adanienterprises.com',
            'ADANIPORTS': 'adaniports.com',
            'ADANIPOWER': 'adanipower.com',
            'AMBUJACEM': 'ambujacement.com',
            'APOLLOHOSP': 'apollohospitals.com',
            'BAJAJ-AUTO': 'bajajauto.com',
            'BANKBARODA': 'bankofbaroda.in',
            'BEL': 'bel-india.in',
            'BPCL': 'bpcl.in',
            'BRITANNIA': 'britannia.co.in',
            'CIPLA': 'cipla.com',
            'COALINDIA': 'coalindia.in',
            'DABUR': 'dabur.com',
            'DRREDDY': 'drreddys.com',
            'EICHERMOT': 'eichermotors.com',
            'GAIL': 'gailonline.com',
            'GRASIM': 'grasim.com',
            'HAL': 'hal-india.co.in',
            'HCLTECH': 'hcltech.com',
            'HDFCLIFE': 'hdfclife.com',
            'HEROMOTOCO': 'heromotocorp.com',
            'HINDALCO': 'hindalco.com',
            'INDUSINDBK': 'indusind.com',
            'IOC': 'iocl.com',
            'M&M': 'mahindra.com',
            'NESTLEIND': 'nestle.in',
            'NTPC': 'ntpc.co.in',
            'ONGC': 'ongcindia.com',
            'POWERGRID': 'powergrid.in',
            'TATACONSUM': 'tataconsumer.com',
            'TATAMOTORS': 'tatamotors.com',
            'TATASTEEL': 'tatasteel.com',
            'TECHM': 'techmahindra.com',
            'TRENT': 'trentlimited.com',
            'TVSMOTOR': 'tvsmotor.com',
            'JIOFIN': 'jiofinancialservices.com',
            'JSWENERGY': 'jsw.in',
            'LICI': 'licindia.in',
            'LODHA': 'lodhagroup.in',
            'NHPC': 'nhpcindia.com',
            'PNB': 'pnbindia.in',
            'RECLTD': 'recindia.nic.in',
            'SHRIRAMFIN': 'shriramfinance.in',
            'SIEMENS': 'siemens.com',
        }

        companies = Company.objects.all()
        updated_count = 0
        
        for company in companies:
            domain = domain_map.get(company.symbol)
            if domain:
                logo_url = f"https://www.google.com/s2/favicons?sz=128&domain={domain}"
            else:
                # Use a high-quality initials logo if domain is unknown
                bg_color = "0D9488" # Teal
                logo_url = f"https://ui-avatars.com/api/?name={company.symbol}&background={bg_color}&color=fff&size=128&font-size=0.4"
            
            company.company_logo = logo_url
            company.save()
            updated_count += 1
            
        self.stdout.write(self.style.SUCCESS(f"Successfully updated logos for {updated_count} companies!"))

import subprocess
import os
import sys
from django.conf import settings
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Max, Count
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Sector, FiscalYear
from .serializers import CompanySerializer, SectorSerializer
from analytics.models import MLScores

class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        sector = self.get_object()
        companies = sector.companies.all()
        
        # Get latest ML scores for each company (SQLite compatible)
        peer_data = []
        total_score = 0
        max_score = 0
        count = 0

        for company in companies:
            latest_score = MLScores.objects.filter(company=company).order_by('-computed_at').first()
            score_val = latest_score.overall_score if latest_score else 0
            
            peer_data.append({
                'symbol': company.symbol,
                'name': company.company_name,
                'score': round(score_val, 2)
            })
            
            if score_val > 0:
                total_score += score_val
                count += 1
                if score_val > max_score:
                    max_score = score_val
        
        avg_score = total_score / count if count > 0 else 0
        
        return Response({
            'sector_name': sector.sector_name,
            'company_count': companies.count(),
            'avg_overall_score': round(avg_score, 2),
            'max_overall_score': round(max_score, 2),
            'companies': peer_data
        })

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sector', 'sub_sector']
    search_fields = ['symbol', 'company_name']
    ordering_fields = ['company_name', 'symbol']

@method_decorator(csrf_exempt, name='dispatch')
class IngestViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def health(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def trigger(self, request):
        try:
            # Run the ETL scripts using the current environment
            # Note: In a real production app, use Celery/Redis
            base_dir = settings.BASE_DIR.parent
            
            # Step 1: Extraction
            subprocess.run([sys.executable, os.path.join(base_dir, "etl/01_extract_from_mysql.py")], check=True)
            # Step 2: Transformation
            subprocess.run([sys.executable, os.path.join(base_dir, "etl/02_clean_and_transform.py")], check=True)
            # Step 3: Loading
            from django.core.management import call_command
            call_command('load_financials')
            call_command('seed_missing_data')
            call_command('update_logos')
            call_command('generate_ml_scores')
            call_command('analyze_companies')
            call_command('generate_pros_cons')
            
            return Response({"status": "success", "message": "Data pipeline executed successfully."})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework import serializers
from .models import Company, Sector, FiscalYear
from financials.models import ProfitLoss, BalanceSheet, CashFlow
from analytics.models import MLScores, HealthLabel, Analysis, ProsCons

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class HealthLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthLabel
        fields = '__all__'

class MLScoresSerializer(serializers.ModelSerializer):
    health_label = HealthLabelSerializer(read_only=True)
    class Meta:
        model = MLScores
        fields = '__all__'

class ProfitLossSerializer(serializers.ModelSerializer):
    year_label = serializers.CharField(source='year.year_label', read_only=True)
    class Meta:
        model = ProfitLoss
        fields = '__all__'

class BalanceSheetSerializer(serializers.ModelSerializer):
    year_label = serializers.CharField(source='year.year_label', read_only=True)
    class Meta:
        model = BalanceSheet
        fields = '__all__'

class CashFlowSerializer(serializers.ModelSerializer):
    year_label = serializers.CharField(source='year.year_label', read_only=True)
    class Meta:
        model = CashFlow
        fields = '__all__'

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'

class ProsConsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProsCons
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    sector = SectorSerializer(read_only=True)
    latest_score = serializers.SerializerMethodField()
    profit_loss = ProfitLossSerializer(many=True, read_only=True)
    balance_sheets = BalanceSheetSerializer(many=True, read_only=True)
    cash_flows = CashFlowSerializer(many=True, read_only=True)
    analysis = AnalysisSerializer(many=True, read_only=True)
    pros_cons = ProsConsSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            'symbol', 'company_name', 'sector', 'sub_sector', 
            'company_logo', 'website', 'nse_url', 'bse_url', 
            'face_value', 'book_value', 'about_company',
            'latest_score', 'profit_loss', 'balance_sheets', 'cash_flows',
            'analysis', 'pros_cons'
        ]

    def get_latest_score(self, obj):
        score = MLScores.objects.filter(company=obj).order_by('-computed_at').first()
        if score:
            return MLScoresSerializer(score).data
        return None

from rest_framework import serializers
from .models import *

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherDetail
        fields = ('__all__')
        # fields = ['date','max','min','percipitation','station']

class WeatherImportSerializer(serializers.Serializer):
    file = serializers.FileField()

class WeatherStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStatistics
        fields = ('__all__')
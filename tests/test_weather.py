from django.test import TestCase
from api.views import *
from api.models import WeatherDetail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

class WeatherDetailTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.weather_object = WeatherDetail.objects.all()
        self.wurl = reverse(weatherApiList)
        WeatherDetail.objects.create(date='2023-02-10', max=55, min=32, percipitation=0, station='STATION002')
    
    def test_weather_create(self):
        data = {'date':'2023-02-09', 'max':35, 'min':12, 'percipitation':0, 'station':'STATION001'}
        response = self.client.post(self.wurl, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_weather_station(self):
        data = {'station':'STATION002'}
        response = self.client.get(self.wurl,data,format='json')
        self.assertEqual(WeatherDetail.objects.count(),1)
        self.assertEqual(WeatherDetail.objects.get().station =='STATION002',True)
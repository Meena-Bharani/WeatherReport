from django.urls import path, re_path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # re_path(r'^weather$',views.weatherApiList),
    # re_path(r'^weather/?P<id>[0-9]+)$',views.weatherApiDetail),
    path('weather',views.weatherApiList),
    path('weather/<int:id>',views.weatherApiDetail),
    path('importdata/',views.ImportWeatherView.as_view(), name='import-file'),
    path('weather/stats/',views.WeatherStatisticsApiView),
]

urlpatterns = format_suffix_patterns(urlpatterns)
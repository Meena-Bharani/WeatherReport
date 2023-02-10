from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import WeatherDetail, WeatherStatistics
from .serializers import WeatherSerializer, WeatherImportSerializer, WeatherStatisticsSerializer

import os, sys,csv, pandas as pd
import datetime
from django.core.files import File

import logging
from django.db import connection

# Create your views here.

filename= os.path.join(os.getcwd(),'logdetails.txt')
logging.basicConfig(filename=filename)
logging.info("Debug logging test...")

logger = logging.getLogger(__name__)

@api_view(['GET','POST'])
def weatherApiList(request):  
    try:   
        if request.method == 'GET':
            weather_all = WeatherDetail.objects.all().order_by('id')
            dt = request.query_params.get('date')
            if dt is not None:
                weather_all = weather_all.filter(date=dt).order_by('id')
            st = request.query_params.get('station')
            if st is not None:
                weather_all = weather_all.filter(station=str.upper(st)).order_by('id')
            paginator = PageNumberPagination()
            context = paginator.paginate_queryset(weather_all, request)
            serializer = WeatherSerializer(context, many=True)
            return paginator.get_paginated_response(serializer.data)
        elif request.method == 'POST':
            serializer = WeatherSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message':'Something went wrong.'+ e},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def weatherApiDetail(request, id):
    try:
        result = WeatherDetail.objects.get(id=id)
        # if type(int(id)).__name__ == 'int':
        #     result = WeatherDetail.objects.get(id=id)
        # else:
        #     return Response({'message':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    except WeatherDetail.DoesNotExist:
        return Response({'message':'Weather is not exists'},status=status.HTTP_404_NOT_FOUND)
    
    try:
        if request.method == 'GET':            
            serializer = WeatherSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':            
            serializer = WeatherSerializer(result, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            result.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'message':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class ImportWeatherView(generics.CreateAPIView):
    serializer_class = WeatherImportSerializer
    
    # import data from the txt file
    def post(self,request):
        try:
            print('Started at: '+ str(datetime.datetime.now()))
            logging.error('Started at: '+ str(datetime.datetime.now()))
            no_of_records_inserted = 0
            directory = os.path.join(os.getcwd(),'data')
            files = os.listdir(directory)
            for f in files:
                file = os.path.join(directory,f)
                station=str.upper(f.split('.')[0])
                logging.error(station)
                dataset = pd.read_csv(file)
                dataset = pd.read_csv(file)
                weather_list =[]
                for i, row in dataset.iterrows():
                    r = row[0].split('\t')                    
                    if len(r) ==4:
                        date = pd.to_datetime(r[0], format='%Y%m%d')
                        max = int(r[1])
                        min = int(r[2])
                        percipitation = int(r[3])
                        try:
                            new_record = WeatherDetail(date=date,max=max,min=min,percipitation=percipitation,station=station)
                            new_record.save()
                            no_of_records_inserted = no_of_records_inserted + 1
                        except Exception as e:
                            print('station: '+station)
                            print(r)
                            logging.error(station+' - '+str(r[0])+' ** '+str(e))
                            continue
                            return Response({'message':'Integrity error'+str(e)},status=status.HTTP_400_BAD_REQUEST)
                        #d = [date,max,min,percipitation]
                        #weather_list.append(d)
                    else:
                        print('station: '+station)
                        print(r)
                # df = pd.DataFrame(weather_list,columns=['date','max','min','percipitation'])
            print('Ended at: '+ str(datetime.datetime.now()))
            print('Number of records inserted: '+ str(no_of_records_inserted))
            logging.error('Ended at: '+ str(datetime.datetime.now()))
            logging.error('Number of records inserted: '+ str(no_of_records_inserted))
            return Response({'message':'success'}, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':'Something went wrong.'+str(e)},status=status.HTTP_400_BAD_REQUEST)

# data Analysis part
@api_view(['GET','POST'])
def WeatherStatisticsApiView(request):
    try:
        if request.method == 'GET':
            statistics = WeatherStatistics.objects.all()
            paginator = PageNumberPagination()
            context = paginator.paginate_queryset(statistics, request)
            serializer = WeatherStatisticsSerializer(context, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            WeatherStatisticsInsertApiView(request)
            statistics = WeatherStatistics.objects.all()
            paginator = PageNumberPagination()
            context = paginator.paginate_queryset(statistics, request)
            serializer = WeatherStatisticsSerializer(context, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message':'Inserted Statistical weather data.'}, status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'message':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

# automatically find the average and insert values. must execute only once 
def WeatherStatisticsInsertApiView(request):
    try:
        query = ''' 
            INSERT INTO api_weatherstatistics (year, avg_max, avg_min,total_percipitation)
            select year, avg_max, avg_min,total_percipitation from (
            SELECT  extract(year from date) as year
                        , round(avg(max),0) as avg_max
                        , round(avg(min),0) as avg_min
                        ,sum(case when percipitation=-9999 then 0 else percipitation end) as total_percipitation
                    FROM api_weatherdetail
                    where max != -9999 or min != -9999
                    group by extract(year from date)
            ) A order by year
            ;
        '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            print(row)
        return row
    except Exception as e:
        return Response({'message':'No duplicates allowed.'+str(e)},status=status.HTTP_400_BAD_REQUEST)

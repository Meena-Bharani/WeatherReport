from django.db import models

# Create your models here.
class WeatherDetail(models.Model):
    date = models.DateField(blank=True)
    max = models.IntegerField(default=0, blank=True)
    min = models.IntegerField(default=0, blank=True)
    percipitation = models.IntegerField(default=0, blank=True)
    station = models.CharField(max_length=100, null=True, blank=True)
    createdDateTime = models.DateTimeField(auto_created=True, auto_now_add=True,blank=True)

    def __str__(self):
        return str(self.date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date','station'], name='station_date_unique'),
        ]


class WeatherStatistics(models.Model):
    year = models.IntegerField(unique=True)
    avg_max = models.IntegerField()
    avg_min = models.IntegerField()
    total_percipitation = models.IntegerField()

    def __str__(self):
        return str(self.year) + ' ' + str(self.avg_max)

    # class Meta:
    #     managed = False
    #     db_table='WeatherStatisticsView'
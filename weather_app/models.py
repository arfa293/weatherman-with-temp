from django.db import models

class WeatherRecord(models.Model):
    date= models.DateField(null=True, blank=True)
    max_Temperature = models.FloatField(null=True,blank=True)
    min_Temperature=models.FloatField(null=True,blank=True)
    humidity=models.IntegerField(null=True,blank=True)
    max_Humidity=models.IntegerField(null=True,blank=True)
    min_humidity = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
       return f"Weather on {self.date}: {self.max_Temperature}°C / {self.min_Temperature}°C"

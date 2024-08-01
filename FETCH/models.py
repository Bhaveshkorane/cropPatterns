from django.db import models

# # Create your models here.

class State(models.Model):
    statecode = models.IntegerField(primary_key=True,default=0)
    englishname = models.CharField(max_length=300,null=True,blank=True)
    localname = models.CharField(max_length=300,null=True,blank=True)
    statecreated = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    stateupdated = models.DateTimeField(auto_now=True,null=True,blank=True)
    
class District(models.Model):
    districtcode = models.IntegerField(primary_key=True,default=1)
    englishname = models.CharField(max_length=200,blank=True,null=True)
    localname = models.CharField(max_length=200,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,default=0,null=True,blank=True)
    districtcreated = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    districtupdated = models.DateTimeField(auto_now=True,null=True,blank=True)


class Subdistrict(models.Model):
    subdistrictcode = models.IntegerField(primary_key=True,default=2)
    englishname = models.CharField(max_length=200,null=True,blank=True)
    localname = models.CharField(max_length=200,null=True,blank=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE,default=1121,blank=True,null=True)           #how to create the foreign key for the data
    subdistrictcreated = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    subdistrictupdated = models.DateTimeField(auto_now=True,blank=True,null=True)
    state = models.IntegerField(null=True,blank=True,default=0)                                                  #added data though the querry

from django.db import models

class Village(models.Model):
    villagecode = models.IntegerField(primary_key=True, default=3)
    englishname = models.CharField(max_length=200, null=True, blank=True)
    localname = models.CharField(max_length=200, null=True, blank=True)
    subdistrict = models.ForeignKey('Subdistrict', on_delete=models.CASCADE, default=12342, blank=True, null=True)                 
    villagecreated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    villageupdated = models.DateTimeField(auto_now=True, blank=True, null=True)
    state = models.ForeignKey('State', null=True, blank=True, default=None, on_delete=models.CASCADE)
    district = models.ForeignKey('District', null=True, blank=True, default=None, on_delete=models.CASCADE)



class Crop(models.Model):
    cropname = models.CharField(max_length=200) 
    # season = models.CharField(max_length=100, null=True, blank=True)  
    # area = models.IntegerField(null=True, blank=True)
    # marketprice = models.IntegerField(null=True, blank=True)
    # fertilizer = models.IntegerField(null=True, blank=True)
    # village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True)  
    # subdistrict = models.ForeignKey(Subdistrict, on_delete=models.CASCADE, null=True, blank=True)  
    # district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)  
    # state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True) 
    




class Cropdatajson(models.Model):
    cropdata = models.JSONField(null=True,blank=True,default=None)


class AgriculturalData(models.Model):
    unique_id = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    area = models.FloatField()
    crop_type = models.CharField(max_length=100)
    area_cultivated = models.FloatField()
    yield_per_hectare = models.FloatField()
    soil_type = models.CharField(max_length=100)
    irrigation_method = models.CharField(max_length=100)
    temperature_average = models.FloatField()
    temperature_max = models.FloatField()
    temperature_min = models.FloatField()
    rainfall_total_mm = models.FloatField()
    rainfall_rainy_days = models.IntegerField()
    humidity_average_percentage = models.FloatField()
    fertilizer_type = models.CharField(max_length=100)
    fertilizer_quantity_kg = models.FloatField()
    pesticide_type = models.CharField(max_length=100)
    pesticide_quantity_l = models.FloatField()
    maxfile  =  models.IntegerField(blank=True,null=True)


class Cropdata(models.Model):
    unique_id = models.CharField(max_length=100,primary_key=True)
    area_cultivated = models.IntegerField(null=True,blank=True)
    crop_type = models.CharField(max_length=100,null=True,blank=True)
    yeild_perhectare = models.IntegerField(null=True,blank=True)
    soil_type = models.CharField(max_length=50,null=True,blank=True)
    irrigation_method = models.CharField(max_length=100,null=True,blank=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE,null=True,blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True,blank=True,default=27)
    district = models.ForeignKey(District,on_delete=models.CASCADE,null=True,blank=True,default=480)
    subdistrict = models.ForeignKey(Subdistrict,on_delete=models.CASCADE,null=True,blank=True,default=3648)

class Weather(models.Model):
    temp_min = models.IntegerField(null=True,blank=True)
    temp_max = models.IntegerField(null=True,blank=True)
    temp_avg = models.IntegerField(null=True,blank=True)
    rainfall_total = models.IntegerField(null=True,blank=True)
    rainfall_rainy_days = models.IntegerField(null=True,blank=True)
    humidity = models.IntegerField(null=True,blank=True)
    crop = models.ForeignKey(Cropdata, on_delete=models.CASCADE,default=None, to_field='unique_id')


class Pesticide(models.Model):
    pesticide_type = models.CharField(max_length=100,null=True,blank=True)
    quantity_l = models.IntegerField(null=True,blank=True)
    crop = models.ForeignKey(Cropdata, on_delete=models.CASCADE, null=True, blank=True)

class fertilizer(models.Model):
    fertilizer_type = models.CharField(max_length=100,null=True,blank=True)
    quantity_kg = models.IntegerField()
    crop = models.ForeignKey(Cropdata, on_delete=models.CASCADE, null=True, blank=True)



    




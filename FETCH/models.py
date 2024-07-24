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

class Village(models.Model):
    villagecode=models.IntegerField(primary_key=tuple,default=3)
    englishname=models.CharField(max_length=200,null=True,blank=True)
    localname=models.CharField(max_length=200,null=True,blank=True)
    subdistrict=models.ForeignKey(Subdistrict,on_delete=models.CASCADE,default=12342,blank=True,null=True)                  #here we need to store the subdistrict key as foreign key 
    vilagecreated = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    villageupdated = models.DateTimeField(auto_now=True,blank=True,null=True)


    



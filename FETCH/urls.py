from django.urls import path

# Imports for creting/inserting the data into database 
from .views import createstate
from .views import createdistrict
from .views import createsubdistrict
from .views import createvillage

# Imports for API's
from .views import VillageGeneric
from .views import StateGeneric
from .views import DistrictGeneric
# from .views import GeneratedData
from .views import generatedata
from .views import state
from .views import district
from .views import subdistrict
from .views import village
from .views import crops
from .views import savejson

from django.urls import path
from . import views
from .views import GenerateDataView  


urlpatterns = [

    # For inserting data into database 

    path('createstate/',createstate,name='createstate_url'),
    path('createdistrict/',createdistrict,name='createdistrict_url'),
    path('createsubdistrict/',createsubdistrict,name='createsubdistrict_url'),
    path('createvillage/',createvillage,name='createvillage_url'),
    # path('dependantfield/', views.dependantfield, name='dependantfield'),

    
    # For fetching data from the database through api 

    path('generic-village/',VillageGeneric.as_view()),
    path('generic-state/',StateGeneric.as_view()),
    path('generic-distirct/',DistrictGeneric.as_view()),
    path('generate-data/', GenerateDataView.as_view(), name='generate_data_view'),
    path('gene/',generatedata.as_view()),


    path('state/',state,name='state_url'),
    path('district/',district,name='district_url'),
    path('subdistrict/',subdistrict,name='subdistrict_url'),
    path('village/',village,name='village_url'),
    path('crop/',crops,name='crop_url'),
    path('savejson/',savejson,name='showjson_url'),




     
]


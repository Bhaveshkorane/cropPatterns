from django.urls import path

# Imports for creting/inserting the data into database 
from .views import createstate
from .views import createdistrict
from .views import createsubdistrict
from .views import createvillage

# Imports for showing the content 
from .views import showdistrict
from .views import showvillage
from .views import showsubdistrict
from .views import showstate

# Imports for API's
from .views import VillageGeneric
from .views import StateGeneric
from .views import DistrictGeneric


urlpatterns = [
    path('createstate/',createstate,name='createstate_url'),
    path('createdistrict/',createdistrict,name='createdistrict_url'),
    path('createsubdistrict/',createsubdistrict,name='createsubdistrict_url'),
    path('createvillage/',createvillage,name='createvillage_url'),
    path('showstate/',showstate,name='showstate_url'),
    path('showdistrict/',showdistrict,name='showdistrict_url'),
    path('showsubdistrict/',showdistrict,name='showsubdistrict_url'),
    path('showvillage/',showvillage,name='showvillage_url'),
    path('generic-village/',VillageGeneric.as_view()),
    path('generic-state/',StateGeneric.as_view()),
    path('generic-distirct/',DistrictGeneric.as_view()),

     
]


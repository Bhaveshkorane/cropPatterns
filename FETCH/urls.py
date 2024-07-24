from django.urls import path
from .views import createstate
from .views import createdistrict
urlpatterns = [
    path('createstate/',createstate,name='createstate_url'),
    path('createdistrict/',createdistrict,name='createdistrict_url'),
    
    
]


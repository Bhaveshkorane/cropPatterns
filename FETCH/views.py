from django.shortcuts import render
from django.shortcuts import HttpResponse
import requests
from rest_framework.response import Response 

# Importing models 
from .models import State
from .models import Subdistrict
from .models import Village
from .models import District


# Importing serializers 
from .serializers import VillageSerializer
from .serializers import StateSerializer
from .serializers import DistrictSerializer

# from rest_framework import response
# Create your views here.

#for .env file
from decouple import config

def createstate(request):
    count=0
    stateData = requests.post(config('state_api')).json()
    for i in stateData:
        #print(i)     # For checking 
        state_code=i['stateCode']
        english_name=i['stateNameEnglish']
        local_name=i['stateNameLocal']
        data=State(
                    statecode=state_code,
                    englishname=english_name,
                    localname=local_name
                    )
        data.save()
        count += 1

    print(f"data is saved successfully and added {count} states ")
    return HttpResponse(f"hello bhavesh you have added {count} states into the database")

# Inserting data into district table
def createdistrict(request):
    dcount = 0
    state_data=State.objects.all()
    for i in state_data:
        id_=i.statecode

        #print(id_)      #for checking 

        # Fetching the data from API
        # query='https://lgdirectory.gov.in/webservices/lgdws/districtList?stateCode='+str(id_)
        # query=f'https://lgdirectory.gov.in/webservices/lgdws/districtList?stateCode={id_}'
        query=config('district_api_link')+str(id_)
        district_data = requests.post(query).json()

        #creating the state instance for passing as foreign key
        state_=State()
        state_.statecode=id_
    
        for dist in district_data:
            district_code = dist['districtCode']
            if District.objects.filter(districtcode=district_code).exists():
                dcount += 1
                continue
            english_name = dist['districtNameEnglish']
            district_name = dist['districtNameLocal']           
            dData=District(
                            districtcode = district_code,
                            englishname= english_name,
                            localname= district_name,
                            state = state_
                            )
            dData.save()
            dcount += 1

    return HttpResponse(f"hello bhavesh you have added {dcount} data into the districts")


# Adding the subdistricts to the data 
""" the data for only 
1.maharashtra 
2.MP
3.Rajastan
4.Uttarpradesh
we are going to add
"""

def createsubdistrict(request):
    sdcount = 0
    state_ids = [23, 27, 9, 8]

    for id_ in state_ids:
        # Retrieve all districts for the current state id
        districts = District.objects.filter(state=id_)

        for district in districts:
            dist_id = district.districtcode
            #query = f'https://lgdirectory.gov.in/webservices/lgdws/subdistrictList?districtCode={dist_id}'
            query = config('subdistrict_api_link')+str(dist_id)
            response = requests.post(query)
            subdistrict_data = response.json()
    
            for subd in subdistrict_data:
                print(subd)
                sdcount += 1
                subdistrict_code = subd['subdistrictCode']
                if Subdistrict.objects.filter(subdistrictcode=subdistrict_code).exists():
                    continue
                english_name = subd['subdistrictNameEnglish']
                local_name = subd['subdistrictNameLocal']

                sd_data = Subdistrict(
                    subdistrictcode=subdistrict_code,
                    englishname=english_name,
                    localname=local_name,
                    district=district,
                )
                sd_data.save()
    return HttpResponse(f"You have added a total of {sdcount} subdistricts into the table")

def createvillage(request):
    vcount = 0
    subdistrict_data = Subdistrict.objects.all()

    for subdistrict in subdistrict_data:
        subdistrict_id = subdistrict.subdistrictcode

        # Taking village Data from API
        #query = f'https://lgdirectory.gov.in/webservices/lgdws/villageList?subDistrictCode={subdistrict_id}'
        query = config('village_api_link')+str(subdistrict_id)

        response = requests.post(query)
        village_data = response.json()


        for village in village_data:
            print(village)
            vcount += 1
            village_code=village['villageCode']
            if Village.objects.filter(villagecode =  village_code).exists():
                continue
            english_name = village['villageNameEnglish']
            local_name = village['villageNameLocal']

            v_data = Village(
                villagecode = village_code,
                englishname = english_name,
                localname = local_name,
                subdistrict = subdistrict
            )

            v_data.save()
    return HttpResponse(f"Total {vcount} number of villages are added into the table")

# Delete if there is no use of below and also delete form urls.py


# def showstate(request):
#     return HttpResponse('hello bhavesh you are on show state page')

# def showdistrict(request):
#     return HttpResponse('hello bhaveh you are on show district page')

# def showsubdistrict(request):
#     return HttpResponse('hello bhavesh you are on show district page')

# def showvillage(request):
#     return HttpResponseI('hello bhavesh you are on show village page ')


# from rest_framework.decorators import api_view
from rest_framework.views import APIView

class DistrictGeneric(APIView):
    def get(self,request):
        id_=request.GET.get('id')
        print(id_)
        district_obj = District.objects.filter(state_id=id_)
        serializer = District(district_obj,many=True)
        return Response({"status:":200,"payload":serializer.data})

class VillageGeneric(APIView):
    def get(self, request):
        village_obj = Village.objects.filter(subdistrict_id=461)

        for i in village_obj:
            print("hello")
            break
        serializer = VillageSerializer(village_obj, many=True)
        return Response({"status": 200, "payload": serializer.data})

class StateGeneric(APIView):
    def get(self, request):
        state_obj = State.objects.filter()
        serializer = StateSerializer(state_obj, many=True)
        return Response({"status": 200, "payload": serializer.data})




    





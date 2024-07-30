from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
import requests
from rest_framework.response import Response 

# Importing models 
from .models import State
from .models import Subdistrict
from .models import Village
from .models import District
from .models import Crop
from .models import Cropdatajson
from .models import Weather
from .models import fertilizer
from .models import Pesticide
# from .models import 
from .models import Cropdata


# uuid for generting the unique id 
import uuid 

# Importing serializers 
from .serializers import VillageSerializer
from .serializers import StateSerializer
from .serializers import DistrictSerializer

from django.views import View
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
        print(type(village_obj))

        for i in village_obj:
            print("hello")
            break
        serializer = VillageSerializer(village_obj, many=True)
        print(type(serializer.data))
        return Response({"status": 200, "payload": serializer.data})

class StateGeneric(APIView):
    def get(self, request):
        state_obj = State.objects.filter()
        serializer = StateSerializer(state_obj, many=True)
        return Response({"status": 200, "payload": serializer.data})


# Here we are doing it for drop down menu

def state(request):
    st = State.objects.all()
    cp=Crop.objects.all()
    context = {'states': st,'crops':cp}
    return render(request, 'states.html', context)

def crops(request):
    cp=Crop.objects.all()
    for crop in cp:
        print(crop)
    context = {'crops':cp}
    return render(request,'state.html',context)

def district(request):
    state = request.GET.get('state')
    print(state)
    dist = District.objects.filter(state_id=state)
    context = {'districts': dist}
    return render(request, 'partials/district.html', context)

def subdistrict(request):
    dist = request.GET.get('district')
    print(dist)
    subdistrict = Subdistrict.objects.filter(district_id=dist)
    context = {'subdistricts': subdistrict}
    return render(request, 'partials/subdistrict.html', context)

def village(request):
    subdistrict = request.GET.get('subdistrict')
    print(subdistrict)
    village = Village.objects.filter(subdistrict_id=subdistrict)
    context = {'villages': village}
    return render(request, 'partials/village.html', context)


# Api for generating random data 
import random


class generatedata(APIView):
    def get(self,request):

        unique_id = uuid.uuid4()
        data = request.data
        village = data['village']
        village_code = data['village_code']
        district = data['district']
        state = data['state']
        crop = data['crop']
       

       

        area = random.randint(1,39)


        soils=['clay', 'sandy', 'silty', 'peaty', 'chalky', 'loamy']
        soil_index=random.randint(0,5)
        soil=soils[soil_index]
        
        data = {
            'uniqueid':unique_id,
            'village':village,             #users input from form
            'state':state,
            'district':district,
            'village_code':village_code,
            "agricultural_data" :{
                "area":area,
                
                        "crop_type":crop,         #users input form 
                        "area_cultivated":random.randint(1,500),
                        "yeild_perhectare":random.randint(5,15),
                        "soil_type":soil,
                        "irrigation_method":'flooing',
                        "weather_data":
                        {
                            "temprature":{
                                "average":random.randint(1,500),
                                "max":random.randint(1,500),
                                "min":random.randint(1,500)
                            },
                            "Rain_fall":{
                                "total_mm":random.randint(1000,3500),
                                "rainy_days":random.randint(1000,3000)
                            },
                            "humidity":{
                                "average_percentage":random.randint(1,100)
                            }


                        },
                        "pesticide_and_fertilizer_usage": {
                                    "fertilizers": [
                                                        {
                                                            "type": "NPK",
                                                            "quantity_kg": random.randint(500,1000)
                                                        },
                                                        {
                                                            "type": "Compost",
                                                            "quantity_kg": random.randint(600,2000)
                                                        }
                                                    ],
                                    "pesticides": [
                                                    {
                                                        "type": "Fungicide",
                                                        "quantity_l": random.randint(40,200)
                                                    }
                                    ]
                            }
                    
            }
        
        
        }

       
        return Response({"status:":200,"payload":data})



class GenerateDataView(View):
    def post(self, request):
        village = request.POST.get('village')
        state = request.POST.get('state')
        district = request.POST.get('district')
        crop = request.POST.get('crop')

        village_name = Village.objects.get(villagecode=village).englishname
        crop_name = Crop.objects.get(id=crop).cropname
        district_name = District.objects.get(districtcode=district).englishname
        state_name = State.objects.get(statecode=state).englishname

        # Call the API
        api_url = 'http://127.0.0.1:8000/gene/'
        api_response = requests.get(api_url, data={'village': village_name, 'crop': crop_name,'state':state_name,'district':district_name,'village_code':village})
        
        # Check if the request was successful
        if api_response.status_code == 200:
            data = api_response.json().get('payload')
        else:
            data = None

        dt=Cropdatajson(cropdata=data)
        dt.save()

        return redirect('/state/')

        return render(request, 'data.html', {'data': data})


def savejson(request):
    jsondata = Cropdatajson.objects.values()

    for data in jsondata:
        # For storing the corp data
        unique_id = data['cropdata']['uniqueid']
        crop_type = data['cropdata']['agricultural_data']['crop_type']
        area_cultivated = data['cropdata']['agricultural_data']['area_cultivated']
        yeild_perhectare = data['cropdata']['agricultural_data']['yeild_perhectare']
        soil_type = data['cropdata']['agricultural_data']['soil_type']
        irrigation_method = data['cropdata']['agricultural_data']['irrigation_method']
        village = data['cropdata']['village_code']

        village_=Village()
        village_.villagecode=village
        
        
       
        # For storing the weather data
        temp_min = data['cropdata']['agricultural_data']['weather_data']['temprature']['max']
        temp_max = data['cropdata']['agricultural_data']['weather_data']['temprature']['min']
        temp_avg = data['cropdata']['agricultural_data']['weather_data']['temprature']['average']
        rainfall_total = data['cropdata']['agricultural_data']['weather_data']['Rain_fall']['total_mm']
        rainfall_rainy_days = data['cropdata']['agricultural_data']['weather_data']['Rain_fall']['rainy_days']
        humidity = data['cropdata']['agricultural_data']['weather_data']['humidity']['average_percentage']
        

        savecrop = Cropdata(unique_id=unique_id,
                          crop_type=crop_type,
                          area_cultivated=area_cultivated,
                          yeild_perhectare=yeild_perhectare,
                          soil_type=soil_type,irrigation_method=irrigation_method,
                          village=village_
                        )

        # For passing it as foreign key 
        cropinstance = Cropdata()
        cropinstance.unique_id = unique_id

        saveweather = Weather(temp_avg=temp_avg,
                              temp_max=temp_max,
                              temp_min=temp_min,
                              rainfall_rainy_days=rainfall_rainy_days,
                              rainfall_total=rainfall_total,
                              humidity=humidity,
                              crop=cropinstance
                            )
                    

        npk = data['cropdata']['agricultural_data']['pesticide_and_fertilizer_usage']['fertilizers'][0]['quantity_kg']
        compost = data['cropdata']['agricultural_data']['pesticide_and_fertilizer_usage']['fertilizers'][1]['quantity_kg']
        quantity_l = data['cropdata']['agricultural_data']['pesticide_and_fertilizer_usage']['pesticides'][0]['quantity_l']
        type1="npk"
        type2="compost"

        fertilizer_list=[]
        fertilizer1 = fertilizer(
                                    fertilizer_type=type1,
                                    quantity_kg=npk,
                                    crop=cropinstance
                                 )

        fertilizer2 = fertilizer(fertilizer_type=type2,
                                quantity_kg=compost,
                                crop=cropinstance
                                )

        savepesticide = Pesticide(pesticide_type="Fungicide",
                              quantity_l=quantity_l,
                              crop=cropinstance
        )

        fertilizer_list.extend([fertilizer1, fertilizer2])

        # Inserting the data into the table
        fertilizer.objects.bulk_create(fertilizer_list)
        savepesticide.save()               
        savecrop.save()
        saveweather.save()


       
        

    return redirect('/state/')
    return HttpResponse("the data you have fetched successfully ")



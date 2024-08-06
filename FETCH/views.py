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
from .models import Cropdetails
from .models import Aggridata   



# uuid for generting the unique id 
import uuid 

# Importing serializers 
from .serializers import VillageSerializer
from .serializers import StateSerializer
from .serializers import DistrictSerializer

from django.views import View



# For messages 
from django.contrib import messages

#for .env file
from decouple import config


# For user creation and login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Aggrigation functions
from django.db.models import Avg, Count, Min, Sum


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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def state(request):
    st = State.objects.all()
    cp=Crop.objects.all()
    context = {'states': st,'crops':cp}
    return render(request, 'states.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crops(request):
    cp=Crop.objects.all()
    context = {'crops':cp}
    return render(request,'state.html',context)

def district(request):
    state = request.GET.get('state')
    dist = District.objects.filter(state_id=state)
    context = {'districts': dist}
    return render(request, 'partials/district.html', context)

def subdistrict(request):
    dist = request.GET.get('district')
    subdistrict = Subdistrict.objects.filter(district_id=dist)
    context = {'subdistricts': subdistrict}
    return render(request, 'partials/subdistrict.html', context)

def village(request):
    subdistrict = request.GET.get('subdistrict')
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

        print("Generted data for --->",village_code)
        crop = data['crop']
        area = random.randint(1,39)

        soils=['clay', 'sandy', 'silty', 'peaty', 'chalky', 'loamy']
        soil_index=random.randint(0,5)
        soil=soils[soil_index]

        irrigatoins=['flooding','sprinkler','drip']
        irr_index=random.randint(0,2)
        irrigatoin=irrigatoins[irr_index]

        data = {
                    'uniqueid': unique_id,
                    'village': village,  # users input from form
                    'village_code': village_code,
                    "agricultural_data": {
                        "area": area,
                        "crop_type": crop,  # users input from form
                        "area_cultivated": random.randint(1, 500),
                        "yeild_perhectare": random.randint(5, 15),
                        "soil_type": soil,
                        "irrigation_method": irrigatoin,
                        "weather_data": {
                            "temprature": {
                                "average": random.randint(1, 50),
                                "max": random.randint(1, 50),
                                "min": random.randint(1, 50)
                            },
                            "Rain_fall": {
                                "total_mm": random.randint(1000, 3500),
                                "rainy_days": random.randint(1000, 3000)
                            },
                            "humidity": {
                                "average_percentage": random.randint(1, 100)
                            }
                        },
                        "pesticide_and_fertilizer_usage": {
                            "fertilizers": [
                                {
                                    "type": "NPK",
                                    "quantity_kg": random.randint(500, 1000)
                                },
                                {
                                    "type": "Compost",
                                    "quantity_kg": random.randint(600, 2000)
                                }
                            ],
                            "pesticides": [
                                {
                                    "type": "Fungicide",
                                    "quantity_l": random.randint(40, 200)
                                }
                            ]
                        }
                    }
                }

        return Response({"status:":200,"payload":data})



class GenerateDataView(View):
    def post(self, request):
        district = request.POST.get('district')
        crop = request.POST.get('crop')
     
        district_name = District.objects.get(districtcode=district).englishname


        subdistricts = Subdistrict.objects.filter(district_id=district)
        for subd in subdistricts:
            villages = Village.objects.filter(subdistrict_id=subd.subdistrictcode)
            for vil in villages:
                village_name = vil.englishname
                village_code = vil.villagecode
 
                # Call the API
                if crop == "All":
                    crop_names = Crop.objects.values_list('cropname', flat=True)
                    for cp in crop_names:
                        api_url = config('data_generator_api')
                        print("crop:--------->",cp)

                        api_response = requests.get(api_url, data={'village': village_name, 'crop':cp,'village_code':village_code})
                        # Check if the request was successful
                        if api_response.status_code == 200:
                            data = api_response.json().get('payload')
                        else:
                            data = None
                        district = district 
                        dt = Cropdatajson(cropdata=data,added=district,district=district_name)
                        dt.save()       
                else:
                    print("Crop_-------------___+>>>>",crop)
                    crop_name = Crop.objects.get(id=crop).cropname
                    api_url = config('data_generator_api')
                    api_response = requests.get(api_url, data={'village': village_name, 'crop':crop_name,'village_code':village_code})
                        # Check if the request was successful
                    if api_response.status_code == 200:
                        data = api_response.json().get('payload')
                    else:
                        data = None
                    district = district 
                    dt = Cropdatajson(cropdata=data,added=district,district=district_name)
                    dt.save()
                    
        messages.success(request, "Data generated and json saved in the database ")

        # return redirect('/state/')
        return redirect('/queue/')
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def savejson(request,id):
    jsondata = Cropdatajson.objects.filter(added=id).values()

    for data in jsondata:
        # For storing the corp data
        unique_id = data['cropdata']['uniqueid']
        crop_type = data['cropdata']['agricultural_data']['crop_type']
        area_cultivated = data['cropdata']['agricultural_data']['area_cultivated']
        yeild_perhectare = data['cropdata']['agricultural_data']['yeild_perhectare']
        soil_type = data['cropdata']['agricultural_data']['soil_type']
        irrigation_method = data['cropdata']['agricultural_data']['irrigation_method']
        village = int(data['cropdata']['village_code'])

        print("------------------village code =",village)


        # Resloving Foreign keys 
        village_=Village()
        village_.villagecode=int(village)


        vil=Village.objects.get(villagecode=int(village))

        state_ =  State()
        state_.statecode = vil.state_id

        district_ = District()
        district_.districtcode = vil.district_id

        subdistrict_ = Subdistrict()
        subdistrict_.subdistrictcode = vil.subdistrict_id
        
       
        # For storing the weather data
        temp_min = data['cropdata']['agricultural_data']['weather_data']['temprature']['max']
        temp_max = data['cropdata']['agricultural_data']['weather_data']['temprature']['min']
        temp_avg = data['cropdata']['agricultural_data']['weather_data']['temprature']['average']
        rainfall_total = data['cropdata']['agricultural_data']['weather_data']['Rain_fall']['total_mm']
        rainfall_rainy_days = data['cropdata']['agricultural_data']['weather_data']['Rain_fall']['rainy_days']
        humidity = data['cropdata']['agricultural_data']['weather_data']['humidity']['average_percentage']


        # For fertilizer data
        npk = data['cropdata']['agricultural_data']['pesticide_and_fertilizer_usage']['fertilizers'][0]['quantity_kg']
        compost = data['cropdata']['agricultural_data']['pesticide_and_fertilizer_usage']['fertilizers'][1]['quantity_kg']

        # For Pesticides
        quantity_l = data['cropdata']['agricultural_data']['pesticide_and_fertilizer_usage']['pesticides'][0]['quantity_l']

        
        savecrop = Cropdetails(unique_id=unique_id,
                          crop_type=crop_type,
                          area_cultivated=area_cultivated,
                          yeild_perhectare=yeild_perhectare,
                          soil_type=soil_type,irrigation_method=irrigation_method,
                          temp_avg=temp_avg,
                          temp_max=temp_max,
                          temp_min=temp_min,
                          rainfall_rainy_days=rainfall_rainy_days,
                          rainfall_total=rainfall_total,
                          humidity=humidity,
                          fertilizer_NPK_kg = npk,
                          fertilizer_COMPOST_kg = compost,
                          pesticide_type="Fungicide",
                          pesticide_quantity_l=quantity_l,
                          


                          village=village_,
                          district=district_,
                          subdistrict=subdistrict_,
                          state=state_
                        )

        # Adding data into Cropdetails                       
        savecrop.save()

    messages.success(request,"Data stored successfully into the respecive tables ")  

    # Updtating the state added
    jsondata = Cropdatajson.objects.filter(added=id).update(added=0)  

    # Call to function for aggrigating the data
    aggirgatedata()

    return redirect('/queue/')
    return HttpResponse("the data you have fetched successfully ")


def aggirgatedata():
    # Perform the aggregation
    aggregated_data = Cropdetails.objects.values('state', 'district', 'crop_type').annotate(total_area=Sum('area_cultivated'))

    for data in aggregated_data:
        state_name = State.objects.get(statecode=data['state']).englishname
        district_name = District.objects.get(districtcode=data['district']).englishname
        Aggridata.objects.update_or_create(
            state= state_name,
            district    = district_name,
            crop=data['crop_type'],
            defaults={'area_cultivated': data['total_area']}
        )
    

    print("aggrigation saved successfully ---------------------------------------------------->")
    



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def showtables(request):
    data = Aggridata.objects.distinct('district')

    context = {"data":data}
    return render(request, 'data.html', context)
    
        
        


def registeruser(request):
    context = {'uname': "", 'email': "", 'pass1': "", 'pass2': "", 'fname': "", 'lname': ""}

    if request.method == "POST":
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('uemail')
        pass1 = request.POST.get('Password1')
        pass2 = request.POST.get('Password2')

        if pass1 == pass2:
            if not User.objects.filter(username=uname).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=uname, email=email, password=pass1, first_name=fname, last_name=lname)
                    user.save()
                    messages.success(request, "User created successfully")
                    return redirect('/login/')
                else:
                    messages.error(request, "Email Already Exists")
            else:
                messages.error(request, "Username already exists")
        else:
            messages.error(request, "Passwords do not match")
        context = {'uname': uname, 'email': email, 'pass1': pass1, 'pass2': pass2, 'fname': fname, 'lname': lname}
    return render(request, 'registration.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginuser(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        password = request.POST.get('Password')

        user = authenticate(request,username=uname, password=password)

        if user is not None:
            login(request, user)
            print("Authenticated user: ", user)
            return redirect('/state/')
        else:
            print("Authentication failed")
            messages.error(request, "Please Enter the correct Credentials")
               
    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logouturl(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url="/login/")
def queue(request):

    #jsondata = Cropdatajson.objects.exclude(added=0)
    jsondata = Cropdatajson.objects.order_by('added').distinct('added').exclude(added=0)

    context = {'notupdated':jsondata}
    return render(request,'quedjson.html',context)

@login_required(login_url="/login/")
def showdistricttables(request,id):
    print(id)
    data = Aggridata.objects.filter(district=id)
    # state_name = Aggridata.objects.get(district=id).distinct('state').state
    state_names = Aggridata.objects.filter(district=id).values_list('state', flat=True).distinct()


    for dt in data:
        print(dt,"------------------------------------------------------------------")

    return render(request,'distdata.html',context={"data":data,"state":state_names[0],"district":id})
     







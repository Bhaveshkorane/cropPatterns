from django.shortcuts import render
from django.shortcuts import HttpResponse
import requests
from .models import State
from .models import District

# Create your views here.


def createstate(request):
    count=0
    stateData = requests.post('https://lgdirectory.gov.in/webservices/lgdws/stateList').json()
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
        query='https://lgdirectory.gov.in/webservices/lgdws/districtList?stateCode='+str(id_)
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

districtData=Diatricts.objects.all()

    for i in districtData:
        id=i.districtCode
        print(id)
        query='https://lgdirectory.gov.in/webservices/lgdws/subdistrictList?districtCode='+str(id)
        talukaData= requests.post(query).json()

        # dist=Diatricts.objects.filter(id=id)
        dist=Diatricts()
        dist.districtCode=id
        # dist.save()


    

        for subd in talukaData:
            print(subd)
            subDistrictCode=subd['subdistrictCode']
            if SubDistrict.objects.filter(subDistrictCode=subDistrictCode).exists():
                continue
            subDistrictNameEnglish=subd['subdistrictNameEnglish']
            subDistrictNameLocal = subd['subdistrictNameLocal']
            if subd['census2001Code']=='  ' or subd['census2001Code']=='    ':
                census2001Code=0
            else:
                census2001Code=subd['census2001Code']
            census2011Code =subd['census2011Code']
           

            sdData=SubDistrict(subDistrictCode=subDistrictCode,subDistrictNameEnglish=subDistrictNameEnglish,subDistrictNameLocal=subDistrictNameLocal,census2001Code=census2001Code,census2011Code=census2011Code,district=dist)
            sdData.save()





from threading import Thread
import urllib
import json
import datetime
from datetime import date
import time
import requests
import schedule


token_id=''
chat_id = ''

district_id="395"   #mumbai
# district_id="393" #raigad
# district_id="392" #thane

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 


def get_data(url):
    try:
        request=urllib.request.Request(url, method='GET',headers=headers) #The assembled request        
        response = urllib.request.urlopen(request)   
        data = response.read() # The data u needdecode("utf-8") 
        y = json.loads(data.decode("utf-8") )
        return y['centers']
    except:
        get_data(url)
        
        
def get_the_available_center(data):
    avail_centers=[]
    if (data):
        for centers in data:
            sessions = centers['sessions']
            for session in sessions:
                if session['available_capacity'] > 0 :
                    avail_centers.append(centers)
        return avail_centers

def result():
   
    for i in range(3):
        
        date_1 = datetime.datetime.strptime(date.today().strftime("%d-%m-%Y"), "%d-%m-%Y")
        end_date = (date_1 + datetime.timedelta(days=i))
        for_date = (end_date.strftime("%d-%m-%Y"))

        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id="+district_id+"&date="+for_date
        data=get_data(url)
        
                
        avail_centers=get_the_available_center(data)  
        if avail_centers: 
            print(time.strftime("%H:%M" , time.localtime()))
            print("Vaccines available on : ",for_date) 
            for center in avail_centers:
                for i in center['sessions']:
                    if(i["available_capacity"]>0):
                        result = "Name: " +center['name'] +"\n"+ "Address: "+ center["address"] +"\n"+ "Capacity: " + str(i["available_capacity"]) + "\n" + "Date: " + for_date + "\n" +"Age limit: " + str(i['min_age_limit']) + "\n"+ "Vaccine :" + i['vaccine'] + "\n\n" +"https://selfregistration.cowin.gov.in/"    
                        base_url = 'https://api.telegram.org/bot'+token_id+'/sendMessage?chat_id='+chat_id+'&text='+result
                        requests.get(base_url)
        else:
            print(time.strftime("%H:%M" , time.localtime()))
            print("No vaccines available on : ", for_date)
     
def call():
    
    result()    
    schedule.every(5).minutes.do(result)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
 
        
try:   
    call()
except:
    call()



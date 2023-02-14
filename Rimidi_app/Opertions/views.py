from django.shortcuts import render, redirect
import requests
import json

base_url = 'https://hapi.fhir.org/baseR4/CarePlan'
def get_details(request):
    response = requests.get(base_url)
    data = response.json()
    data_entry=[]
    data_id = []
    data_type = []
    data_status = []
    for item in data['entry']:
        data_entry.append(item)
    for item in data_entry:
        data_id.append(item['resource']['id'])
        data_type.append(item['resource']['resourceType'])
        data_status.append(item['resource']['status'])
    result = list(zip(data_id,data_type,data_status))
    return render(request, "home.html", {'results':result})
   
def CreatePageView(request): 
    if request.method == 'POST':
        resourceTypes = request.POST.get('resourceType')
        payload =  {"resourceType": resourceTypes}
        care_plan_json = json.dumps(payload)
        headers = {"Content-Type": "application/fhir+json"}
        response = requests.post(base_url, headers=headers, data=care_plan_json)
        temp_data = response.json()
        print(temp_data)
        if response.status_code == 201:
            print("CarePlan resource created successfully")
        else:
            print("Error creating CarePlan resource: ", response.text)
    return render(request, 'create_data.html')

 
def EditPageView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        updated_data = {'resourceType': request.POST.get('resourceType'), 'id':id}
        headers = {"Content-Type": "application/fhir+json"}
        print(updated_data)
        care_plan_json = json.dumps(updated_data)
        response = requests.put(base_url + "/" + str(id), headers=headers, data=care_plan_json)
        temp_data = response.json()
        print(temp_data)
        if response.status_code == 200:
            print("CarePlan resource created successfully")
        else:
            print("Error creating CarePlan resource: ")
    return render(request, "edit_data.html")
         
def DeletePageView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        response =requests.delete(base_url + "/" + str(id))
        temp_data = response.json()
        print(temp_data)  
        if response.status_code == 204:
            print('Resource deleted successfully.')
        else:
            print('Error deleting resource: ', response.status_code, response.reason)      
    return render(request, "delete_data.html")

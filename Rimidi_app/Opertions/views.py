from django.shortcuts import render, redirect
import requests
import json

base_url = 'https://hapi.fhir.org/baseR4/CarePlan'
def get_details(request):
    context = {}
    if request.method == 'POST':
        resourcetype = request.POST.get('my_dropdown')
        print(resourcetype)
        url = f'https://hapi.fhir.org/baseR4/{resourcetype}'
        response = requests.get(url)
        data = response.json()
        resources = []
        for resource in data['entry']:
            resources.append({
                'id': resource['resource']['id'],
                'resourceType': resource['resource']['resourceType'],
                'status': resource['resource']['status']
            })
        context['resources'] = resources
    return render(request, 'home.html', context)
   
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
    
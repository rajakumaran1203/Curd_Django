from django.shortcuts import render, redirect
import requests

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
        data = {'id': request.POST.get('id'), 'resourceType': request.POST.get('resourceType'), 'status': request.POST.get('status')}
        headers = {'Content-Type': 'application/json'}
        print(data)
        response = requests.post(base_url+'/resource', json=data, headers=headers)
        print(response)
    return render(request , 'create_data.html')

 
def EditPageView(request):
    return render(request , "edit_data.html")
 
        
def DeletePageView(request, id):
    response =requests.delete(f'https://hapi.fhir.org/baseR4/CarePlan/{id}')
    print(response)
    return render(request)


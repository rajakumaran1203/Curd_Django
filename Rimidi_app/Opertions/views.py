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
        #ids = request.POST.get('id')
        resourceTypes = request.POST.get('resourceType')
        #statuss = request.POST.get('status')
        payload = {"entry": [{"resource": {"resourceType": resourceTypes}}]}
        response = requests.post(base_url, data=payload)
        if response.status_code == 201:
            return redirect('get_details')
    return render(request, 'create_data.html')

 
def EditPageView(request):
    response = requests.get('https://hapi.fhir.org/baseR4/CarePlan/{id}')
    data = response.json()  
    if request.method == 'POST':
        updated_data = {'name': request.POST.get('id'), 'resourceType': request.POST.get('resourceType'), 'status': request.POST.get('status')}
        response = requests.put(f'https://hapi.fhir.org/baseR4/CarePlan/{id}', data=updated_data)
        return redirect('display_data')
    context = {'data': data}
    return render(request, "edit_data.html", context)
 
        
def DeletePageView(request, id):
    response =requests.delete(f'https://hapi.fhir.org/baseR4/CarePlan/{id}')
    return render(request, "delete_data.html")


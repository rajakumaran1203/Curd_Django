from django.urls import path
from .views import get_details, EditPageView, DeletePageView, CreatePageView
 
urlpatterns = [
    path('', get_details, name='users'),
    path('edit/', EditPageView, name='edit_data'),
    path('delete/', DeletePageView, name='delete_data'),
    path('create/', CreatePageView, name='create_data')
 
]
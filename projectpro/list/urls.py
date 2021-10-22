from django.urls import path
from . import views
from .views import *
from .views import modification


urlpatterns = [
    path('', persons_list, name='persons_list_url'),
    path('person/create/', PersonCreate.as_view(), name='person_create_url'),
    path('person/<str:slug>/', PersonDetail.as_view(), name='person_detail_url'),
    path('person/<str:slug>/update/', PersonUpdate.as_view(), name='person_update_url'),
    path('person/<str:slug>/delete/', PersonDelete.as_view(), name='person_delete_url'),
    path('organizations/', organizations_list, name='organizations_list_url'),
    path('organization/create/', OrganizationCreate.as_view(), name='organization_create_url'),
    path('organization/<str:slug>/', OrganizationDetail.as_view(), name='organization_detail_url'),
    path('organization/<str:slug>/update/', OrganizationUpdate.as_view(), name='organization_update_url'),
    path('organization/<str:slug>/delete/', OrganizationDelete.as_view(), name='organization_delete_url'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('contacts/', contacts_list, name='contacts_list_url'),
    path('modification/<str:slug>/', modification, name='modification_url'),
    path('createlist/<str:slug>/', createlist, name='createlist_url'),
    path('sendmail/<str:slug>/', sendmail, name='sendmail_url')
]


from django.urls import path
from rest_framework import routers
from . import views 

urlpatterns=[
    path('',views.data_operation,name='home'),
    path('bdd',views.bdd),
    path('stepdefination',views.step_def)
]
from django.urls import path,include
from . import views
from .views import VehicleCounter, Traffic_Signal_Program, Automation, Intersection_Signal_Program
urlpatterns = [
    path('', views.test_api, name="testapi"),
    path('vehicle-counter', VehicleCounter.as_view(), name="vehicle-counter"),
    path('traffic-signal-program/get', Traffic_Signal_Program.as_view(), name="get-traffic-signal-program"),
    path('traffic-signal-program/add', Traffic_Signal_Program.as_view(), name="add-traffic-signal-program"),
    path('automation/', Automation.as_view(), name="automation"),
    path('intersection/', Intersection_Signal_Program.as_view(), name="automation")
]

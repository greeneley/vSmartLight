from django.urls import path,include
from . import views
from .views import VehicleCounter, TrafficSignalProgram
urlpatterns = [
    path('<int:question_id>', views.test_api, name="testapi"),
    path('vehicle-counter', VehicleCounter.as_view(), name="vehicle-counter"),
    path('traffic-signal-program/get', TrafficSignalProgram.as_view(), name="get-traffic-signal-program"),
    path('traffic-signal-program/add', views.add_traffic_signal_program, name="add-traffic-signal-program"),
]

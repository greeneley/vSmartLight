import json
from django.core import serializers
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Phase, Camera, VehicleCounter, TrafficSignalProgram
from .utils import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


def test_api(request, question_id):
    response = json.dumps([{"number": 1}])
    return HttpResponse(response, content_type='text/json')


class VehicleCounter(APIView):
    def get(self, request):
        intersection_id = request.GET["intersection_id"]
        traffic_signal_program_id = request.GET["traffic_signal_program_id"]
        phase_counter, timestamp = GetPhaseVehicleCounter(intersection_id, traffic_signal_program_id)
        response = json.dumps([{
            "intersection_id": str(intersection_id),
            "traffic_signal_program_id": str(traffic_signal_program_id),
            "phase_counter": phase_counter,
            "timestamp": str(timestamp),
            "total_intersection": sum(item['total'] for item in phase_counter)
        }])
        return HttpResponse(response, content_type='text/json')

class TrafficSignalProgram(APIView):
    def get(self, request):
        intersection_id = request.GET["intersection_id"]
        traffic_signal_program_id = request.GET["traffic_signal_program_id"]
        response = Get_Traffic_Signal_Program(intersection_id, traffic_signal_program_id)
        return HttpResponse(response, content_type='text/json')
    def post(self, request):
        pass


@csrf_exempt
def add_traffic_signal_program(request):
    if request.method == "POST":
        payload = json.loads(request.body.decode('utf-8'))
        intersection_id = payload['intersection_id']
        traffic_signal_program_id = payload['traffic_signal_program_id']
        phases = payload['phase']
        yellow_time = payload['yellow_time']
        time_transition = payload['time_transition']
        green_time_max = payload['green_time_max']
        time_available_begin = payload['time_available_begin']
        time_available_end = payload['time_available_end']
        days_of_week = payload['days_of_weeK']
        new_traffic_signal_control = TrafficSignalProgram(traffic_signal_program_id=traffic_signal_program_id,
                                                          intersection_id=intersection_id,
                                                          yellow_time=yellow_time,
                                                          time_transition=time_transition,
                                                          green_time_max=green_time_max,
                                                          time_available_begin=time_available_begin,
                                                          time_available_end=time_available_end,
                                                          days_of_week=Convert_Days_Of_Week(days_of_week),
                                                          type_program=1)
        try:
            new_traffic_signal_control.save()
        except:
            response = json.dumps([{'Error': 'TrafficSignalProgram could not be added!'}])
        # try:
        #
        # except:
        #
        for phase in phases:
            new_phase = Phase(traffic_signal_program=new_traffic_signal_control,index=phase['index'],
                              green_time=phase['green_time'],
                              start_time_index=phase['start_time_index'],
                              capacity=phase['capacity'])
            try:
                new_phase.save()
            except:
                response = json.dumps([{'Error': 'Phase could not be added!'}])
        response = json.dumps([{'Success': 'Traffic signal program added successfully!'}])
        return HttpResponse(response, content_type="text/json")


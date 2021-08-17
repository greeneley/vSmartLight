import json
from django.core import serializers
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
from .utils import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from datetime import datetime


# Create your views here.


def test_api(request):
    response = json.dumps([{"number": 1}])
    # process(1, 1)
    return HttpResponse(response, content_type='text/json')


class VehicleCounter(APIView):
    def get(self, request):
        list_phase_id = request.GET["phase_id"].split(",")
        day = request.GET["day"]
        time = request.GET["time"]
        phase_counter, timestamp = Get_Phase_Vehicle_Counter(list_phase_id, day, time)
        # intersection_name = request.GET['phase_id']
        # traffic_signal_program_name = request.GET['traffic_signal_program_name']

        # intersection_id = Intersection.objects.get(name=intersection_name).intersection_id
        # traffic_signal_program_id = \
        #     TrafficSignalProgram.objects.filter(intersection_id=intersection_id,
        #                                         name=traffic_signal_program_name).values()[0][
        #         "traffic_signal_program_id"]
        #
        # phase_counter, timestamp = Get_Phase_Vehicle_Counter(intersection_id, traffic_signal_program_id)
        try:
            response = json.dumps([{
                "phase_counter": phase_counter,
                "timestamp": str(timestamp),
                "intersection_total": sum(item['total'] for item in phase_counter)
            }])
        except:
            response = json.dumps([{"status": "fail"}])
        return HttpResponse(response, content_type='text/json')


class Intersection_Signal_Program(APIView):
    def get(self, request):
        intersection_id = request.GET["intersection_id"]
        day = request.GET["day"]
        time = request.GET["time"]
        _ = Get_Traffic_Signal_Program_ID_apply(intersection_id, day, time)
        if _ is None:
            response = json.dumps([{"status": "fail"}])
        else:
            response = json.dumps([{"traffic_signal_program_id": _}])
        return HttpResponse(response, content_type='text/json')


class Traffic_Signal_Program(APIView):
    def get(self, request):
        traffic_signal_program_id = request.GET["traffic_signal_program_id"]
        # intersection_name = request.GET['id']
        # traffic_signal_program_name = request.GET['traffic_signal_program_name']
        response = Get_Traffic_Signal_Program(traffic_signal_program_id)
        return HttpResponse(response, content_type='text/json')

    @csrf_exempt
    def post(self, request):
        payload = json.loads(request.body.decode('utf-8'))
        intersection_id = payload["intersection_id"]
        traffic_signal_program_name = payload["traffic_signal_program_name"]
        phases = payload['phase']
        yellow_time = payload['yellow_time']
        time_transition = payload['time_transition']
        green_time_max = None
        time_available_begin = payload['time_available_begin']
        time_available_end = payload['time_available_end']
        days_of_week = payload['days_of_weeK']
        type_program = payload['type_program']
        active_automation = payload['active_automation']
        green_time_max = payload['green_time_max']
        active_threashold = payload['active_threashold']
        # if active_automation == 1:
        #     green_time_max = payload['green_time_max']
        #     active_threashold = payload['active_threashold']

        add_traffic_signal_program(intersection_id, traffic_signal_program_name, phases, yellow_time, time_transition,
                                   green_time_max, time_available_begin, time_available_end, days_of_week, type_program,
                                   active_automation=active_automation, active_threashold=active_threashold,
                                   performance=None,
                                   origin_traffic_signal_program_id=None, name_orgin_traffic_signal_program=None)

        response = json.dumps(
            [{'Success': 'Traffic signal program {} added successfully!'.format(traffic_signal_program_name)}])
        return HttpResponse(response, content_type="text/json")


class Automation(APIView):
    def get(self, request):
        intersection_id = request.GET['intersection_id']
        day = request.GET["day"]
        time = request.GET["time"]
        # traffic_signal_program_name = request.GET['traffic_signal_program_name']
        process(intersection_id, day, time)
        response = json.dumps([{'Success': 'A new traffic signal program added successfully!'}])
        return HttpResponse(response, content_type='text/json')

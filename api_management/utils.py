from .models import *
import json

def Convert_Bit_To_Days_Of_Week(binary):
    list_days_of_week = []
    if (binary & 1) > 0:
        list_days_of_week.append("Sunday")
    if (binary & 2) > 0:
        list_days_of_week.append("Monday")
    if (binary & 4) > 0:
        list_days_of_week.append("Tuesday")
    if (binary & 8) > 0:
        list_days_of_week.append("Wednesday")
    if (binary & 16) > 0:
        list_days_of_week.append("Thursday")
    if (binary & 32) > 0:
        list_days_of_week.append("Friday")
    if (binary & 64) > 0:
        list_days_of_week.append("Saturday")
    return list_days_of_week

def Convert_Days_Of_Week(list_days):
    value = 0
    if "Sunday" in list_days:
        value += 1
    if "Monday" in list_days:
        value += 2
    if "Tuesday" in list_days:
        value += 4
    if "Wednesday" in list_days:
        value += 8
    if "Thursday" in list_days:
        value += 16
    if "Friday" in list_days:
        value += 32
    if "Saturday" in list_days:
        value += 64
    return value


def GetPhaseVehicleCounter(intersection_id, traffic_signal_program_id):
    phase_counter = []
    phase_list = Phase.objects.filter(traffic_signal_program=traffic_signal_program_id)
    for phase in phase_list:
        phase_once = {"index": None, "total": 0, "motorbike": 0, "car": 0, "bus": 0, "truck": 0}
        phase_once["index"] = phase.index
        camera_list = Camera.objects.filter(phase_id=phase.phase_id)
        for camera in camera_list:
            object = VehicleCounter.objects.filter(camera_id=camera.camera_id).values()
            timestamp = object[0]['timestamp']
            phase_once["total"] += object[0]["total"]
            phase_once["motorbike"] += object[0]["motorbike"]
            phase_once["car"] += object[0]["car"]
            phase_once["car"] += object[0]["car"]
        phase_counter.append(phase_once)
    return phase_counter, timestamp

def Get_Traffic_Signal_Program(intersection_id, traffic_signal_program_id):
    traffic_signal_program = TrafficSignalProgram.objects.get(pk=traffic_signal_program_id)
    phase_list = Phase.objects.filter(traffic_signal_program=traffic_signal_program_id)

    phases = []
    for phase in phase_list:
        phases.append({"index": phase.index, "green_time": phase.green_time, "start_time_index": phase.start_time_index,
                       "capacity": phase.capacity})

    response = json.dumps([{
        "intersection_id": str(intersection_id),
        "traffic_signal_program_id": str(traffic_signal_program_id),
        "phase": phases,
        "yellow_time": traffic_signal_program.yellow_time,
        "time_transition": traffic_signal_program.time_transition,
        "green_time_max": traffic_signal_program.green_time_max,
        "time_available_begin": str(traffic_signal_program.time_available_begin),
        "time_available_end": str(traffic_signal_program.time_available_end),
        "days_of_week": Convert_Bit_To_Days_Of_Week(traffic_signal_program.days_of_week),
        "type_program": 0
    }])
    return response
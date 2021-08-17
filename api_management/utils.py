from .models import *
import json
import random
import datetime
from datetime import datetime


def evaluation_programs(old_program, new_program):
    return random.randint(10, 20)


def Convert_Bit_To_Days_Of_Week(binary):
    list_days_of_week = []
    if (binary & 1) > 0:
        list_days_of_week.append("Monday")
    if (binary & 2) > 0:
        list_days_of_week.append("Tuesday")
    if (binary & 4) > 0:
        list_days_of_week.append("Wednesday")
    if (binary & 8) > 0:
        list_days_of_week.append("Thursday")
    if (binary & 16) > 0:
        list_days_of_week.append("Friday")
    if (binary & 32) > 0:
        list_days_of_week.append("Saturday")
    if (binary & 64) > 0:
        list_days_of_week.append("Sunday")
    return list_days_of_week


def Convert_Days_Of_Week(list_days):
    value = 0
    if "Monday" in list_days:
        value += 1
    if "Tuesday" in list_days:
        value += 2
    if "Wednesday" in list_days:
        value += 4
    if "Thursday" in list_days:
        value += 8
    if "Friday" in list_days:
        value += 16
    if "Saturday" in list_days:
        value += 32
    if "Sunday" in list_days:
        value += 64
    return value


def Get_Phase_Vehicle_Counter(list_phase_id, day, time):
    """
    :param intersection_id:
    :param traffic_signal_program_id:
    :return:
     {
                "index": 0,
                "total": 44,
                "motorbike": 24,
                "car": 8,
                "bus": 0,
                "truck": 0
            },
            {
                "index": 1,
                "total": 47,
                "motorbike": 24,
                "car": 8,
                "bus": 0,
                "truck": 0
            }
    """
    phase_counter = []
    timestamp = day + " " + time
    for phase_id in list_phase_id:
        list_vehicle_counters = VehicleCounter.objects.filter(phase_id=phase_id)
        for obj in list_vehicle_counters:
            datetime_created = obj.time_created.split(" ")
            day_created = datetime_created[0]
            time_created = datetime_created[1]
            if day == day_created:
                if time == time_created:
                    phase = Phase.objects.get(pk=phase_id)
                    phase_once = {"index": None, "total": 0, "motorbike": 0, "car": 0, "bus": 0, "truck": 0}
                    phase_once["index"] = phase.index
                    phase_once["total"] += obj.total
                    phase_once["motorbike"] += obj.motorbike
                    phase_once["car"] += obj.car
                    phase_once["bus"] += obj.bus
                    phase_once["truck"] += obj.truck
                    phase_counter.append(phase_once)
    return phase_counter, timestamp


def Get_Traffic_Signal_Program_ID_apply(intersection_id, day, time):
    """
    :param intersection_id:
    :param day: 2021-08-17
    :param time: 10:00:00
    :return: traffic_signal_program_id
    """
    weekday = datetime.strptime(day, "%Y-%m-%d").weekday()
    list_traffic_signal_programs = TrafficSignalProgram.objects.filter(intersection_id=intersection_id)
    for element in list_traffic_signal_programs:
        if time >= str(element.time_available_begin) and time <= str(element.time_available_end):
            if (weekday & element.days_of_week) > 0:
                return element.traffic_signal_program_id
    return None


def Get_Traffic_Signal_Program(intersection_id, traffic_signal_program_id):
    """
    :param intersection_id:
    :param traffic_signal_program_id:
    :return:
    [
    {
        "intersection_id": "1",
        "traffic_signal_program_id": "1",
        "intersection_name": "Nguyễn Văn Linh - Hàm Nghi",
        "traffic_signal_program_name": "CT_01",
        "phase": [
            {
                "index": 0,
                "green_time": 27,
                "start_time_index": 0,
                "capacity": 400,
                "name": "bắc - nam, nam - bắc"
            },
            {
                "index": 1,
                "green_time": 27,
                "start_time_index": 19,
                "capacity": 300,
                "name": "đông - tây, tây - đông"
            }
        ],
        "yellow_time": 3,
        "time_transition": 0,
        "green_time_max": 60,
        "time_available_begin": "00:00:00",
        "time_available_end": "08:00:00",
        "days_of_week": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday"
        ],
        "type_program": 0,
        "active_automation": 1,
        "active_threashold": 15,
        "performance": null,
        "origin_traffic_signal_program_id": null,
        "name_orgin_traffic_signal_program": null
    }
]
    """

    # intersection_id = Intersection.objects.get(name=intersection_name).intersection_id
    # traffic_signal_program_id = \
    #     TrafficSignalProgram.objects.filter(intersection_id=intersection_id,
    #                                         name=traffic_signal_program_name).values()[0][
    #         "traffic_signal_program_id"]
    traffic_signal_program = TrafficSignalProgram.objects.get(pk=traffic_signal_program_id)
    phase_list = Phase.objects.filter(traffic_signal_program=traffic_signal_program_id)

    phases = []
    for phase in phase_list:
        phases.append({"phase_id": phase.phase_id, "index": phase.index, "green_time": phase.green_time,
                       "start_time_index": phase.start_time_index,
                       "capacity": phase.capacity, "name": phase.name})

    response = json.dumps([{
        "traffic_signal_program_id": str(traffic_signal_program_id),
        "intersection_id": traffic_signal_program.intersection_id,
        "traffic_signal_program_name": traffic_signal_program.name,
        "phase": phases,
        "yellow_time": traffic_signal_program.yellow_time,
        "time_transition": traffic_signal_program.time_transition,
        "green_time_max": traffic_signal_program.green_time_max,
        "time_available_begin": str(traffic_signal_program.time_available_begin),
        "time_available_end": str(traffic_signal_program.time_available_end),
        "days_of_week": Convert_Bit_To_Days_Of_Week(traffic_signal_program.days_of_week),
        "type_program": traffic_signal_program.type_program,
        "active_automation": traffic_signal_program.active_automation,
        "active_threashold": traffic_signal_program.active_threashold,
        "performance": traffic_signal_program.performance,
        "origin_traffic_signal_program_id": traffic_signal_program.origin_traffic_signal_program_id,
        "name_orgin_traffic_signal_program": traffic_signal_program.name_orgin_traffic_signal_program
    }])
    return response


def add_traffic_signal_program(intersection_id, traffic_signal_program_name, phases, yellow_time, time_transition,
                               green_time_max, time_available_begin, time_available_end, days_of_week, type_program,
                               active_automation=None, active_threashold=None, performance=None,
                               origin_traffic_signal_program_id=None, name_orgin_traffic_signal_program=None):
    new_traffic_signal_control = TrafficSignalProgram(intersection_id=intersection_id,
                                                      name=traffic_signal_program_name,
                                                      yellow_time=yellow_time,
                                                      time_transition=time_transition,
                                                      green_time_max=green_time_max,
                                                      time_available_begin=time_available_begin,
                                                      time_available_end=time_available_end,
                                                      days_of_week=Convert_Days_Of_Week(days_of_week),
                                                      type_program=type_program,
                                                      active_automation=active_automation,
                                                      active_threashold=active_threashold,
                                                      performance=performance,
                                                      origin_traffic_signal_program_id=origin_traffic_signal_program_id,
                                                      name_orgin_traffic_signal_program=name_orgin_traffic_signal_program,
                                                      time_created=datetime.now())
    try:
        new_traffic_signal_control.save()
    except:
        response = json.dumps([{'Error': 'TrafficSignalProgram could not be added!'}])
    # try:
    #
    # except:
    #
    for phase in phases:
        new_phase = Phase(traffic_signal_program=new_traffic_signal_control,
                          index=phase['index'],
                          green_time=phase['green_time'],
                          start_time_index=phase['start_time_index'],
                          capacity=phase['capacity'],
                          name=phase["name"])
        try:
            new_phase.save()
        except:
            response = json.dumps([{'Error': 'Phase could not be added!'}])

        # if active_automation == 1:
        #     try:
        #         list_camera = phase["camera"]
        #         for _camera in list_camera:
        #             new_camera = Camera(phase=new_phase, http=_camera["http"], rstp=_camera["rstp"])
        #             try:
        #                 new_camera.save()
        #             except:
        #                 print("Camera could not be added")
        #                 response = json.dumps([{'Error': 'Camera could not be added!'}])
        #     except:
        #         print("Camera data doesn't exist")


def get_volume_to_capacity(motocycle_count, car_count, bus_count, truck_count, capacity):
    return (0.25 * motocycle_count + 1 * car_count + 3 * bus_count + 2.5 * truck_count) / capacity


def get_level_of_service(motocycle_count, car_count, bus_count, truck_count, capacity):
    """
    Phan loai Density cua giao lo
    KHONG CAN VIET LAI
    """
    volume_to_capacity_value = get_volume_to_capacity(motocycle_count, car_count, bus_count, truck_count, capacity)
    if volume_to_capacity_value < 0.6:
        return "A"
    elif volume_to_capacity_value < 0.7:
        return "B"
    elif volume_to_capacity_value < 0.8:
        return "C"
    elif volume_to_capacity_value < 0.9:
        return "D"
    elif volume_to_capacity_value < 1:
        return "E"
    else:
        return "F"


def changeCycleTimeTrafficLightControl(traffic_signal_program, scale):
    for _item in traffic_signal_program["phase"]:
        _item["green_time"] = round(_item["green_time"] * scale)
    return traffic_signal_program


def changeGreenTimeTrafficLightControlForEachLanes(traffic_signal_program, vehicle_counter):
    for phase_program, phase_counter in zip(traffic_signal_program["phase"], vehicle_counter):
        los = get_level_of_service(phase_counter["motorbike"], phase_counter["car"], phase_counter["bus"],
                                   phase_counter["truck"], phase_program['capacity'])
        phase_program["level"] = los

    """
    """
    GREEN_TIME_MAX = traffic_signal_program["green_time_max"]
    GREEN_TIME_MIN = 15
    loss_time = 0
    count = 0

    for _element in traffic_signal_program["phase"]:
        if _element["level"] == "B":
            loss_time += round(GREEN_TIME_MAX * (1 - 0.5)) - _element["green_time"]
            count += 1
        elif _element["level"] == "C":
            loss_time += round(GREEN_TIME_MAX * (1 - 0.7)) - _element["green_time"]
            count += 1
        elif _element["level"] == "D":
            loss_time += round(GREEN_TIME_MAX * (1 - 0.3)) - _element["green_time"]
            count += 1
        elif _element["level"] == "E":
            loss_time += round(GREEN_TIME_MAX * (1 - 0.4)) - _element["green_time"]
            count += 1
        elif _element["level"] == "F":
            loss_time += GREEN_TIME_MAX - _element["green_time"]
            count += 1
        else:
            count = 1
    for _element in traffic_signal_program["phase"]:
        if _element["level"] == "B":
            _element["green_time"] = round(GREEN_TIME_MAX * (1 - 0.5))
            _element.pop('level')
        elif _element["level"] == "C":
            _element["green_time"] = round(GREEN_TIME_MAX * (1 - 0.7))
            _element.pop('level')
        elif _element["level"] == "D":
            _element["green_time"] = round(GREEN_TIME_MAX * (1 - 0.3))
            _element.pop('level')
        elif _element["level"] == "E":
            _element["green_time"] = round(GREEN_TIME_MAX * (1 - 0.4))
            _element.pop('level')
        elif _element["level"] == "F":
            _element["green_time"] = round(GREEN_TIME_MAX)
            _element.pop('level')
        else:
            _element["green_time"] = round(_element["green_time"] - (loss_time) / count if _element["green_time"] - (
                loss_time) / count >= GREEN_TIME_MIN else GREEN_TIME_MIN)
            _element.pop('level')
    return traffic_signal_program


def process(intersection_id, day, time):
    """
    1.Lấy dữ liệu đếm xe của từng pha
    1.1
    2. Lấy dữ liệu
    :return:
    """

    # intersection_id = Intersection.objects.get(name=intersection_name).intersection_id
    # traffic_signal_program_id = \
    #     TrafficSignalProgram.objects.filter(intersection_id=intersection_id,
    #                                         name=traffic_signal_program_name).values()[0][
    #         "traffic_signal_program_id"]

    traffic_signal_program_id = Get_Traffic_Signal_Program_ID_apply(intersection_id=intersection_id, day=day, time=time)
    traffic_signal_program = json.loads(Get_Traffic_Signal_Program(intersection_id, traffic_signal_program_id))[0]
    list_phase_id = []
    for _element in traffic_signal_program["phase"]:
        list_phase_id.append(_element["phase_id"])
    vehicle_counter, _ = Get_Phase_Vehicle_Counter(list_phase_id, day,time)
    total_counter = {"total": 0, "motorbike": 0, "car": 0, "bus": 0, "truck": 0, "capacity": 0}
    for _counter in vehicle_counter:
        total_counter["total"] += _counter["total"]
        total_counter["motorbike"] += _counter["motorbike"]
        total_counter["car"] += _counter["car"]
        total_counter["bus"] += _counter["bus"]
        total_counter["truck"] += _counter["truck"]
    for _phase in traffic_signal_program["phase"]:
        total_counter["capacity"] += _phase["capacity"]
    #
    los_total = get_level_of_service(total_counter["motorbike"], total_counter["car"], total_counter["bus"],
                                     total_counter["truck"], total_counter["capacity"])
    print(los_total)
    if los_total == "A":
        return None
    elif los_total == "B":
        new_program = changeCycleTimeTrafficLightControl(traffic_signal_program, scale=1.1)
    elif los_total == "C":
        new_program = changeCycleTimeTrafficLightControl(traffic_signal_program, scale=1.2)
    else:
        new_program = changeGreenTimeTrafficLightControlForEachLanes(traffic_signal_program, vehicle_counter)
    print(new_program)
    #
    add_traffic_signal_program(intersection_id=intersection_id,
                               traffic_signal_program_name="AT_" + traffic_signal_program["traffic_signal_program_name"],
                               phases=new_program["phase"],
                               yellow_time=new_program["yellow_time"],
                               time_transition=new_program["time_transition"],
                               green_time_max=new_program["green_time_max"],
                               time_available_begin=new_program["time_available_begin"],
                               time_available_end=new_program["time_available_end"],
                               days_of_week=new_program["days_of_week"],
                               type_program=1,
                               active_automation=1,
                               active_threashold=traffic_signal_program["active_threashold"],
                               performance=evaluation_programs(traffic_signal_program, new_program),
                               origin_traffic_signal_program_id=traffic_signal_program_id,
                               name_orgin_traffic_signal_program=traffic_signal_program["traffic_signal_program_name"])

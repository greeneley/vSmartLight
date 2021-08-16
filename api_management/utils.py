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


def Get_Phase_Vehicle_Counter(intersection_id, traffic_signal_program_id):
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
            phase_once["bus"] += object[0]["bus"]
            phase_once["truck"] += object[0]["truck"]
        phase_counter.append(phase_once)
    return phase_counter, timestamp

def Get_Traffic_Signal_Program(intersection_id, traffic_signal_program_id):
    """
    :param intersection_id:
    :param traffic_signal_program_id:
    :return:
    [
    {
        "intersection_id": "0",
        "traffic_signal_program_id": "1",
        "phase": [
            {
                "index": 0,
                "green_time": 15,
                "start_time_index": 0,
                "capacity": 600
            },
            {
                "index": 1,
                "green_time": 39,
                "start_time_index": 19,
                "capacity": 700
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
        "type_program": 0
    }
]
    """

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

def add_traffic_signal_program(intersection_id, traffic_signal_program_id, phases, yellow_time, time_transition, green_time_max, time_available_begin, time_available_end, days_of_week, type_program):
    new_traffic_signal_control = TrafficSignalProgram(traffic_signal_program_id=traffic_signal_program_id,
                                                      intersection_id=intersection_id,
                                                      yellow_time=yellow_time,
                                                      time_transition=time_transition,
                                                      green_time_max=green_time_max,
                                                      time_available_begin=time_available_begin,
                                                      time_available_end=time_available_end,
                                                      days_of_week=Convert_Days_Of_Week(days_of_week),
                                                      type_program=type_program)
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
                          capacity=phase['capacity'])
        try:
            new_phase.save()
        except:
            response = json.dumps([{'Error': 'Phase could not be added!'}])


def getVolumeToCapacity(motocycle_count, car_count, bus_count, truck_count, capacity):
    return (0.25*motocycle_count + 1*car_count + 3*bus_count + 2.5*truck_count)/capacity


def get_level_of_service(motocycle_count, car_count, bus_count, truck_count, capacity):
    """
    Phan loai Density cua giao lo
    KHONG CAN VIET LAI
    """
    volume_to_capacity_value = getVolumeToCapacity(motocycle_count, car_count, bus_count, truck_count, capacity)
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

# def evaluation_road():
#     # traffic_signal_program = Get_Traffic_Signal_Program()
#     # Vehiclle_Counter = Get_Phase_Vehicle_Counter()
#     los = get_level_of_service(Vehicle_Counter[0], traffic_signal_program.phase[0].capacity)
#     return los


def changeCycleTimeTrafficLightControl(traffic_signal_program, scale):
    for _item in traffic_signal_program["phase"]:
        _item["green_time"] = round(_item["green_time"]*scale)
    return traffic_signal_program

def changeGreenTimeTrafficLightControlForEachLanes(traffic_signal_program, vehicle_counter):
    for phase_program, phase_counter in zip(traffic_signal_program["phase"], vehicle_counter):
        los = get_level_of_service(phase_counter["motorbike"], phase_counter["car"], phase_counter["bus"], phase_counter["truck"], phase_program['capacity'])
        phase_program["level"] = los

    """
    """
    GREEN_TIME_MAX = traffic_signal_program["green_time_max"]
    GREEN_TIME_MIN = 15
    loss_time = 0
    count = 0

    for _element in traffic_signal_program["phase"]:
        if _element["level"] == "B":
            loss_time += round(GREEN_TIME_MAX*(1-0.5)) - _element["green_time"]
            count += 1
        elif _element["level"] == "C":
            loss_time += round(GREEN_TIME_MAX*(1-0.7)) - _element["green_time"]
            count += 1
        elif _element["level"] == "D":
            loss_time += round(GREEN_TIME_MAX*(1-0.3)) - _element["green_time"]
            count += 1
        elif _element["level"] == "E":
            loss_time += round(GREEN_TIME_MAX*(1-0.4)) - _element["green_time"]
            count += 1
        elif _element["level"] == "F":
            loss_time += GREEN_TIME_MAX - _element["green_time"]
            count += 1
        else:
            count = 1
    for _element in traffic_signal_program["phase"]:
        if _element["level"] == "B":
            _element["green_time"] = round(GREEN_TIME_MAX(1-0.5))
            _element.pop('level')
        elif _element["level"] == "C":
            _element["green_time"] = round(GREEN_TIME_MAX(1-0.7))
            _element.pop('level')
        elif _element["level"] == "D":
            _element["green_time"] = round(GREEN_TIME_MAX(1-0.3))
            _element.pop('level')
        elif _element["level"] == "E":
            _element["green_time"] = round(GREEN_TIME_MAX(1-0.4))
            _element.pop('level')
        elif _element["level"] == "F":
            _element["green_time"] = round(GREEN_TIME_MAX)
            _element.pop('level')
        else:
            _element["green_time"] = round(_element["green_time"] - (loss_time)/count if _element["green_time"] - (loss_time)/count >= GREEN_TIME_MIN else GREEN_TIME_MIN)
            _element.pop('level')
    return traffic_signal_program
def process(intersection_id, traffic_signal_program_id):

    """
    1.Lấy dữ liệu đếm xe của từng pha
    1.1
    2. Lấy dữ liệu
    :return:
    """

    traffic_signal_program = json.loads(Get_Traffic_Signal_Program(intersection_id, traffic_signal_program_id))[0]
    vehicle_counter, _ = Get_Phase_Vehicle_Counter(intersection_id, traffic_signal_program_id)

    total_counter = {"total": 0, "motorbike": 0, "car": 0, "bus": 0, "truck": 0, "capacity": 0}
    for _counter in vehicle_counter:
        total_counter["total"] += _counter["total"]
        total_counter["motorbike"] += _counter["motorbike"]
        total_counter["car"] += _counter["car"]
        total_counter["bus"] += _counter["bus"]
        total_counter["truck"] += _counter["truck"]
    for _phase in traffic_signal_program["phase"]:
        total_counter["capacity"] += _phase["capacity"]
    print(total_counter)

    los_total = get_level_of_service(total_counter["motorbike"], total_counter["car"], total_counter["bus"], total_counter["truck"], total_counter["capacity"])
    print(los_total)
    if los_total == "A":
        pass
    elif los_total == "B":
        new_program = changeCycleTimeTrafficLightControl(traffic_signal_program, scale=1.1)
    elif los_total == "C":
        new_program = changeCycleTimeTrafficLightControl(traffic_signal_program, scale=1.2)
    else:
        new_program = changeGreenTimeTrafficLightControlForEachLanes(traffic_signal_program, vehicle_counter)

    add_traffic_signal_program(int(new_program["intersection_id"]), 201, new_program["phase"],new_program["yellow_time"], new_program["time_transition"], new_program["green_time_max"],
                               new_program["time_available_begin"], new_program["time_available_end"], new_program["days_of_week"], type_program = 1)




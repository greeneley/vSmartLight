from django.db import models


# Create your models here.

class AdaptiveSignalProgram(models.Model):
    adaptive_signal_program_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    alarm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adaptive_signal_program'


class Camera(models.Model):
    camera_id = models.AutoField(primary_key=True)
    phase = models.ForeignKey('Phase', models.DO_NOTHING)
    device_name = models.CharField(max_length=45, blank=True, null=True)
    ip_device = models.CharField(max_length=45, blank=True, null=True)
    port_device = models.SmallIntegerField(blank=True, null=True)
    mac_device = models.CharField(max_length=45, blank=True, null=True)
    http = models.TextField(db_column='HTTP')  # Field name made lowercase.
    rstp = models.TextField(db_column='RSTP', blank=True, null=True)  # Field name made lowercase.
    longitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camera'



class Direction(models.Model):
    direction_id = models.AutoField(primary_key=True)
    phase = models.ForeignKey('Phase', models.DO_NOTHING)
    name = models.CharField(max_length=45, blank=True, null=True)
    longitude_origin = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    latitude_origin = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude_destination = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    latitude_destination = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direction'


class Intersection(models.Model):
    intersection_id = models.AutoField(primary_key=True)
    light_control = models.ForeignKey('LightControl', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    ip_tu_dieu_khien = models.CharField(max_length=45, blank=True, null=True)
    mac_tu_dieu_khien = models.CharField(max_length=45, blank=True, null=True)
    phase_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intersection'



class LightControl(models.Model):
    light_control_id = models.AutoField(primary_key=True)
    ip_control_device = models.CharField(unique=True, max_length=45, blank=True, null=True)
    mac_control_device = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'light_control'


class LightControlHistory(models.Model):
    light_control_history_id = models.AutoField(primary_key=True)
    intersection = models.ForeignKey(Intersection, models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)
    traffic_signal_file = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'light_control_history'


class Phase(models.Model):
    phase_id = models.AutoField(primary_key=True)
    traffic_signal_program = models.ForeignKey('TrafficSignalProgram', models.DO_NOTHING)
    index = models.IntegerField(blank=True, null=True)
    green_time = models.IntegerField(blank=True, null=True)
    start_time_index = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phase'


class TrafficSignalProgram(models.Model):
    traffic_signal_program_id = models.AutoField(primary_key=True)
    intersection = models.ForeignKey(Intersection, models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    yellow_time = models.IntegerField(blank=True, null=True)
    time_transition = models.IntegerField(blank=True, null=True)
    green_time_max = models.IntegerField(blank=True, null=True)
    time_available_begin = models.TimeField(blank=True, null=True)
    time_available_end = models.TimeField(blank=True, null=True)
    days_of_week = models.IntegerField(blank=True, null=True)
    type_program = models.IntegerField(blank=True, null=True)
    active_automation = models.IntegerField(blank=True, null=True)
    active_threashold = models.IntegerField(blank=True, null=True)
    performance = models.CharField(max_length=45, blank=True, null=True)
    origin_traffic_signal_program_id = models.IntegerField(blank=True, null=True)
    name_orgin_traffic_signal_program = models.CharField(max_length=45, blank=True, null=True)
    time_created = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'traffic_signal_program'


class TrafficSignalProgramLog(models.Model):
    traffic_signal_program_log_id = models.AutoField(primary_key=True)
    intersection_id = models.IntegerField(blank=True, null=True)
    traffic_signal_program_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    type_program = models.IntegerField(blank=True, null=True)
    time_generate_new_program = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'traffic_signal_program_log'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    sso_id = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class VehicleCounter(models.Model):
    record_id = models.AutoField(primary_key=True)
    intersection_id = models.IntegerField(blank=True, null=True)
    phase = models.ForeignKey(Phase, models.DO_NOTHING)
    time_created = models.CharField(max_length=100, blank=True, null=True)
    motorbike = models.IntegerField(blank=True, null=True)
    car = models.IntegerField(blank=True, null=True)
    bus = models.IntegerField(blank=True, null=True)
    truck = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_counter'

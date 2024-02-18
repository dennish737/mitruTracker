import os
from dotenv import dotenv_values
import random
import time
import os
import time
from datetime import datetime


import numpy as np
import pandas as pd
import pandas.io.sql as psql

import utils as utils
import db_mysql as db

import mariadb as database

from haversine import haversine, Unit
from paho.mqtt import client as mqtt_client
from rule_class import Vehicle, StatusMessage

""" Rules 
TrailerDataCapture.py collect the data from the MITRU vehicles, and provides a time series of information
and current status information. 
Rules.py analyzes and looks for conditions where a message needs to be sent. For example; by monitoring the 
vehicle temperature and voltage, we can send an alert when the values exceeds a threshold (e.g. (to hot, to cold), or
(low voltage, over voltage))

"""

# check functions

def GT(val, limit):
    rtn = False
    if val > limit:
        rtn = True
    return rtn

def GE(val, limit):
    rtn = False
    if val >= limit:
        rtn = True
    return rtn

def LT(val, limit):
    rtn = False
    if val < limit:
        rtn = True
    return rtn

def LE(val, limit):
    rtn = False
    if val <= limit:
        rtn = True
    return rtn

def EQ(val, limit):
    rtn = False
    if val <= limit:
        rtn = True
    return rtn

def delta_time(t1,t2):
    dt = (t2 - t1).seconds  # difference in time in seconds
    return dt

def sys_delta_time(t):
    timestamp = pd.Timestamp(datetime.utcnow(), tz='UTC').tz_convert(None)
    dt = delta_time(t, timestamp)
    return dt


def time_check(val, limit):
    rtn = False
    if val > limit:
        rtn = True
    return rtn

operators = { 'GT': GT, 'GE': GE, 'LT': LT, 'LE': LE, 'EQ': EQ, 'time_check': time_check}

def queue_message(vehicle, rule_id, severity, message):
    timestamp = pd.Timestamp(datetime.utcnow(), tz='UTC')
    status_id = 0
    if severity == 'ALERT':
        status_id = vehicle.check_alerts(rule_id)
    elif severity == 'ALARM':
        status_id = vehicle.check_alarms(rule_id)
    if status_id == 0:
        status_msge = StatusMessage(rule_id, timestamp, vehicle.get_id(), severity, message)
        vehicle.add_message(status_msge)
    else:
        vehicle.update_message(status_id)

def clear_message(vehicle, rule):
    timestamp = pd.Timestamp(datetime.utcnow(), tz='UTC')
    rule_id = rule['id']
    severity = rule['severity']
    status_id = 0
    if severity == 'ALERT':
        status_id = vehicle.check_alerts(rule_id)
    elif severity == 'ALARM':
        status_id = vehicle.check_alarms(rule_id)
    if status_id != 0:
        vehicle.clear_status_msg( status_id, timestamp)


def temp_check(vehicle, rule):
    temp = vehicle.get_temp()
    limit = rule['limit_value']
    vname = vehicle.name
    severity = rule['severity']
    rule_id = rule['id']
    if temp is not None:
        if operators[rule['rule_function']](temp, limit):
            message = rule['message'].format(vname, severity, limit, temp)
            queue_message(vehicle, rule_id, severity, message)
        else:
            clear_message(vehicle, rule)


def volt_check(vehicle, rule):
    volts = vehicle.get_volts()
    limit = rule['limit_value']
    if volts is not None:
        vname = vehicle.name
        severity = rule['severity']
        rule_id = rule['id']
        if operators[rule['rule_function']](volts, limit):
            message = rule['message'].format(vname, severity, limit, volts)
            queue_message(vehicle, rule_id, severity, message)
        else:
            clear_message(vehicle, rule)

def no_contact(vehicle, rule):
    contact = vehicle.contact()
    limit = rule['limit_value']
    if contact is not None:
        vname = vehicle.name
        severity = rule['severity']
        rule_id = rule['id']
        if operators[rule['rule_function']](contact, limit):
            message = rule['message'].format(vname, severity, limit, contact)
            queue_message(vehicle, rule_id,  severity, message)
        else:
            clear_message(vehicle, rule)


rule_functions = {'temp_check': temp_check, 'volt_check': volt_check, 'no_contact': no_contact}

def run(conn, mqtt_conn, topic_base):



    # on startup make connection to MQtt
    #mqtt_conn.loop_start()
    msg_count = 0

    vehicles = db.get_vehicles(conn)
    locations = None
    mqtt_strings = []
    mqtt_loc_data = {}
    readings = None
    timestamp = pd.Timestamp(datetime.datetime.utcnow(), tz='UTC').tz_convert(None)
    for index, row in vehicles.iterrows():
        last_location = db.get_last_location(conn, row['id'])

        if not last_location.empty:
            changes = db.get_location_changes(conn, row['id'])
            print(changes)
            #dt = delta_t(last_location.iloc[1]['last_reading'], last_location.iloc[0]['last_reading'])
            #sys_dt = delta_t(last_location.iloc[0]['last_reading'], timestamp)
            #loc1 = (last_location.iloc[1]['latitude'], last_location.iloc[1]['longitude'])
            #loc2 = (last_location.iloc[0]['latitude'], last_location.iloc[0]['longitude'])
            #print(distance(loc1,loc2))
            #last_readings = get_last_readings(conn, row['id'])
            # walk the row and create mqtt entries


    """
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        publish(client, topic, msg )
        msg_count += 1

    """
# MQTT
def connect_mqtt(client_id, username, password):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            print("No DB Connection")
            exit(1)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, message):

    result = client.publish(topic, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    return status





if __name__ == '__main__':

    """ On startup, get the list of vehicles """
    config = dotenv_values(".pyenv")
    username = config["DB_USERNAME"]
    password = config["DB_PASSWD"]
    host = config["DB_HOST"]

    # On startup, make a connection to the DB, and get the vehicle list
    conn = db.dbconnect(host, username, password)
    if conn is None:
        print("No DB Connection")
        exit(1)

    # get the INFO, ALERT and ALARM rules
    df_info = db.get_rules(conn, severity='INFO')
    df_alerts = db.get_rules(conn, severity='ALERT')
    df_alarms = db.get_rules(conn, severity='ALARM')


    vehicles_info = db.get_vehicles(conn)
    vehicles = {}
    for index, row in vehicles_info.iterrows():
        name = row['name']
        vehicles[name] = Vehicle(conn, row)
        vehicles[name].get_data()

    for k, v in vehicles.items():
        #print('k=: ', k, ' , v=: ', v)

        if not df_alarms.empty:
            vehicle_alarms = df_alarms[df_alarms['v_id'] == v.id]

            if not vehicle_alarms.empty:
                for i, r in vehicle_alarms.iterrows():
                    rule_functions[r['rule_class']](v, r)

        if not df_alerts.empty:
            vehicle_alerts = df_alerts[df_alerts['v_id'] == v.id]

            if not vehicle_alarms.empty:
                for i, r in vehicle_alerts.iterrows():
                    rule_functions[r['rule_class']](v, r)
        v.queue_send()


    """
    # on startup make connection to MQTT
    mqtt_conn = None
    #mqtt_conn = connect_mqtt(client_id, mqtt_username, mqtt_password)
    run(conn, mqtt_conn, topic_base)
    conn.close()
    """




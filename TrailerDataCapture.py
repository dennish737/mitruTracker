import os
from dotenv import dotenv_values

import time
import re
from datetime import datetime
import ssl
import numpy as np
import pandas as pd
import pandas.io.sql as psql

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from haversine import haversine, Unit
import mariadb as database
import utils as utils

import db_mysql as db

""" Trailer Data Capture
This script uses the APRS.fi and APRS-IS system retrieve the APRS Data  sent by the trailers.

Each trailer has an APRS Tracker device that reports the position and 'status' of the trailer.
This utility scrapes the data from APRS and adds it to a data base. This data is then processed by
the alert package to determine if a message is to be sent. Because the broadcast rate of the MITRU
 trailers is different, the 'Last Time' is used to determine if new data has arrived. If no new data 
 has arrived, no update to the database is made.
 
 In additon to scrapping hte data, this tool also standardizes te data output, for consistent alarm processing.
 """


def strip_end(text, suffix):
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    return text

def get_page(url, data_type):
    data_dict = {}
    context = ssl._create_unverified_context()
    page = urlopen(url, context=context)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.findAll("table")

    for table in tables:
        rows = table.find_all(['tr'])

        for row in rows:
            headers = row.find_all('th')
            for header in headers:
                cells = row.find_all('td')
                for cell in cells:
                    ht = strip_end(header.text.strip(),':')
                    if ht == "Location":
                        values = cell.text.split('-')
                        # value[0] latitude longitude in degree and min
                        latlong = values[0].replace(u'\xa0', u'').split(' ')
                        lat = utils.ddm2dec(latlong[0])
                        long = utils.ddm2dec(latlong[1])
                        data_dict[ht] = (lat,long)
                        data_dict['Locator'] = values[1].split(' ')[2]
                    elif ht == "Last position":
                        values = cell.text.split('(')
                        #data_dict[ht] = datetime.strptime(values[0].strip(), '%Y-%m-%d %H:%M:%S %Z')
                        data_dict[ht] = values[0].strip()
                    elif ht == "Last telemetry":
                        values = cell.text.split('(')
                        #data_dict[ht] = datetime.strptime(values[0].strip(), '%Y-%m-%d %H:%M:%S %Z')
                        data_dict[ht] = values[0].strip()
                        if data_type == 'info':
                            data_dict['Channels'] = values[1]
                    elif ht == "Altitude":
                        values = cell.text.split(' ')[0]
                        data_dict["Altitude"] = float(re.findall(r'\d+', values)[0])
                    else:
                        data_dict[ht] = cell.text

    return data_dict

def parse_channels(channel_values):
    data_dict = {}
    
    start = 0
    channel_number = 0
    j = 0
    while j >= 0:
        channel_text = ''
        channel_number +=1
        channel_key = "Ch {0}".format(channel_number)
        j = channel_values.find(channel_key, start)

        if j != -1:
            start = j + len(channel_key)
            k = channel_values.find(',', j)
            if k == -1:
                channel_text = channel_values[j:]
            else:
                channel_text = channel_values[j:k]
            # split test at ':'
            text = channel_text.split(':')
            val_text = text[1].strip().split(' ')
            if len(val_text) > 1:
                data_dict[channel_key] = (float(val_text[0]), val_text[1])
            else:
                data_dict[channel_key] = (float(val_text[0]), 'None')
    
    return data_dict

def parse_named_channels(channel_values):
    data_dict = {}
    start = 0
    channel_number = 0
    j = 0
    channel_strings = ['Battery', 'Temp']
    while channel_number < 5:
        channel_number += 1
        channel_key = "Ch {0}".format(channel_number )
        if channel_number < len(channel_strings) + 1:
            channel_str = channel_strings[channel_number - 1]
        else:
            channel_str = "Channel {0}".format(channel_number)
        j = channel_values.find(channel_str, start)

        if j != -1:
            channel_text = ''

            start = j + len(channel_str)
            k = channel_values.find('(', j)
            if k == -1:
                channel_text = channel_values[j:]
            else:
                channel_text = channel_values[j:k]
            # split test at ':'
            text = channel_text.split(':')
            val_text = text[1].strip().split(' ')
            if len(val_text) > 1:
                data_dict[channel_key] = (float(val_text[0]), val_text[1])
            else:
                data_dict[channel_key] = (float(val_text[0]), 'None')
        else:
            channel_key = "Ch {0}".format(channel_number)
            data_dict[channel_key] = (float(0.0), 'None')
    return data_dict


def parse_telem_channels(channel_values):
    data_dict = {}
    
    start = 0
    channel_number = 0
    j = 0
    while j >= 0:
        channel_text = ''
        channel_number +=1
        channel_str = "Channel {0}".format(channel_number)
        channel_key = "Ch {0}".format(channel_number)
        j = channel_values.find(channel_str, start)

        if j != -1:
            start = j + len(channel_str)
            k = channel_values.find('(', j)
            if k == -1:
                channel_text = channel_values[j:]
            else:
                channel_text = channel_values[j:k]
            # split test at ':'
            text = channel_text.split(':')
            val_text = text[1].strip().split(' ')
            if len(val_text) > 1:
                data_dict[channel_key] = (float(val_text[0]), val_text[1])
            else:
                data_dict[channel_key] = (float(val_text[0]), 'None')


    return data_dict


def parse_telemetry( device):
    data_dict = {}
    url = "https://aprs.fi/telemetry/a/" + device
    data = get_page(url, 'telemetry')

    channel_values = {}
    if 'Values' in data:
        j = data['Values'].find('Channel')
        if j >= 0:
            channel_values = parse_telem_channels(data['Values'])
        else:
            channel_values = parse_named_channels(data['Values'])
        # update data dictionary
    for key, val in data.items():
        if key == 'Values':
            data_dict['Channels'] = channel_values
        else:
            data_dict[key] = val        
    return data_dict

def parse_info( device):
    data_dict = {}
    url = "https://aprs.fi/info/a/" + device
    data = get_page(url, 'info')
    channel_values = {}
    if 'Channels' in data:
        channel_values = parse_channels(data['Channels'])
    # update data dictionary
    for key, val in data.items():
        if key == 'Values':
            data_dict[key] = channel_values
        else:
            data_dict[key] = val        
    return data_dict

def get_vehicle_data(vehicle, id, url_type):
    data = None

    if url_type == 'info':
        data = parse_info(vehicle)
    else:
        data = parse_telemetry(vehicle)
    data['vid'] = id
    return data

def get_location(data, locations):

    new_data_dict = {'v_id': data['vid'], 'last_reading': data['Last position'],
                     'latitude': data['Location'][0], 'longitude': data['Location'][1],
                     'locator': data['Locator'], 'altitude_m': data['Altitude']}

    if locations is None:
        # if locations is None, there was no historical data, or we were not able to connect to the DB
        # in that case use ethe first sample to start the dataframe
        locations = pd.DataFrame(new_data_dict, index=[0])
        locations['last_reading'] = pd.to_datetime(locations['last_reading'], format='%Y-%m-%d %H:%M:%S %Z')
    else:
        df = pd.DataFrame(new_data_dict, index=[0])
        df['last_reading'] = pd.to_datetime(df['last_reading'], format='%Y-%m-%d %H:%M:%S %Z')
        locations = pd.concat([locations, df], axis=0)
    return locations

def get_readings(data, readings):
    channels = data['Channels']
    channel_list = ['Ch 1', 'Ch 2', 'Ch 3', 'Ch 4', 'Ch 5']
    num_channels = 5

    if len(channels) > 0:
        #print("len channels) = {0}".format(len(channels)))
        # process channel information
        for i in range(num_channels):
            new_data_dict = {'v_id': data['vid'], 'c_id': (i + 1), 'last_reading': data['Last position'],
                                 'latitude': data['Location'][0], 'longitude': data['Location'][1],
                                 'altitude_m': data['Altitude'], 'chan_value': channels[channel_list[i]][0],
                             'chan_units': channels[channel_list[i]][1]}
            #print("Readings New Data ---------------------------------------------------")
            #print(new_data_dict)

            if readings is None:
                # if locations is None, there was no historical data, or we were not able to connect to the DB
                # in that case use ethe first sample to start the dataframe
                readings = pd.DataFrame(new_data_dict, index=[0])
                readings['last_reading'] = pd.to_datetime(readings['last_reading'], format='%Y-%m-%d %H:%M:%S %Z')
            else:
                df = pd.DataFrame(new_data_dict, index=[0])
                df['last_reading'] = pd.to_datetime(df['last_reading'], format='%Y-%m-%d %H:%M:%S %Z')
                readings = pd.concat([readings, df], axis=0)

    else:
        print("no channels")

    return readings



if __name__ == '__main__':

    """ On startup, get the list of vehicles """
    config = dotenv_values(".pyenv")
    username = config["DB_USERNAME"]
    password = config["DB_PASSWD"]
    host = config["DB_HOST"]
    # time between vehicle poles
    wait_time = 1

    # On startup, make a connection to the DB, and get the vehicle list
    conn = db.dbconnect(host, username, password)
    if conn is None:
        print("No DB Connection")
        exit(1)

    # on startup make connection to MQtt
    #mqtt_conn = connect_mqtt(client_id, mqtt_username, mqtt_password)

    vehicles = db.get_vehicles(conn)

    # use the vehicle list for data
    # Now that we have a list of vehicles to monitor, we can begin to query APRS
    # for there information. We will do this in batches, with and interval between
    # batches of 'sleep_time'. Also, to prevent over loading the APRS system we want to
    # space out our request, so we will delay 'wait_time' between each vehicle request.
    # After collecting data for a vehicle, we will check the data, update the database.
    #

    locations = None

    readings = None
    for index, row in vehicles.iterrows():
        data = get_vehicle_data(row['vid'], row['id'],'telemetry')
        # Note data contains 'Comment' and 'Mic-e message' values
        # We currently do no capture these values, but may in the future.
        locations = get_location(data, locations)
        readings = get_readings(data, readings)

    #print(locations)
    #print(readings)
    # At this point we have location readings and maybe channel reading for each vehicle

    # Check:
    # Location reporting time (locations[last_reading])
    # Why?
    # APRS-IS will store the last reported position for months, and report that position
    # whenever requested. But will stop reporting the channel information after a few hours.
    # One of the questions we would like answered -  is has a vehicle gone dark (e.g.
    # stopped transmitting, or is unreachable). We can do this by looking at the 'last_reading' time
    # value. We can assume that a healthy vehicle will report at least once every 27 hours

    timestamp = pd.Timestamp(datetime.utcnow(), tz='UTC')
    # add column for loc


    for index, row in locations.iterrows():

        #delta_t = pd.Timedelta(timestamp - row['last_reading']).seconds / 3600.0  # difference in reading time and system time
        # check for channel data
        n = len(readings[readings['v_id']==row['v_id']])

        #print("working on {0}".format(row['v_id']))
        #row['last_reading'] = row['last_reading'].tz_convert(None)
        db.update_locations(conn, row)
        changes = db.get_location_changes(conn, row['v_id'])
        if len(changes) > 0:
            db.update_changes(conn,changes)
        if n > 0:
            db.update_readings(conn, readings[readings['v_id'] == row['v_id']])

        else:
            print("vehicle {0} has no readings".format(row['v_id']))

        time.sleep(wait_time)








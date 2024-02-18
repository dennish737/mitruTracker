import os

from datetime import datetime
import mariadb as database
import pandas as pd
import numpy as np
import pandas.io.sql as psql

import utils as utils
from dataclasses import dataclass

import db_mysql as db

@dataclass
class StatusMessage:
    rule_id: int
    timestamp: np.datetime64
    v_id: int
    severity: str
    message: str


class Vehicle:
    def __init__(self, conn, row_info):
        self.connection = conn
        self.name = row_info['name']
        self.id = row_info['id']
        self.status = row_info['status']
        self.base = row_info['base']
        self.base_location = row_info['base_loc']
        self.info_enabled = row_info['info_enabled']
        self.alert_enabled = row_info['alert_enabled']
        self.alarm_enabled = row_info['alarm_enabled']

        self.location = None
        self.readings = None
        self.changes = None
        self.last_contact = None
        self.alarms = None
        self.alerts = None
        self.status_messages = []

    def get_data(self):
        self.location = db.get_last_location(self.connection, self.id)
        self.readings = db.get_last_readings(self.connection, self.id)
        self.changes = db.get_location_changes(self.connection, self.id)
        self.last_contact = db.get_last_contact(self.connection, self.id)
        self.alarms = db.get_alarms(self.connection, self.id)
        self.alerts = db.get_alerts(self.connection, self.id)

    def get_id(self):
        return self.id

    def contact(self):
        lc = None
        if self.last_contact is not None:
            lc = self.last_contact
        return lc[0]

    def get_temp(self):
        temp = None
        if self.readings is not None:
            df = self.readings[self.readings['c_id']==2]
            temp = df['chan_value'][1]
        return temp

    def get_volts(self):
        volts = None
        if self.readings is not None:
            df = self.readings[self.readings['c_id'] == 1]
            volts = df['chan_value'][0]
        return volts

    def check_alarms(self, rule_id):
        alarm_id = 0   # no alarms

        if not self.alarms.empty:
            # we have outstanding alarms see if our alarm is in the set
            outstanding_alarms = self.alarms.loc[self.alarms['rule_id'] == rule_id]
            if not outstanding_alarms.empty:
                # get the alarm id
                alarm_id = outstanding_alarms.loc[0]['id']

        return alarm_id

    def check_alerts(self, rule_id):
        alert_id = 0

        if not self.alerts.empty:
            # we have outstanding alert see if our alarm is in the set
            outstanding_alerts = self.alerts.loc[self.alerts['rule_id'] == rule_id]
            if not outstanding_alerts.empty:
                # get the alarm id
                alert_id = outstanding_alerts.loc[0]['id']

        return alert_id

    def add_message(self, status_message):
        self.status_messages.append(status_message)


    def update_message(self, status_id):
        print("update message")
        db.update_status(self.connection, status_id)

    def queue_send(self):
        for status_message in self.status_messages:
            db.insert_status(self.connection, status_message.rule_id, status_message.timestamp, status_message.v_id,
                             status_message.severity, status_message.message)

    def clear_status_msg(self, status_id, timestamp):
        db.clear_status(self.connection, status_id, timestamp)

import os
from dotenv import dotenv_values

import time
import re
from datetime import datetime
import ssl
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import db_mysql as db
import mariadb as database

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration Data

config = dotenv_values(".pyenv")
email = config["EMAIL_USERNAME"]
pas = config["EMAIL_PASSWD"]
host = config["DB_HOST"]


# The server we use to send emails in our case it will be gmail but every email provider has a different smtp
# and port is also provided by the email provider.
smtp = "smtp-mail.outlook.com"
port = 587

def send_alert(sms_gateway, subject, message):
    print("send to: ", sms_gateway)
    print("subject: ", subject)
    print("message: ", message)

    # This will start our email server
    server = smtplib.SMTP(smtp,port)
    # Starting the server
    server.starttls()
    # Now we need to login
    server.login(email,pas)

    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    # Make sure you add a new line in the subject
    msg['Subject'] = subject
    # Make sure you also add new lines to your body
    body = message
    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    server.sendmail(email,sms_gateway,sms)


def format_provider_email_address(contact):
    number = contact['phone']
    domain = contact['sms']

    return f"{number}@{domain}"

if __name__ == '__main__':
    send_cleared_messages = True
    config = dotenv_values(".pyenv")
    username = config["DB_USERNAME"]
    password = config["DB_PASSWD"]
    host = config["DB_HOST"]

    # On startup, make a connection to the DB, and get the vehicle list
    conn = db.dbconnect(host, username, password)
    if conn is None:
        print("No DB Connection")
        exit(1)

    vehicles = db.get_vehicles(conn)
    # get unsent messages
    messages = db.get_new_messages(conn)
    timestamp = pd.Timestamp(datetime.utcnow(), tz='UTC')
    for index, row in messages.iterrows():
        message_id = row['id']
        v_id = row['v_id']
        vehicle = vehicles.loc[vehicles['id'] == v_id]
        v_name = vehicle['name'].values[0]
        rule_id = row['rule_id']
        severity = row['severity']
        message = row['message']
        subject = f"{v_name} {severity} rule {rule_id}  Message_id:{message_id}"
        contacts = db.get_contacts(conn, severity, v_id)
        if not contacts.empty:
            #sms_gateways = []
            for idx, contact in contacts.iterrows():
                provider = format_provider_email_address(contact)
                #sms_gateways.append(provider)
            	#receivers = ';'.join(sms_gateways)
                send_alert(provider, subject, message)
        db.send_status(conn, message_id, timestamp)
    # now send the cleared messages
    if send_cleared_messages:
        cleared_messages = db.get_cleared_notsent(conn)
        for index, row in cleared_messages.iterrows():
            message_id = row['id']
            v_id = row['v_id']
            vehicle = vehicles.loc[vehicles['id'] == v_id]
            v_name = vehicle['name'].values[0]
            rule_id = row['rule_id']
            severity = row['severity']
            message = row['message']
            message += " cleared"
            subject = f"{v_name} {severity} rule {rule_id}  Message_id:{message_id} clear"
            contacts = db.get_contacts(conn, severity, v_id)
            if not contacts.empty:
                #sms_gateways = []
                for idx, contact in contacts.iterrows():
                    provider = format_provider_email_address(contact)
                    #sms_gateways.append(sms_gateways)
                    #receivers = ';'.join(sms_gateways)
                    send_alert(provider, subject, message)
            db.clear_sent(conn, message_id)


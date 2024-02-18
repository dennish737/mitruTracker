MITRU Database Documentation
============================

The MITRU Trailers and other support vehicles are used to supply on seen network
communications throughout Snohomish County Washington. These vehicles are
tracked and monitored, using multiple applications, for:

-   Location

-   Power and Temperature

-   Readiness

-   Connectivity

-   Etc.

The information gathered about the MITRU, and other communication support
vehicles, for current and post event analysis.

This document describes the database tables, the information contained and what
the data is used for.

The database consists of five classes of data, separated into tables:

1.  Basic Data

2.  Compound Data

3.  Rules Data – The rules data tables define the alert and alarm rules. This
    data defined ‘if’ or ‘when’ and alert or alarm will be generated, and who
    should be notified.

4.  Real Time Data – We are constantly monitoring trailer activity and equipment
    status. Whenever new data arrives, it is saved. When an event occurs, and a
    vehicle is deployed, we are able to track the status throughout the mission
    and recovery, and provide this data if required. Once this data is recovered
    and stored, these tables can be cleared and readied for the next event.

5.  Timers – Applications are run on a periodically, and are not always active.
    Thus, timers are persisted in the database. These timers are used to update
    status, and for rule triggers.

Database Schema Diagram
-----------------------

\<insert data schema diagram here\>

Basic Data Tables
-----------------

Data that are static in nature, and are ‘enter once’. Examples of Basic Data are
phone carries SMS information, APRS Channel information, Base Location
information, etc. Data in these tables are initially loaded at the time the
table is created, and new information is manually added or update as needed.

### Base Location Information

Each vehicle is assigned to a ‘base location’, which is the location the vehicle
is stored, or pre-deployed. Depending on the vehicle, there are requirements
that a storage or pre-deployment are required to meet, requiring a site survey
before equipment can be assigned. The ‘base_locations’ table contains the
approved sites for storage of vehicles. Each vehicle is assigned a base
location, and when away from their base location are considered deployed.

### Carrier SMS Information

>   Cell Phone services often provide a feature that allows someone to send an
>   email message to cell phone as a ‘Short Text Message’ (sms). Also, some
>   carriers allow user to send multimedia messages using ‘Multimedia Messaging
>   Service’ (mms). The carrier_sms table, provides a list of carriers that
>   provide sms and/or mms services, and the suffix to attach to the message to
>   line. The ‘carrier_sms’ table contains the sms contact suffix.

### Data Channels

The vehicles use APRS to provide location and SCADA data (temperature, voltage,
…). APRS allows up to five (5) SCADA channels to be reported. The data type and
value reported in any channel is configurable. The ‘channels’ table, maps the
APRS data channels, to the parameters monitored.

### Message Contact Information

Ome of the services provided by the, monitoring service which provides messages
when changes occur. Messages are broken down ‘Informational’, ‘Alerts’ and
‘Alarms’. To receive these messages, the user must provide their contact
information, and what messages they want to receive. The ‘contacts’ table
contains the user contact information and what messages they want to receive.

Compound Data Tables
--------------------

The compound data tables provide information about an object (e.g. and Mitru
Trailer, Alarm Contact, etc.) and provide links to basic information, and a
‘container’ for events and real time data

### Message Contact Information

One of the services provided by the, monitoring service which provides messages
when changes occur. Messages are broken down ‘Informational’, ‘Alerts’ and
‘Alarms’. To receive these messages, the user must provide their contact
information, and what messages they want to receive. The ‘contacts’ table
contains the user contact information and what messages they want to receive.

### Vehicles

Currently, vehicles are the primary object that we are monitoring. Vehicles have
sub systems, that are currently not managed, but may be managed in future
releases.

Vehicles, are managed in the ‘vehicles’ table.

### Real Time Data

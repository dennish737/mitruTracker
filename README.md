# TrailerAlert
MITRU Monitoring Application

Snohomish County Department of Emergency Management (SnoDEM) has developed 
the MITRU trailer, which can be deployed to support Disasters, Emergency 
Management and other Activities, providing power, communication and internet 
services anywhere in Snohomish County or neighboring counties in the 
State of Washington.

As part of the MITRU system, each unit has an onboard APRS tracking system, providing location, 
temperature and power status. Allowing anyone to view and track the status of MITRU Trailer using 
the APRS tracking web page (aprs.fi) and the MITRU trailer id.

TrailerAlert is a software package, running on a small Ubuntu/LINX client 
(e.g. NUC or Raspberry Pi) that:

1.	Periodically scans the aprs.fi page for MITRU Data and update the statusdata (TrailerDataCapture.py).
3.	Applies a set of rules to the updated data to determine if any alerts need to be set and cleared (Rules.py).
4.	Send new Alert and Alert Cleared messages (alert.py).
5.	Provide a set of web pages to manage and view MITRU Data (<server>/trailers).

Each of the major application are executed from crontab via a shell script. 
There is one shell script for each of the application

The php pages provide a dashboard allowing SnoDEM to monitor and track the MITRU Trailers.

# Instilation

1. Clone the repository
2. Copy content of php directory to /var/www/trailers
3. Copy content of html directory into /var/www/trailers
4. Copy lib and js directories to /var/www/trailers
5. Create DB mitru and install schema
6. 
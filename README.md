TrailerAlert
============

MITRU Monitoring Application

Snohomish County Department of Emergency Management (SnoDEM) has developed the
MITRU trailer, which can be deployed to support Disasters, Emergency Management
and other Activities, providing power, communication and internet services
anywhere in Snohomish County or neighboring counties in the State of Washington.

As part of the MITRU system, each unit has an onboard APRS tracking system,
providing location, temperature and power status. Allowing anyone to view and
track the status of MITRU Trailer using the APRS tracking web page (aprs.fi) and
the MITRU trailer id.

TrailerAlert is a software package, running on a small Ubuntu/LINX client (e.g.
NUC or Raspberry Pi) that:

1.  Periodically scans the aprs.fi page for MITRU Data and update the statusdata
    (TrailerDataCapture.py).

2.  Applies a set of rules to the updated data to determine if any alerts need
    to be set and cleared (Rules.py).

3.  Send new Alert and Alert Cleared messages (alert.py).

4.  Provide a set of web pages to manage and view MITRU Data (/trailers).

Each of the major application are executed from crontab via a shell script.
There is one shell script for each of the application

The php pages provide a dashboard allowing SnoDEM to monitor and track the MITRU
Trailers.

Instilation
===========

1.  Clone the repository

2.  Copy content of ‘trailers’ directory to /var/www/trailers

3.  Create DB mitru

4.  Restore DB

5.  Create config.php file in ‘trailers’ directory

    1. Add the following code , substituting ‘server’, ‘user’, ‘passwd’ and
        ‘db-name’ with your names
~~~
    <?php
        /* Database credentials for mysql (mariadb) */

        define('DB_SERVER', 'server');
        define('DB_USERNAME', 'user');
        define('DB_PASSWORD', 'password');
        define('DB_NAME', 'db-nsame');
    ?>
~~~

6. Create ‘.pyenv’ file in Clone Directory, replacing user, password, host, email_addr and email_password with your values


~~~
    DB_USERNAME="user"
    DB_PASSWD="password"
    DB_HOST="host"
    EMAIL_USERNAME="email_user_name"
    EMAIL_PASSWD="email_password"
~~~

7. Create python environment and load packages

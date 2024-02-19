import os

from datetime import datetime
import mariadb as database
import pandas as pd
import pandas.io.sql as psql

import utils as utils
# Database Tools

def dbconnect(host_name, username, password):
    connection = None
    try:
        connection = database.connect(
                user=username,
                password=password,
                host=host_name,
                port=3306,
                database="mitru"
        )
    except database.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    return connection

def read_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data is None:
            cursor.execute( query )
        else:
            cursor.execute(query, data)
        names = [ x[0] for x in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=names)
        return df
    finally:
        if cursor is not None:
            cursor.close()

def insert_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()

def get_vehicles(connection):
    vehicles = None
    try:
        query = "SELECT * FROM vehicles ORDER BY id ASC"
        vehicles = read_query(connection, query)
    except database.Error as e:
        print(f"Error retrieving vehicles from database: {e}")
    return vehicles

def get_last_location(connection, v_id):
    locations = None
    try:
        query = """SELECT * FROM locations a
                    INNER JOIN (SELECT MAX(l.last_reading)as max_reading, l.v_id  as lv_id FROM locations l 
                        WHERE l.v_id = %s GROUP BY v_id) as t
                    ON t.lv_id = a.v_id AND
                        t.max_reading = a.last_reading;"""
        data = (v_id,)
        locations = read_query(connection, query, data=data)
        locations.drop(['max_reading', 'lv_id'], axis=1, inplace=True)
    except database.Error as e:
        print(f"Error retrieving vehicle history from database: {e}")
    return locations

def get_last_readings(connection, v_id):
    locations = None
    try:
        query = """SELECT * FROM readings a
                    INNER JOIN
                    (SELECT MAX(l.last_reading)as max_reading, l.v_id FROM locations l 
                        WHERE l.v_id = %s GROUP BY v_id) as t
                    ON t.v_id = a.v_id AND
                        t.max_reading = a.last_reading;"""
        data = (v_id,)
        readings = read_query(connection, query, data)

    except database.Error as e:
        print(f"Error retrieving vehicle history from database: {e}")
    return readings

def get_location_changes(connection, v_id):
    changes = {}
    query = """SELECT * FROM locations 
                WHERE v_id = %s 
                ORDER BY last_reading DESC LIMIT 2"""
    data = (v_id,)
    locations = read_query(connection, query, data=data)
    if not locations.empty and len(locations.index) == 2:
        # build the change dictionary
        # reading time difference
        changes['v_id'] = v_id
        changes['reading_time'] = locations.iloc[0]['last_reading']
        changes['sys_t_delta'] = round(utils.sys_delta_t(locations.iloc[0]['last_reading'])/60.0, 3)
        changes['poling_time'] = round(utils.delta_t(locations.iloc[1]['last_reading'], locations.iloc[0]['last_reading'])/60.0, 3)
        loc1 = (locations.iloc[1]['latitude'], locations.iloc[1]['longitude'])
        loc2 = (locations.iloc[0]['latitude'], locations.iloc[0]['longitude'])
        d_move = utils.distance(loc1, loc2)
        changes['distance_moved'] = d_move if d_move > 50.0 else 0.0
        d_alt = locations.iloc[0]['altitude_m'] - locations.iloc[1]['altitude_m']
        changes['alt_change'] = d_alt if d_alt > 15.0 else 0.0
        changes['speed'] = (d_move/changes['poling_time'] ) if changes['poling_time'] != 0 else 0;

    return changes

def insert_motion( connection, changes):
    """

    :param connection: database connection
    :param changes: dictionary of changes
    :return:
    """
    query = """INSERT INTO motion(v_id, last_reading, dt, dlen, speed, dalt) 
                VALUES ({0}, '{1}', {2}, '{3}', '{4}', '{5}');""".format(
                    changes['v_id'],
                    changes['reading_time'],
                    changes['poling_time'] ,
                    changes['distance_moved'],
                    changes['speed'],
                    changes['alt_change'])
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()


def update_locations(connection, row):
    """ update the location information in the database.
        This is done by inserting a row in the location table.
        Before inserting the row, we want to check that the location
        'last _reading' value has changed has changed. We  will
        do that by getting the last location reading and comparing the last_reading
        value"""

    #delta_t2 = pd.Timedelta(timestamp - row['last_reading']).seconds / 60.0  # difference in reading time and system time

    row['last_reading'] = row['last_reading'].tz_convert(None)
    last_location = get_last_location(connection, row['v_id'])
    dt = 10
    # if we have a previous location get the delta time value
    if not last_location.empty:
        dt = utils.delta_t( last_location.iloc[-1]['last_reading'] , row['last_reading']) / 60.0 # time difference in minutes reading time
        lc = utils.delta_t( last_location.iloc[-1]['last_reading'] , datetime.utcnow()) / 60.0 # time difference in minutes current time
    columns = ','.join("`" + str(x).replace('/','_') + "`" for x in row.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for k, x in row.items())
    loc_items = [row['longitude'], row['latitude'] ]

    if dt > 5:
        columns = ','.join("`" + str(x).replace('/','_') + "`" for x in row.keys())
        # add location
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for k, x in row.items())
        loc = "PointFromText(\'POINT(" + ' '.join(str(x) for x in loc_items) + ")\', 4326)"
        # insert location
        sql = "INSERT INTO %s ( %s, `loc`) VALUES ( %s , %s);" % ('locations', columns, values, loc)
        insert_query(connection, sql)
        update_contact(connection, row['v_id'], 0)
        changes = get_location_changes(connection, row['v_id'])
        move_status = 0
        if changes['speed'] > 1:
            move_status = 1
        update_move_status(connection, row['v_id'], move_status )

    else:
        print("duplicate location reading: skipping")
        update_contact(connection, row['v_id'], lc)

def update_readings(connection, readings):
    """"""
    last_readings = get_last_readings(connection, readings.iloc[0]['v_id'])
    for index, row in readings.iterrows():
        row['last_reading'] = row['last_reading'].tz_convert(None)
        delta_t = 10
        if  not last_readings.empty:
            delta_t = pd.Timedelta(row['last_reading'] - last_readings.iloc[-1]['last_reading'] ).seconds  # difference in reading time and system time
            #print("delta_t = ", delta_t)

        if delta_t > 5:
            columns = ','.join("`" + str(x).replace('/', '_') + "`" for x in row.keys())
            values = ', '.join("'" + str(x).replace('/', '_') + "'" for k, x in row.items())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('readings', columns, values)
            insert_query(connection, sql)
        #else:
        #    print("duplicate data reading: skipping")

def update_contact(connection, v_id, dt):
    # time is the time in minutes since last contact
    # note we overwrite time values
    sql = "UPDATE last_contact SET lt_minutes = {0} WHERE v_id = {1};".format(int(dt),v_id)
    cursor = connection.cursor()
    try:
        cursor.execute( sql )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()

def update_move_status(connection, v_id, moving):
    # time is the time in minutes since last contact
    # note we overwrite time values

    sql = "UPDATE move_status SET `moving`={0} WHERE v_id={1};".format(int(moving), v_id)
    print(sql)
    cursor = connection.cursor()
    try:
        cursor.execute( sql )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
def update_changes(connection, row):
    """

    :param connection: db connection
    :param changes: dictionary of changes
    :return:
    """
    #print(changes)

def get_rules(connection, v_id= None, severity='INFO' ):
    try:
        rules = None
        data = (severity,)
        query = """SELECT a.id, a.v_id, a.rule_name, a.rule_class, a.rule_function, a.limit_value, a.severity, b.message
                    FROM rules a
                    INNER JOIN messages b
                    ON a.message = b.id
                    WHERE severity = %s AND ENABLED = TRUE 
                    ORDER BY a.id;"""
        if v_id is not None:
            query = """SELECT a.id, a.v_id, a.rule_name, a.rule_class, a.rule_function, a.limit_value, a.severity, b.message
                        FROM rules a
                        INNER JOIN messages b
                        ON a.message = b.id
                        WHERE a.v_id = %s AND severity = %s AND ENABLED = TRUE
                        ORDER BY a.id;"""

            data = (v_id, severity)

        rules = read_query(connection, query, data)
    except database.Error as e:
        print(f"Error retrieving vehicle history from database: {e}")
    return rules

def get_last_contact(connection,v_id=None):
    rtn = 0
    try:
        data = None
        query = "SELECT * FROM last_contact ORDER BY v_id;"
        if v_id is not None:
            query = "SELECT * FROM last_contact WHERE v_id = %s;"
            data = (v_id,)
        lc = read_query(connection, query, data)
        rtn = lc['lt_minutes']
    except database.Error as e:
        print(f"Error retrieving vehicle history from database: {e}")
    return rtn

def get_alerts(connection, v_id):
    alerts = None
    try:
        data = (v_id,)
        query = "SELECT * FROM status_queue WHERE v_id = %s AND severity = 'ALERT' " \
                "AND cleared = FALSE;"
        alerts = read_query(connection, query, data)
    except database.Error as e:
        print(f"Error retrieving vehicle history from database: {e}")
    return alerts

def get_alarms(connection, v_id):
    alarms = None
    try:
        data = (v_id,)
        query = "SELECT * FROM status_queue WHERE v_id = %s AND severity = 'ALARM' " \
                "AND cleared = FALSE;"
        alarms = read_query(connection, query, data)
    except database.Error as e:
        print(f"Error retrieving vehicle history from database: {e}")
    return alarms

def insert_status(connection, rule_id, timestamp, v_id, severity, message):
    ts = timestamp.tz_convert(None)
    query = """INSERT INTO status_queue(rule_id, post_time, v_id, severity, message) 
                VALUES ({0}, '{1}', {2}, '{3}', '{4}');""".format(rule_id, ts, v_id, severity, message)
    #print(query)
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()

def update_status(connection, status_id):
    query = "UPDATE status_queue SET count = count + 1 WHERE id = {0};".format(status_id)
    print(query)
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()

def send_status(connection, status_id, timestamp):
    ts = timestamp.tz_convert(None)
    query = "UPDATE status_queue SET count = 0, sent = TRUE, sent_time = '{0}' WHERE id = {1};".format(ts, status_id)
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()

def clear_sent(connection, status_id):

    query = "UPDATE status_queue SET cleared_sent=1 WHERE id = {0};".format(status_id)
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()

def clear_status(connection, status_id, timestamp):
    ts = timestamp.tz_convert(None)
    query = "UPDATE status_queue SET count = 0, cleared = TRUE, clear_time = '{0}' WHERE id = {1};".format(ts, status_id)
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()


def get_new_messages(connection):
    query = "SELECT * FROM status_queue WHERE cleared=0 AND sent = 0 ORDER BY id;"
    data = None
    new_messages = read_query(connection, query, data)
    return new_messages

def get_cleared_notsent(connection):
    query = "SELECT * FROM status_queue WHERE cleared=1 AND cleared_sent = 0 ORDER BY id;"
    data = None
    cleared_messages = read_query(connection, query, data)
    return cleared_messages

def get_carriers(connection):
    query = "SELECT * FROM carrier_sms ORDER BY id;"
    data = None
    carriers = read_query(connection, query, data)
    return carriers

def get_contacts(connection, severity, v_id):
    # set the level
    level = 3
    if severity == 'ALARM':
        level = 1
    elif severity == 'ALERT':
        level = 2
    else:
        level = 0

    # set the vehicles
    match v_id:
        case 1:
            v_set = '(1,3,5,7)'
        case 2:
            v_set = '(2,3,6,7)'
        case 3:
            v_set = '(4,5,6,7)'
        case _:
            v_set = '(0)'

    query = """SELECT a.name, a.phone, b.sms FROM contacts a
                INNER JOIN carrier_sms b
                ON a.carrier_id = b.id
                WHERE level >= {0} AND vehicles in {1} 
                ORDER BY a.id; """.format(level, v_set)
    data = None
    contacts = read_query(connection, query, data)
    return contacts

def get_moving_status(connection, v_id):
    data = None
    query = """WITH move AS (
            SELECT v_id, speed,
                COALESCE(LAG(speed, 1)
                    OVER (PARTITION BY v_id ORDER BY id DESC), 0)AS speed1,
                COALESCE(LAG(speed, 2)
                    OVER (PARTITION BY v_id ORDER BY id DESC),0)AS speed2
            FROM motion
            ), is_moving AS (
            SELECT v_id, 
                CASE 
                    WHEN speed = 0 and speed1 = 0 and speed2 = 0 THEN 0
                    -- WHEN speed > 0 or speed1 > 0 or speed2 > 0 THEN 1
                    WHEN speed > 0  THEN 1
                    -- ELSE 0
                END as moving
            FROM move
            )
            SELECT moving FROM is_moving 
            WHERE  v_id = {1}
            LIMIT 1;
        """.format(v_id)

    moving_status = read_query(connection, query, data)
    return moving_status
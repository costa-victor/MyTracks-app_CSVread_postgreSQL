# -*- coding: utf-8 -*-

import csv
import psycopg2
import math


def querySyntaxExample1():
    try:
        connection = psycopg2.connect(user="your_user",
                                      password="your_password",
                                      host="your_ip_address",
                                      port="your_postgreSQL_port",
                                      database="your_database_name")
        cursor = connection.cursor()
        query = 'select * from your_table'
        cursor.execute(query)

        # Fetching all data from cursor
        my_query_data = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return my_query_data


def querySyntaxExample2():
    try:
        connection = psycopg2.connect(user="your_user",
                                      password="your_password",
                                      host="your_ip_address",
                                      port="your_postgreSQL_port",
                                      database="your_database_name")
        cursor = connection.cursor()
        query = 'select max(something) from your_table'
        cursor.execute(query)

        # Fetching one data from cursor, which returns only one value
        my_query_data = cursor.fetchone()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return my_query_data



def insertSyntaxExample1(param1, param2, param3):
    try:
        connection = psycopg2.connect(user="your_user",
                                      password="your_password",
                                      host="your_ip_address",
                                      port="your_postgreSQL_port",
                                      database="your_database_name")
        cursor = connection.cursor()

        insert1 = """ insert into your_table(p1, p2, p3) values(%s, %s, %s) """
        data_inserted1 = (param1, param2, param3)

        # This will insert data using a parameter list
        cursor.execute(insert1, data_inserted1)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert data on your_table", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return None



def insertSyntaxExample2(toInsert):
    try:
        connection = psycopg2.connect(user="your_user",
                                      password="your_password",
                                      host="your_ip_address",
                                      port="your_postgreSQL_port",
                                      database="your_database_name")
        cursor = connection.cursor()

        # Restart your serial ID back to 1
        query = 'ALTER SEQUENCE public.your_table_seq RESTART WITH 1'
        cursor.execute(query)
        connection.commit()

        insert3 = """ insert into your_table(p1, p2, p3,  p4) values(%s, %s, %s, %s)"""

        # This will insert row by row on list toInsert, which must have 4 values like your_table(p1, p2, p3,  p4)
        cursor.executemany(insert3, toInsert)
        connection.commit()
        print(cursor.rowcount, "data has been successfully inserted into your_table table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert data on bus_stop table", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return None



# Calculate the distance between two coordinates (Usefull for small distances, does't considerate the globe curvature)
def dist(x_ref, y_ref, x, y):
    return 1e5*(math.sqrt(pow((x - x_ref), 2) + pow((y - y_ref), 2)))


# Open a CSV File and read their values
csv_file = open('car_test.csv', 'r')
csv_reader = csv.reader(csv_file, delimiter=',')
markerFile = []
locationFile = []
critParada = 0

for row in csv_reader:
    if(not row):
        critParada = critParada+1
    # Save all marker points
    elif(critParada == 1):
        # Ignoring the header from CSV File
        if(row[0] == 'Marker'):
            print('')
        else:
            markerFile.append(
                [int(float(row[0])), float(row[2]), float(row[3])])
    # Save all location points
    elif(critParada == 2):
        # Ignoring the header from CSV File
        if(row[0] == 'Location'):
            print('')
        else:
            locationFile.append(
                [int(float(row[0])), float(row[2]), float(row[3]), float(row[4])])


csv_file.close()

# Convert List to Dictionary  ~ Easier to work, depending on your application
markerDB = []
markerCSV = []
locationCSV = []

for row in markerFile:
    markerCSV.append({'id': row[0], 'lat': row[1], 'lon': row[2]})

for row in locationFile:
    locationCSV.append(
        [row[1], row[2], row[3]])

temp = querySyntaxExample1()
for row in temp:
    markerDB.append({'idGlobal': row[0], 'lat': row[1], 'lon': row[2]})





# This function applies a filter on markers location. When one marker is close enough to a marker in the database, based on a "radius" parameter, it will not be added on database.
def filterMarkers(radius):
    for db in markerDB:
        for csv in markerCSV:
            distance = dist(db['lat'], db['lon'], csv['lat'], csv['lon'])
            if(distance <= radius):
                print(db['idGlobal'], '---', csv['id'],
                      '--- Distance: ', distance)
                csv['id'] = db['idGlobal']
                csv['lat'] = db['lat']
                csv['lon'] = db['lon']

    return None


#### Example - Insert on busStop table

# Filter called
filterMarkers(50.0)

# List to be inserted - Converting dict to list
busStopToInsert = []

for row in markerCSV:
    busStopToInsert.append(
        [row['id'], row['lat'], row['lon'], 0])

insertSyntaxExample2(busStopToInsert)





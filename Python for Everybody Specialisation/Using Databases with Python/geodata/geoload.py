import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

#Create SQLite table
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("where.data")
count = 0
for line in fh:
    if count > 200 :
        print('Retrieved 200 locations, restart to retrieve more')
        break

    address = line.strip()
    # print(address) #added to visualise data
    print('')   #added as an empty line separator
    # https://www.geeksforgeeks.org/memoryview-in-python/#:~:text=memoryview%20objects%20allow%20Python%20code,needing%20to%20copy%20it%20first.
    # memoryview objects allow Python code to access the internal data of an object that supports the buffer protocol without copying. The memoryview() function allows direct read and write access to an object's byte-oriented data without needing to copy it first.

    # ***still not sure why we need to 'encode' when querying the SQLite DB***
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))

    #if 'address' is already found in the SQLite DB, move to the next 'address' in the 'where.data' file
    #without incrementing counter
    try:
        data = cur.fetchone()[0]
        print("Found in database ",address)
        continue
    #otherwise, 'pass' and move on to the code segments below
    #In Python, pass is a null statement. The interpreter does not ignore a pass statement, but nothing happens and the statement results into no operation.
    #https://www.educative.io/edpresso/what-is-pass-statement-in-python
    except:
        pass



    parms = dict()
    parms["address"] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)
    # print(parms) #added to visualise data

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    # print(data) #added to visualise data
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1
    # print('Count :', count) #added to visualise process

    try:
        js = json.loads(data)
        # print(js) #added to visualise data
    except:
        print(data)  # We print in case unicode causes an error
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break

    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
    conn.commit()
    if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")


'''
#After addding 'Hanken' to row 299 of 'where.data'
#output from running 'geoload.py' during the 1st iteration is as follows

Retrieving http://py4e-data.dr-chuck.net/json?address=Universitas+Gadjah+Mada&key=42
Retrieved 2319 characters {    "results" : [
Retrieved 200 locations, restart to retrieve more
Run geodump.py to read the data from the database so you can vizualize it on a map.
'''




'''
#sample output from running 'geoload.py' during the 2nd iteration is as follows

#print("Found in database ",address)
Found in database  AGH University of Science and Technology
...


# print(address)
Hanken

# print(parms)
{'address': 'Hanken', 'key': 42}
# print('Retrieving', url)
Retrieving http://py4e-data.dr-chuck.net/json?address=Hanken&key=42
# print(data)
{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "22",
               "short_name" : "22",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "Arkadiankatu",
               "short_name" : "Arkadiankatu",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Helsinki",
               "short_name" : "Helsinki",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Finland",
               "short_name" : "FI",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "00100",
               "short_name" : "00100",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "Arkadiankatu 22, 00100 Helsinki, Finland",
         "geometry" : {
            "location" : {
               "lat" : 60.1707416,
               "lng" : 24.9244352
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 60.17209058029151,
                  "lng" : 24.9257841802915
               },
               "southwest" : {
                  "lat" : 60.1693926197085,
                  "lng" : 24.9230862197085
               }
            }
         },
         "place_id" : "ChIJ83-U5DMKkkYR5wT2816WJNc",
         "plus_code" : {
            "compound_code" : "5WCF+7Q Helsinki, Finland",
            "global_code" : "9GG65WCF+7Q"
         },
         "types" : [ "establishment", "point_of_interest", "university" ]
      }
   ],
   "status" : "OK"
}

# print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
Retrieved 1721 characters {    "results" : [
# print('Count :', count)
Count : 98
# print(js)
{'results': [{'address_components': [{'long_name': '22', 'short_name': '22', 'types': ['street_number']}, {'long_name': 'Arkadiankatu', 'short_name': 'Arkadiankatu', 'types': ['route']}, {'long_name': 'Helsinki', 'short_name': 'Helsinki', 'types': ['locality', 'political']}, {'long_name': 'Finland', 'short_name': 'FI', 'types': ['country', 'political']}, {'long_name': '00100', 'short_name': '00100', 'types': ['postal_code']}], 'formatted_address': 'Arkadiankatu 22, 00100 Helsinki, Finland', 'geometry': {'location': {'lat': 60.1707416, 'lng': 24.9244352}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 60.17209058029151, 'lng': 24.9257841802915}, 'southwest': {'lat': 60.1693926197085, 'lng': 24.9230862197085}}}, 'place_id': 'ChIJ83-U5DMKkkYR5wT2816WJNc', 'plus_code': {'compound_code': '5WCF+7Q Helsinki, Finland', 'global_code': '9GG65WCF+7Q'}, 'types': ['establishment', 'point_of_interest', 'university']}], 'status': 'OK'}
#print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
Run geodump.py to read the data from the database so you can vizualize it on a map.
'''

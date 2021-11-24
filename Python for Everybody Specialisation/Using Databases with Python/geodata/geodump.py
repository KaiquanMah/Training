import sqlite3
import json
import codecs

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('where.js', 'w', "utf-8")

#rewrite the whole 'where.js' file
#'myData = [' would be in the 1st row
fhand.write("myData = [\n")
count = 0

#from the SQLite DB
for row in cur :
    data = str(row[1].decode())
    # print(data) #visualise data
    # print(row) #visualise data

    #load the json data into a dictionary
    try: js = json.loads(str(data))
    except: continue


    if not('status' in js and js['status'] == 'OK') : continue

    #analyse the longitude, latitude values
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue

    #address > remove single quote "'" if found
    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")

    try :
        print(where, lat, lng)

        count = count + 1
        #newline for the second or subsequent record
        if count > 1 : fhand.write(",\n")

        #construct the row to write to the 'where.js' file
        output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
        fhand.write(output)
    except:
        continue

#newline, then '];' on the same line
#then another newline
fhand.write("\n];\n")
# close connections to the SQLite DB cursor and 'where.js' file handle
cur.close()
fhand.close()

print(count, "records written to where.js")
print("Open where.html to view the data in a browser")




'''
print(data)
{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "30",
               "short_name" : "30",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "aleja Adama Mickiewicza",
               "short_name" : "aleja Adama Mickiewicza",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Krowodrza",
               "short_name" : "Krowodrza",
               "types" : [ "political", "sublocality", "sublocality_level_1" ]
            },
            {
               "long_name" : "Kraków",
               "short_name" : "Kraków",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Kraków",
               "short_name" : "Kraków",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Małopolskie",
               "short_name" : "Małopolskie",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Poland",
               "short_name" : "PL",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "30-059",
               "short_name" : "30-059",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "aleja Adama Mickiewicza 30, 30-059 Kraków, Poland",
         "geometry" : {
            "location" : {
               "lat" : 50.06688579999999,
               "lng" : 19.9136192
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 50.0682347802915,
                  "lng" : 19.9149681802915
               },
               "southwest" : {
                  "lat" : 50.0655368197085,
                  "lng" : 19.9122702197085
               }
            }
         },
         "place_id" : "ChIJIZu1VqdbFkcR0RezIbqNDLI",
         "plus_code" : {
            "compound_code" : "3W87+QC Kraków, Poland",
            "global_code" : "9F2X3W87+QC"
         },
         "types" : [ "establishment", "point_of_interest", "university" ]
      }
   ],
   "status" : "OK"
}





print(row)
(b'AGH University of Science and Technology', b'{\n   "results" : [\n      {\n         "address_components" : [\n            {\n               "long_name" : "30",\n               "short_name" : "30",\n               "types" : [ "street_number" ]\n            },\n            {\n               "long_name" : "aleja Adama Mickiewicza",\n               "short_name" : "aleja Adama Mickiewicza",\n               "types" : [ "route" ]\n            },\n            {\n               "long_name" : "Krowodrza",\n               "short_name" : "Krowodrza",\n               "types" : [ "political", "sublocality", "sublocality_level_1" ]\n            },\n            {\n               "long_name" : "Krak\xc3\xb3w",\n               "short_name" : "Krak\xc3\xb3w",\n               "types" : [ "locality", "political" ]\n            },\n            {\n               "long_name" : "Krak\xc3\xb3w",\n               "short_name" : "Krak\xc3\xb3w",\n               "types" : [ "administrative_area_level_2", "political" ]\n            },\n            {\n               "long_name" : "Ma\xc5\x82opolskie",\n               "short_name" : "Ma\xc5\x82opolskie",\n               "types" : [ "administrative_area_level_1", "political" ]\n            },\n            {\n               "long_name" : "Poland",\n               "short_name" : "PL",\n               "types" : [ "country", "political" ]\n            },\n            {\n               "long_name" : "30-059",\n               "short_name" : "30-059",\n               "types" : [ "postal_code" ]\n            }\n         ],\n         "formatted_address" : "aleja Adama Mickiewicza 30, 30-059 Krak\xc3\xb3w, Poland",\n         "geometry" : {\n            "location" : {\n               "lat" : 50.06688579999999,\n               "lng" : 19.9136192\n            },\n            "location_type" : "ROOFTOP",\n            "viewport" : {\n               "northeast" : {\n                  "lat" : 50.0682347802915,\n                  "lng" : 19.9149681802915\n               },\n               "southwest" : {\n                  "lat" : 50.0655368197085,\n                  "lng" : 19.9122702197085\n               }\n            }\n         },\n         "place_id" : "ChIJIZu1VqdbFkcR0RezIbqNDLI",\n         "plus_code" : {\n            "compound_code" : "3W87+QC Krak\xc3\xb3w, Poland",\n            "global_code" : "9F2X3W87+QC"\n         },\n         "types" : [ "establishment", "point_of_interest", "university" ]\n      }\n   ],\n   "status" : "OK"\n}\n')

#so row[1] extracts only the JSON data into the 'data' variable




print(type(json.loads(str(data))))
<class 'dict'>
'''

import csv
import json

filtered = []

with open('large_airports.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        filtered.append(row)

jsonObject = {}
for row in filtered:
    jsonObject[row[7]] = {
        'ident': row[0],
        'lat': row[1],
        'lon': row[2],
        'elevation_ft': row[3],
        'continent': row[4],
        'iso_country': row[5],
        'iso_region': row[6]
    }

with open('locations.json', 'wb') as outfile:
    json.dump(jsonObject, outfile, indent=4)

with open('large_airports.csv', 'wb') as airportcsv:
    spamwriter = csv.writer(airportcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in filtered:
        spamwriter.writerow(row)

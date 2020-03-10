import csv
from urllib import request
import geopy
from geopy.distance import distance
from geopy.geocoders import Nominatim

ZIP_CODE = input("Enter your ZIP CODE: ")

# Download and parse the CSV file
file_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
data = [d.decode('utf-8') for d in request.urlopen(file_url).readlines()]

# Add blank space for missing cities to prevent dropping columns
for n, row in enumerate(data):
    data[n] = "Unknown" + row if row[0] == "," else row

# Split each row into a list of data
data_split = [row[0:4] + row[-1:] for row in csv.reader(data)]

# Find date of last update
last_updated = data_split[0][-1]
cities = data_split[1:]

# Setup the geolocator
geopy.geocoders.options.default_user_agent = 'my_app/1'
geopy.geocoders.options.default_timeout = 7
geolocator = Nominatim()

# Find location based on my zip code
location = geolocator.geocode({"postalcode": ZIP_CODE, 'country': 'United States'})
my_loc = (location.latitude, location.longitude)

# Calculate the distance between my location and the other locations in the dataset
def distance_in_miles(my_loc, city_loc):
    miles = distance(my_loc, city_loc).miles
    return miles

# Add the calculated distance for each location in `cities`
distances = []
for n, row in enumerate(cities):
    city_loc = tuple(row[2:4])
    distances.append((distance_in_miles(my_loc, city_loc), n))

# Top closest locations
dist_ranked = sorted(distances)
top = dist_ranked[:10]

top_dict = {}
for n, row in enumerate(top):
    miles, index = row
    top_dict[n] = cities[index] + [miles]

print(f"\nTOP 10 NEAREST LOCATIONS FROM MY ZIPCODE -- updated {last_updated}\n")
print("RANK".ljust(5), "MILES".ljust(15), "CASES".ljust(8), "COUNTY STATE")
for k, v in top_dict.items():
    print(f"{k+1}".ljust(5), f"({v[5]:,.1f} miles)".ljust(15), f"{v[4]}".ljust(8), f"{v[0]}")

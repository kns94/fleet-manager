from flask import Flask, render_template
from math import radians, cos, sin, asin, sqrt
import requests
import pandas as pd
import threading
import atexit

POOL_TIME = 5  # Seconds
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
polling_thread = threading.Thread()

# header to call samsara API
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer TOKEN"
}
# params to call samsara API
params = {"types": "gps"}

# creating a pandas dataframe to track vehicles
column_names = ["id", "name", "timestamp", "latitude", "longitude"]
df = pd.DataFrame(columns=column_names)
# cache used for faster dataframe updation
vehicle_cache = {}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


def interrupt():
    global polling_thread
    polling_thread.cancel()


def save_locations():
    """
        Polls updated locations from Samsara and saves locations in a CSV file
    """

    global polling_thread
    global df

    url = "https://api.samsara.com/fleet/vehicles/stats/feed"

    response = requests.request("GET", url, headers=headers, params=params).json()
    for vehicle in response["data"]:
        for gps_ping in vehicle['gps']:
            if vehicle['id'] not in vehicle_cache:
                idx = len(df.index)
                vehicle_cache[vehicle['id']] = len(df.index)
            else:
                idx = vehicle_cache[vehicle['id']]

            df.loc[idx] = [
                vehicle['id'],
                vehicle['name'],
                gps_ping['time'],
                gps_ping['latitude'],
                gps_ping['longitude'],
            ]

            invite_home = df.apply(lambda row: haversine_from_home(row['longitude'], row['latitude']) < 200, axis=1)
            invite_home = df[invite_home]

            if len(invite_home.index) != 0:
                invite_home.to_csv("static/invite_home.csv", sep=',')

            df.to_json("static/data.json", orient="records", indent=4)

        params['after'] = response['pagination']['endCursor']

    # Set the next thread to happen
    polling_thread = threading.Timer(POOL_TIME, save_locations, ())
    polling_thread.start()


def poll_fleets():
    global polling_thread
    polling_thread = threading.Timer(POOL_TIME, save_locations, ())
    polling_thread.start()


def haversine_from_home(lat, lon):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """

    lat_home = 38.00089003740244
    lon_home = -121.287269144516

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon_home, lat_home, lon, lat])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return c * r


if __name__ == "__main__":
    poll_fleets()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    app.run()

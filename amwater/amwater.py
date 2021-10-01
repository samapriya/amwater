
__copyright__ = """
    Copyright 2021 Samapriya Roy
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__license__ = "Apache 2.0"


import requests
import argparse
import time
import sys
import os
import platform
import subprocess
from os.path import expanduser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
if str(platform.system().lower()) == "windows":
    # Get python runtime version
    version = sys.version_info[0]
    try:
        import pipwin

        if pipwin.__version__ == "0.5.0":
            pass
        else:
            a = subprocess.call(
                "{} -m pip install pipwin==0.5.0".format(sys.executable),
                shell=True,
                stdout=subprocess.PIPE,
            )
            b = subprocess.call(
                "{} -m pip install wheel".format(sys.executable),
                shell=True,
                stdout=subprocess.PIPE,
            )
            subprocess.call("pipwin refresh", shell=True)
        """Check if the pipwin cache is old: useful if you are upgrading porder on windows
        [This section looks if the pipwin cache is older than two weeks]
        """
        home_dir = expanduser("~")
        fullpath = os.path.join(home_dir, ".pipwin")
        file_mod_time = os.stat(fullpath).st_mtime
        if int((time.time() - file_mod_time) / 60) > 180000:
            print("Refreshing your pipwin cache")
            subprocess.call("pipwin refresh", shell=True)
    except ImportError:
        a = subprocess.call(
            "{} -m pip install pipwin==0.5.0".format(sys.executable),
            shell=True,
            stdout=subprocess.PIPE,
        )
        subprocess.call("pipwin refresh", shell=True)
    except Exception as e:
        print(e)
    try:
        import shapely
    except ImportError:
        subprocess.call("pipwin install shapely", shell=True)
    except Exception as e:
        print(e)

from shapely.geometry import box
import shapely.wkt

# Checks for last 10 alerts
MAIN_URL = "https://alertsdetail.awapps.com/launch?orgId=4007&launchCount=10"

# Parse Geometry from alert url
def geometry_parse(alert_url):
    alert_detail = requests.get(alert_url)
    soup = BeautifulSoup(alert_detail.text, "xml")
    alert_geom = soup.find_all("script", type="text/javascript")
    for geoms in alert_geom:
        try:
            # start = datetime.strptime(start, "%Y-%m-%d")
            aoi_geometry = (
                geoms.text.split("var areaLocations = ")[1]
                .split(";")[0]
                .split('"')[1]
                .split('"')[0]
            )
        except Exception as e:
            pass
    if not "POLYGON" in aoi_geometry:
        aoi_geometry = "POLYGON" + (aoi_geometry)
    return aoi_geometry


# Water Alert from Ameren
def water_alert(n, place):
    alert_list = requests.get(MAIN_URL)
    soup = BeautifulSoup(alert_list.text, "xml")
    alert_time = soup.find_all("AlertTime")
    expiration_time = soup.find_all("ExpirationTime")
    alert_link = soup.find_all("LaunchDetailLink")
    alert_id = soup.find_all("LaunchId")
    alert_type = soup.find_all("LaunchType")
    alert_message = soup.find_all("Message")
    alert_count = []
    alert_miss = []
    if place is not None:
        if (",") in place:
            place.split(",")
            place = "".join(place)
        else:
            place = place
        r = requests.get(
            "https://nominatim.openstreetmap.org/search?q=" + place + "&format=jsonv2"
        )
        response = r.json()
        for things in response:
            try:
                if len(response) >= 1:
                    minmax = things.get("boundingbox")
                    tuple_minmax = tuple([float(s) for s in minmax])
                    boundary_poly = box(
                        tuple_minmax[2],
                        tuple_minmax[0],
                        tuple_minmax[3],
                        tuple_minmax[1],
                    )
                    boundary_poly = boundary_poly.buffer(0.0005).simplify(
                        4
                    )  # Adding buffer and simplifying
                else:
                    print("Found no matching address {}".format(len(response)))
            except Exception as e:
                print(e)

    print(
        f"Now processing for {place} from {str(datetime.now() - timedelta(n)).split(' ')[0]} onwards"
        + "\n"
    )

    for i in range(0, len(alert_time)):
        dt = datetime.now() - timedelta(n)
        dt = datetime.strptime(str(dt).split(" ")[0], "%Y-%m-%d")
        start = alert_time[i].get_text().split("T")[0]
        start_time = datetime.strptime(start, "%Y-%m-%d")
        try:
            alert_geom = shapely.wkt.loads(geometry_parse(alert_link[i].get_text()))
            if start_time >= dt and alert_geom.intersects(boundary_poly):
                print("Start Time: {}".format(str(start_time).split(" ")[0]))
                print(
                    "Expiration Time: {}".format(
                        expiration_time[i].get_text().split("T")[0]
                    )
                )
                print("Alert ID: {}".format(alert_id[i].get_text()))
                print("Alert Type: {}".format(alert_type[i].get_text()))
                print("Alert Link: {}".format(alert_link[i].get_text()))
                print("Alert Message: {}".format(alert_message[i].get_text()).strip())
                alert_count.append(str(start_time).split(" ")[0])
                print("")
            else:
                alert_miss.append(str(start_time).split(" ")[0])
        except Exception as e:
            print(e)
    print("\n" + "Total alerts for {} : {}".format(place, len(alert_count)))
    print("Total alerts unrelated to {} : {}".format(place, len(alert_miss)))


def check_from_parser(args):
    water_alert(n=args.days, place=args.address)


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Alert CLI for American water: water alert"
    )
    subparsers = parser.add_subparsers()

    parser_check = subparsers.add_parser(
        "amcheck", help="Check for any american water issued alerts for given adddress"
    )
    required_named = parser_check.add_argument_group("Required named arguments.")
    required_named.add_argument("--address", help="Your address", required=True)
    optional_named = parser_check.add_argument_group("Optional named arguments")
    optional_named.add_argument(
        "--days", help="Number of days to check for alert default is 1 day", default=1
    )
    parser_check.set_defaults(func=check_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()

# amwater: Simple CLI for SofarOcean API

![](https://tokei.rs/b1/github/samapriya/amwater?category=code)
![](https://tokei.rs/b1/github/samapriya/amwater?category=files)
[![CI amwater](https://github.com/samapriya/amwater/actions/workflows/package_ci.yml/badge.svg)](https://github.com/samapriya/amwater/actions/workflows/package_ci.yml)
![PyPI - License](https://img.shields.io/pypi/l/amwater)
![PyPI - Downloads](https://img.shields.io/pypi/dm/amwater)
![PyPI](https://img.shields.io/pypi/v/amwater)


## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [amwater Simple CLI for Sofarocean API](#amwater-simple-cli-for-sofarocean-api)
    * [amwater auth](#amwater-auth)
    * [amwater reset](#amwater-reset)
    * [amwater devlist](#amwater-devlist)
    * [amwater spotcheck](#amwater-spotcheck)
    * [amwater spotdata](#amwater-spotdata)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

**amwater only support Python v3.4 or higher**

To install **amwater: Simple CLI for SofarOcean API** you can install using two methods.

```pip install amwater```

or you can also try

```
git clone https://github.com/samapriya/amwater.git
cd amwater
python setup.py install
```
For Linux use sudo or try ```pip install amwater --user```.

I recommend installation within a virtual environment. Find more information on [creating virtual environments here](https://docs.python.org/3/library/venv.html).

## Getting started

As usual, to print help:

```
amwater -h
usage: amwater [-h] {auth,reset,devlist,spot-check,spot-data} ...

Simple CLI for Sofarocean API

positional arguments:
  {auth,reset,devlist,spot-check,spot-data}
    auth                Authenticates and saves your API token
    reset               Regenerates your API token
    devlist             Print lists of devices available under your account
    spot-check          Spot check a Spotter location and time
    spot-data           Export Spotter Data based on Spotter ID & grouped by date

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for specific functionality, simply call it with _help_ switch, e.g.: `amwater spot-check -h`. If you didn't install amwater, then you can run it just by going to *amwater* directory and running `python amwater.py [arguments go here]`

## amwater Simple CLI for Sofarocean API
The tool is designed to interact with the SofarOcean API, for now this is focused only on the spotter endpoints.

### amwater auth
This allows you to save your authentication token, this is then used for authentication for requests. This uses your email and your password to fetch the token.

``` amwater auth```

### amwater reset
For some reason if you need to reset your token , this will allow you to use your current authentication to reset and fetch your new token. This requires no user input

```amwater reset```

### amwater devlist
This will simply print the names of all devices to which you have access, instead of trying to remember the list. This tool requires no user input.

```
usage: amwater devlist [-h]

optional arguments:
  -h, --help  show this help message and exit

```

usage is simply

```amwater devlist```


### amwater spotcheck
This tool is built to fetch simply the latest information from the spotter including battery, humidity, power and lat long. Since these spotter can move across multiple time zones, it uses the lat long to estimate the time zone and converts the UTC time to local time for the spotter.

```
amwater spot-check -h

usage: amwater spot-check [-h] --sid SID

optional arguments:
  -h, --help  show this help message and exit

Required named arguments.:
  --sid SID   Spotter ID
```

Example usage would be

```
amwater spot-check --sid 0320
```


### amwater spotdata
This tool was designed to get the datasets out of the spotter. It seems that API currently returns about a month of data, and the best way to group it was using dates. This script uses the result JSON objects, and adds a date field from the timestamp to make the grouping easy, since timestamps are unique. This then writes these CSV file with column headers and can export both wind and wave data as needed.

```
usage: amwater spot-data [-h] --sid SID --dtype DTYPE --folder FOLDER

optional arguments:
  -h, --help       show this help message and exit

Required named arguments.:
  --sid SID        Spotter ID
  --dtype DTYPE    Data type: wind/wave
  --folder FOLDER  Folder to export CSV data

```

Sample setup would be

```
amwater spot-data --sid 1234 --dtype wave --folder "full path to folder"
```


## Changelog

#### v0.0.4
- added spot id to spot data export and metadata
- gracefully handles missing data and better error handling
- general improvements

#### v0.0.3
- added spot check tool to get latest info about spotter
- spot data now exports CSV after grouping by date
- general improvements

#### v0.0.2
- added time zone parser from spotter lat long
- now prints UTC and local time for spotter
- pretty prints output

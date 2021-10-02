# amwater: Alert CLI for American Water

![](https://tokei.rs/b1/github/samapriya/amwater?category=code)
![](https://tokei.rs/b1/github/samapriya/amwater?category=files)
[![CI amwater](https://github.com/samapriya/amwater/actions/workflows/ci-amwater.yml/badge.svg)](https://github.com/samapriya/amwater/actions/workflows/ci-amwater.yml)
![PyPI - License](https://img.shields.io/pypi/l/amwater)
![PyPI - Downloads](https://img.shields.io/pypi/dm/amwater)
![PyPI](https://img.shields.io/pypi/v/amwater)


## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [amwater Alert CLI for American Water](#amwater-alert-cli-for-american-water)
    * [amwater setup](#amwater-auth)
    * [amwater check](#amwater-reset)

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
usage: amwater [-h] {setup,amcheck} ...

Alert CLI for American water

positional arguments:
  {setup,amcheck}
    setup          Setup default address and optional (slack webhook)
    check          Check for any american water issued alerts for given
                   adddress

optional arguments:
  -h, --help       show this help message and exit
```

To obtain help for specific functionality, simply call it with _help_ switch, e.g.: `amwater amcheck -h`. If you didn't install amwater, then you can run it just by going to *amwater* directory and running `python amwater.py [arguments go here]`

## amwater Alert CLI for American Water
American water releases alerts for things like pipe repairs and water boil orders among other things for Illinois and areas it serves within the state. This tool is focused on allowing the user to quickly check if a give address has any alerts issued within a given number of days (defaults of last 1 day). Since there is no current API to fetch this information standard XML is parsed and a geocoding API endpoint from openstreetmap is used to confirm a geometry match.

### amwater setup
This allows you to save your default address, this also allows you to save a slack webhook which can be used to send messages incase there is an actual alert. This does require setting up a slackbot and enabling incoming webhook and is an experimental feature of the tool.

``` amwater setup```

### amwater check
This allows you to check any address for any alerts issues by american water within a given number of days. The number of days is an optional argument and the tool chooses 1 day as default for alert notification. The function also allows you to optinally pass the slack webhook url incase webhook url was not set during setup but it is completely optional.

```
amwater check -h
usage: amwater check [-h] [--address ADDRESS] [--days DAYS]
                     [--webhook WEBHOOK]

optional arguments:
  -h, --help         show this help message and exit

Optional named arguments:
  --address ADDRESS  Your address
  --days DAYS        Number of days to check for alert default is 1 day
  --webhook WEBHOOK  Slack webhook to send alert link (experimental)
```

if you have used the setup tool to set up a default address you can run the tool as is ```amwater check```. Other setups can be as following

```
amwater check --address "Hessel Boulevard,Champaign,IL"
```

with slack webhook incase you didn't save it using the setup tool

```
amwater check --address "Hessel Boulevard,Champaign,IL" --webhook "https://hooks.slack.com/services/T6U1JC/BVL5/Lw8uEYNWX4D7"
```

## Known issues
- Geometry search for this application is based on the responsiveness of the alert URL, while this usually works, it sometimes fails with the server not returning and expected result.
- This tool can be used without the slack webhook functionality to run spot checks (I will include a tutorial about setting up slack bots and webhook later at some point)

## Changelog

#### v0.0.2
- added date time parser to get date and time in 12 hr format
- integrated slack notificationa and webhook blocks
- general improvements to error handling
- overall improvements

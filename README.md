# arduino_libraries_search

This is a script to search into Arduino library.

## Install

This is just a work in progress.

No `setup.py` as it's just a script and 
you're supposed to know how to use it by watching code.

### Requirements
- python https://www.python.org/
- pandas https://pandas.pydata.org/
- click http://click.pocoo.org/
- requests_cache https://github.com/reclosedev/requests-cache
- openpyxl https://openpyxl.readthedocs.io/

### Install latest development version
```bash
$ git clone https://github.com/scls19fr/arduino_libraries_search/
$ cd arduino_libraries_search
```

## Usage
```bash
$ python arduino_search.py --help
Usage: arduino_search.py [OPTIONS]

Options:
  --max-rows INTEGER              Number of rows to display.
  --cache INTEGER                 Number of days to cache queries.
  --search TEXT                   Search keyword
  --write-excel / --no-write-excel
  --help                          Show this message and exit.
```

## Alternatives
- https://www.arduino.cc/en/Reference/Libraries
- https://www.arduinolibraries.info/
- https://platformio.org/lib

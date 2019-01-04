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
- python-semver>=2.8.0 https://github.com/k-bx/python-semver for https://semver.org/

### Install latest development version
```bash
$ git clone https://github.com/scls19fr/arduino_libraries_search/
$ cd arduino_libraries_search
```

## Usage
### Command line interface
See

```bash
$ python arduino_libraries_search.py --help
```

```bash
$ python arduino_libraries_show_license.py --help
```

### Interactive usage
Run IPython

```bash
$ ipython
```

try the following commands

```python
In [1]: import pandas as pd

In [2]: from utils import *

In [3]: pd.set_option('max_rows', MAX_ROWS_DEFAULT)

In [4]: df = download_index()

In [5]: df
Out[5]: 
     architectures             archiveFileName  \
2960            []             A4963-0.2.0.zip   
2959            []             A4963-0.1.0.zip   
2608           [*]  A4990MotorShield-2.0.0.zip   
3163           [*]            ACE128-1.7.0.zip   
3162           [*]            ACE128-1.6.2.zip   
...            ...                         ...   
3718           [*]      wiring_timer-2.4.0.zip   
2310           [*]   xxtea_iot_crypt-1.2.1.zip   
2309           [*]   xxtea_iot_crypt-1.2.0.zip   
2308           [*]   xxtea_iot_crypt-1.1.0.zip   
2307           [*]   xxtea_iot_crypt-1.0.0.zip
...

In [6]: name = "ArduinoJSON"

In [7]: find_nearest_names(name, df)  # passing df is optional
Out[7]: 
                 name     score
1         ArduinoJson  1.000000
2        ArduinoSound  0.666667
3          ArduinoIHC  0.631579
4          ArduinoIRC  0.631579
5          ArduinoSTL  0.631579
...               ...       ...
1532             Luni  0.000000
1533           M10ADC  0.000000
1534         M10CODEC  0.000000
1535          M10DTMF  0.000000
1536  xxtea-iot-crypt  0.000000

[1536 rows x 2 columns]

In [8]: name = find_nearest_name(name, df)

In [9]: name
Out[9]: 'ArduinoJson'

In [10]: get_versions(name, df)  # passing df is optional
Out[11]: 
45    5.9.0
44    5.8.4
43    5.8.3
42    5.8.2
41    5.8.1
      ...  
5     5.0.3
4     5.0.2
3     5.0.1
2     5.0.0
1     4.0.0
Name: version, Length: 45, dtype: object

In [11]: version = get_latest_version(name, df)  # passing df is optional

In [12]: version
Out[12]: '5.9.0'

In [13]: url = get_archive_url(name, version, df)  # passing df is optional

In [14]: url
Out[14]: 'http://downloads.arduino.cc/libraries/github.com/bblanchon/ArduinoJson-5.9.0.zip'

In [15]: show_licence(url)

ArduinoJson-5.9.0/LICENSE.md

The MIT License (MIT)
---------------------

Copyright © 2014-2017 Benoit BLANCHON

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

In [16]: show_versions(name)
Out[16]: 
45    5.9.0
44    5.8.4
43    5.8.3
42    5.8.2
41    5.8.1
      ...  
5     5.0.3
4     5.0.2
3     5.0.1
2     5.0.0
1     4.0.0
Name: version, Length: 45, dtype: object

In [17]: show_licence(name)  # to show license of latest version

In [18]: show_licence(name, "5.8.0")  # to show license of a given version

In [19]: search("json")  # several keywords must be separated with a white space (use at your own risk)
                              architectures  \
name                                          
AJSP                                    [*]   
ArduinoJson                             [*]   
Bifrost library for HC-SR04             [*]   
CTBot                                   [*]   
Constellation                           [*]   
IFTTTMaker                              [*]   
InstagramStats                          [*]   
Json Streaming Parser                   [*]   
Marceau                      [avr, esp8266]
```

Have a look at code to see more commands!

Reading "Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython" may help.

## Alternatives
- https://www.arduino.cc/en/Reference/Libraries
- https://www.arduinolibraries.info/
- https://github.com/arduino/arduino-cli
- https://platformio.org/lib

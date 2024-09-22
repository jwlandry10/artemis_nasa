#!/usr/bin/python3

import ephem
import datetime
## [...]

name = "ISS (ZARYA)";
line1 = "1 25544U 98067A   24266.53887038  .00020034  00000-0  36467-3 0  9990";
line2 = "2 25544  51.6393 193.1783 0007440  21.6459 148.9337 15.49461066473644";

tle_rec = ephem.readtle(name, line1, line2);
tle_rec.compute();

print(tle_rec.sublong, tle_rec.sublat);
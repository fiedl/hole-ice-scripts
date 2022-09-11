#!/usr/bin/env python

import os
from I3Tray import I3Tray
from icecube import icetray, phys_services, dataio, dataclasses

from I3Tray import I3Units
from icecube.dataclasses import I3Position, I3Direction
from icecube.simclasses import I3FlasherPulse, I3FlasherPulseSeries
from icecube.simclasses import I3CLSimMediumCylinder, I3CLSimMediumCylinderSeries

DETECTOR_GEOMETRY_FILE = os.path.expandvars(
  '$I3_TESTDATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz')

def main():
  tray = I3Tray()

  tray.Add(
    'I3Reader',
    Filenamelist = [DETECTOR_GEOMETRY_FILE]
  )

  tray.Add(
    add_hole_ice_cylinders,
    Streams = [icetray.I3Frame.Geometry]
  )

  tray.AddModule(
    'I3Writer',
    filename = "data/hole_ice_geometry.i3"
  )

  tray.Execute()

def add_hole_ice_cylinders(frame):
  cylinder = I3CLSimMediumCylinder()
  cylinder.x = -256.02301025390625
  cylinder.y = -521.2819824218750
  cylinder.radius = 0.3
  cylinder.scattering_length = 100.0
  cylinder.absorption_length = 0.0

  cylinders = I3CLSimMediumCylinderSeries([cylinder])
  frame.Put("cylinders", cylinders)

if __name__=='__main__':
  main()

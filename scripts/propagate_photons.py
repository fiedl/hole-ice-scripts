#!/usr/bin/env python

import os
from I3Tray import I3Tray
from icecube import icetray, clsim, phys_services, simclasses, photonics_service

DETECTOR_GEOMETRY_FILE = os.path.expandvars(
  '$I3_TESTDATA/GCD/GeoCalibDetectorStatus_2020.Run134142.Pass2_V0.i3.gz')

icetray.set_log_level(icetray.I3LogLevel.LOG_TRACE)


def main():
  random_number_generator = phys_services.I3SPRNGRandomService(
    seed = 1234,
    nstreams = 100000000,
    streamnum = 1
  )

  tray = I3Tray()
  tray.context['I3RandomService'] = random_number_generator

  tray.Add(
    'I3Reader',
    Filenamelist = [DETECTOR_GEOMETRY_FILE, 'data/generated_photons.i3']
  )

  tray.Add(
    clsim.I3CLSimMakePhotons,
    GCDFile = DETECTOR_GEOMETRY_FILE,
    UseCPUs = True,
    UseGPUs = False,
    UseI3PropagatorService = False,
    #MCTreeName = 'I3MCTree',
    OutputMCTreeName = None,
    PhotonSeriesName = 'PhotonSeriesMap',
    MCPESeriesName = None,
    RandomService = tray.context['I3RandomService'],
    IceModelLocation = os.path.expandvars('$I3_SRC/ice-models/resources/models/ICEMODEL/spice_bfr-v2'),
    UseCascadeExtension = False,
    DisableTilt = False,
    DoNotParallelize = False,
    DOMOversizeFactor = 1.0,
    DOMEfficiency = 1.0,
    HoleIceParameterization = os.path.expandvars('$I3_SRC/ice-models/resources/models/ANGSENS/angsens/as.nominal'), # no hole-ice approximation
    UnWeightedPhotons = True,
    UnWeightedPhotonsScalingFactor = 1.0,
    StopDetectedPhotons = False,
    SaveAllPhotons = True,
    SaveAllPhotonsPrescale = 1.0,
    PhotonHistoryEntries = 0 # infinite entries
  )

  tray.Add(
    'I3Writer',
    filename = "data/propagated_photons.i3"
  )

  tray.Execute()


if __name__=='__main__':
  main()
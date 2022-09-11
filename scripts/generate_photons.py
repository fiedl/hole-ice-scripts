#!/usr/bin/env python

import os
from I3Tray import I3Tray
from icecube import icetray, phys_services, dataio

from I3Tray import I3Units
from icecube.dataclasses import I3Position, I3Direction
from icecube.simclasses import I3FlasherPulse, I3FlasherPulseSeries

NUMBER_OF_FRAMES_TO_GENERATE = 1
PHOTON_START_POSITION = I3Position(-256.02301025390625 + 1, -521.281982421875, 500)
PHOTON_START_DIRECTION = I3Direction(-1.0, 0, 0)

def main():
  random_number_generator = phys_services.I3GSLRandomService(
    seed = 1234
  )

  tray = I3Tray()
  tray.context['I3RandomService'] = random_number_generator

  tray.AddModule(
    "I3InfiniteSource",
    Stream = icetray.I3Frame.DAQ
  )

  tray.Add(
    generate_photons,
    Streams = [icetray.I3Frame.DAQ]
  )

  tray.AddModule(
    'I3Writer',
    filename = "data/generated_photons.i3",
    streams = [icetray.I3Frame.DAQ]
  )

  tray.Execute(NUMBER_OF_FRAMES_TO_GENERATE)


def generate_photons(frame):
  pulse = I3FlasherPulse()

  pulse.SetPos(PHOTON_START_POSITION)
  pulse.SetDir(PHOTON_START_DIRECTION)
  pulse.SetTime(0.0 * I3Units.ns)
  pulse.SetNumberOfPhotonsNoBias(30)
  pulse.SetType(I3FlasherPulse.FlasherPulseType.LED340nm)
  pulse.SetPulseWidth(1. * I3Units.ns)
  pulse.SetAngularEmissionSigmaPolar(0.001 * I3Units.deg)
  pulse.SetAngularEmissionSigmaAzimuthal(0.001 * I3Units.deg)

  pulse_series = I3FlasherPulseSeries()
  pulse_series.append(pulse)

  frame['PhotonFlasherPulseSeries'] = pulse_series


if __name__=='__main__':
  main()

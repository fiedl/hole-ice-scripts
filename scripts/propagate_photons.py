#!/usr/bin/env python

import os
from I3Tray import I3Tray
from icecube import icetray, clsim, phys_services, simclasses, photonics_service, dataclasses

icetray.set_log_level(icetray.I3LogLevel.LOG_TRACE)


def main():
  random_number_generator = phys_services.I3GSLRandomService(
    seed = 1234
  )

  tray = I3Tray()
  tray.context['I3RandomService'] = random_number_generator

  tray.Add(
    'I3Reader',
    Filenamelist = ['data/hole_ice_geometry.i3', 'data/generated_photons.i3']
  )

  tray.Add(
    clsim.I3CLSimMakePhotons,
    GCDFile = 'data/hole_ice_geometry.i3',
    UseCPUs = True,
    UseGPUs = False,
    UseI3PropagatorService = False,
    OutputMCTreeName = None,
    FlasherPulseSeriesName = 'PhotonFlasherPulseSeries',
    PhotonSeriesName = 'PhotonSeriesMap',
    MCPESeriesName = None,
    RandomService = tray.context['I3RandomService'],
    IceModelLocation = os.path.expandvars('$I3_SRC/ice-models/resources/models/ICEMODEL/spice_bfr-v2'),
    UseCascadeExtension = False,
    DisableTilt = False,
    DoNotParallelize = True,
    DOMOversizeFactor = 1.0,
    DOMEfficiency = 1.0,
    HoleIceParameterization = os.path.expandvars('$I3_SRC/ice-models/resources/models/ANGSENS/angsens/as.nominal'), # no hole-ice approximation
    UnWeightedPhotons = True,
    UnWeightedPhotonsScalingFactor = 1.0,
    StopDetectedPhotons = False,
    SaveAllPhotons = True,
    SaveAllPhotonsPrescale = 1.0,
    PhotonHistoryEntries = 100
  )

  # Add a fake monte-carlo-particle tree as workaround for a steamshovel issue:
  # https://github.com/fiedl/hole-ice-scripts/issues/6#issuecomment-1212560461
  # FIXME Resolve steamshovel issue and remove this step.
  #
  tray.Add(
    add_fake_monte_carlo_particle_tree,
    Streams = [icetray.I3Frame.DAQ]
  )

  tray.Add(
    'I3Writer',
    filename = "data/propagated_photons.i3"
  )

  tray.Add(
    count_propagated_photons,
    Streams = [icetray.I3Frame.DAQ]
  )

  tray.Execute()

# Add a fake monte-carlo tree as workaround for a steamshovel issue:
# https://github.com/fiedl/hole-ice-scripts/issues/6#issuecomment-1212560461
# FIXME Resolve steamshovel issue and remove this function.
#
def add_fake_monte_carlo_particle_tree(frame):
  frame['I3MCTree'] = dataclasses.I3MCTree()
  particle = dataclasses.I3Particle()
  particle.pos = dataclasses.I3Position(-255.023, -521.282, 500)
  particle.dir = dataclasses.I3Direction(3.14 / 2, 0)
  particle.time = 0
  particle.type = dataclasses.I3Particle.ParticleType.Hadrons
  frame['I3MCTree'].add_primary(particle)

def count_propagated_photons(frame):
  print(f"number of PhotonSeriesMap entries: {len(frame['PhotonSeriesMap'])}")

if __name__=='__main__':
  main()

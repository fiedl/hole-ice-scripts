# Hole-Ice Scripts

Example scripts for the hole-ice extension of clsim in the IceCube simulation framework.

## Usage

### Checkout this repo

```
[2022-08-10 11:16:50] fiedl@fiedl-mbp ~/icecube
▶ git clone git@github.com:fiedl/hole-ice-scripts.git
```

### Generate photons

```
[2022-08-11 17:08:05] fiedl@fiedl-mbp ~/icecube/hole-ice-scripts master ⚡ e6cc5e9
▶ docker-compose run icetray scripts/generate_photons.py
```

### Add hole-ice cylinders to detector geometry

```python
# in: scripts/generate_hole_ice_geometry.py

tray.Add(
  add_hole_ice_cylinders,
  Streams = [icetray.I3Frame.Geometry]
)

def add_hole_ice_cylinders(frame):
  cylinder = I3CLSimMediumCylinder()
  cylinder.x = -256.02301025390625
  cylinder.y = -521.2819824218750
  cylinder.radius = 0.3
  cylinder.scattering_length = 100.0
  cylinder.absorption_length = 0.0

  cylinders = I3CLSimMediumCylinderSeries([cylinder])
  frame.Put("I3CLSimMediumCylinders", cylinders)
```

```
[2022-09-11 23:01:53] fiedl@kepler00 ~/icecube/hole-ice-scripts master ⚡ 60d7778
▶ scripts/generate_hole_ice_geometry.py
```

### Propagate Photons

```
[2022-08-11 17:08:05] fiedl@fiedl-mbp ~/icecube/hole-ice-scripts master ⚡ 4b4a968
▶ docker-compose run icetray scripts/propagate_photons.py
```


## SSH connection to Zeuthen

1. Install `openssh` from homebrew.

   ```shell
   [2022-09-10 13:46:51] fiedl@fiedl-mbp ~/icecube
   ▶ brew install openssh
   ▶ ssh -V
   OpenSSH_8.6p1, LibreSSL 3.3.6
   ```

2. Configure `~/.ssh/config`

   ```shell
   # ~/.ssh/config

   host pub*.zeuthen.desy.de transfer.zeuthen.desy.de transfer.ifh.de
     ProxyCommand none

   host burst.ifh.de transit.ifh.de
     IdentityFile ~/.ssh/id_rsa.zeuthen
     ProxyCommand ssh -qax -W %h:%p ztf-wgs.ifh.de

   host *.ifh.de *.zeuthen.desy.de
     User fiedl
     GSSAPIAuthentication yes
     GSSAPIDelegateCredentials yes
     ProxyCommand ssh -qax -W %h:%p pub2.zeuthen.desy.de

   host *
     ServerAliveInterval 55
     ServerAliveCountMax 5
     ControlPath ~/.ssh/master-%r@%h:%p
   ```

3. Request kerberos ticket. This will ask for your password one and allow password-less login for 30 days.

   ```shell
   [2022-09-10 13:46:51] fiedl@fiedl-mbp ~/icecube
   ▶ kinit --renewable fiedl@IFH.DE
   ```

4. Then `ssh` into the gpu machine in zeuthen.

   ```
   [2022-09-10 13:46:51] fiedl@fiedl-mbp ~/icecube
   ▶ ssh ice-wgs-gpu.ifh.de
   ```

## Build icetray in Zeuthen

1. Clone repos locally on your development machine.

   ```shell
   [2022-08-10 11:16:50] fiedl@fiedl-mbp ~/icecube
   ▶ git clone git@github.com:icecube/icetray.git
   ▶ git clone git@github.com:fiedl/hole-ice-scripts.git
   ```

2. Use scratch space for quota reasons in zeuthen.

   ```shell
   [2022-09-09 14:20:59] fiedl@kepler00 ~
   ▶ ln -s /afs/ifh.de/group/amanda/scratch/fiedl/icecube ~/icecube
   ```

3. Sync local dev machine with zeuthen.

   ```shell
   [2022-09-09 14:23:47] fiedl@fiedl-mbp ~/icecube
   ▶ brew install mutagen-io/mutagen/mutage
   ▶ brew install mutagen-io/mutagen/mutagen-compose
   ▶ mutagen sync create --stage-mode=internal --sync-mode=two-way-resolved --name hole-ice-scripts-zeuthen ~/icecube/hole-ice-scripts fiedl@ice-wgs-gpu.ifh.de:~/icecube/hole-ice-scripts
   ▶ mutagen sync create --stage-mode=internal --sync-mode=two-way-resolved --name icetray-zeuthen ~/icecube/icetray fiedl@ice-wgs-gpu.ifh.de:~/icecube/icetray
   ```

   [Mutagen](https://github.com/fiedl/hole-ice-scripts/issues/9#issuecomment-1242719364) will keep the local directories in sync with the zeuthen directories. This is similar to mounting, but you have a local copy, and it feels much faster because you are not constantly waiting for the remote server. To stop the background sync, run: `mutagen sync terminate icetray-zeuthen hole-ice-scripts-zeuthen`.

4. For opencl support, we need a newer cmake version in zeuthen.

   ```shell
   [2022-09-09 16:28:48] fiedl@kepler00 ~/icecube
   ▶ wget -qO- https://github.com/Kitware/CMake/releases/download/v3.24.1/cmake-3.24.1.tar.gz | tar xz

   [2022-09-09 16:30:43] fiedl@kepler00 ~/icecube/cmake-3.24.1
   ▶ cmake .
   ▶ make -j 8
   ▶ export PATH=~/icecube/cmake-3.24.1/bin:$PATH
   ▶ cmake --version
   cmake version 3.24.1
   ```

5. Finally, build icetray in zeuthen.

   ```shell
   [2022-09-09 16:39:46] fiedl@kepler00 ~/icecube/icetray-build
   ▶ /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/setup.sh
   ▶ module load cuda/11.6
   ▶ export OPENCL_VENDOR_PATH=/cvmfs/icecube.opensciencegrid.org/distrib/OpenCL_RHEL_7_x86_64/etc/OpenCL/vendors
   ▶ cmake -D CMAKE_BUILD_TYPE=Debug -D SYSTEM_PACKAGES=true ../icetray
   ▶ make -j 8
   ```

6. Run a test script in zeuthen.

   ```shell
   [2022-09-09 17:50:55] fiedl@kepler00 ~/icecube/hole-ice-scripts
   ▶ ~/icecube/icetray-build/env-shell.sh
   ▶ scripts/generate_photons.py
   ▶ scripts/propagate_photons.py
   ```

## Manual Installation on macOS

OpenCL is currently [not supported](https://github.com/fiedl/hole-ice-scripts/issues/11) by icetray on M1 chips. But installing icetray on macOS is still useful to run steamshovel locally.

```
[2022-08-10 11:16:50] fiedl@fiedl-mbp ~/icecube
▶ git clone git@github.com:icecube/icetray.git

[2022-08-10 11:44:58] fiedl@fiedl-mbp ~/icecube/icetray main 6ce97c3a7
▶ brew bundle

[2022-08-10 13:59:36] fiedl@fiedl-mbp ~/icecube/icetray main 6ce97c3a7
▶ brew unlink python@3.9
▶ brew link python@3.10
▶ python3 --version
Python 3.10.6

[2022-08-10 13:31:06] fiedl@fiedl-mbp ~/icecube/icetray main 6ce97c3a7
▶ python3 -m venv --system-site-packages ${HOME}/py3/
▶ source ${HOME}/py3/bin/activate

# https://github.com/freqtrade/freqtrade/issues/4162
[2022-08-10 13:44:03] fiedl@fiedl-mbp ~/icecube/icetray main 6ce97c3a7
▶ export HDF5_DIR=/opt/homebrew/

[2022-08-10 13:35:40] fiedl@fiedl-mbp ~/icecube/icetray main 6ce97c3a7
▶ python3 -m pip install --upgrade pip
▶ python3 -m pip install -r requirements.txt

[2022-08-10 11:43:32] fiedl@fiedl-mbp ~/icecube/icetray-build
▶ cmake -D CMAKE_BUILD_TYPE=Debug -D SYSTEM_PACKAGES=true ~/icecube/icetray
...
-- python
-- +  version: 3.10.6
-- +   binary: /Users/fiedl/py3/bin/python3.10
-- + includes: /opt/homebrew/opt/python@3.10/Frameworks/Python.framework/Versions/3.10/include/python3.10
-- +     libs: /opt/homebrew/opt/python@3.10/Frameworks/Python.framework/Versions/3.10/lib/libpython3.10.dylib
-- +    numpy: /opt/homebrew/lib/python3.10/site-packages/numpy/core/include
-- +    scipy: FOUND
--
-- Boost
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE
-- Found Boost: /opt/homebrew/include (found version "1.79.0") found components: system thread date_time filesystem program_options regex iostreams python310 chrono atomic

[2022-08-10 14:23:08] fiedl@faustaff-010-020-007-137 ~/icecube/icetray-build
▶ make -j 4
```

## Further Resources

- Framework Repository: https://github.com/icecube/icetray
- Framework Documentation: https://docs.icecube.aq/icetray/main/

## Author and License

2022, Sebastian Fiedlschuster and the IceCube Collaboration
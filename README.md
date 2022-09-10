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

### Propagate Photons

```
[2022-08-11 17:08:05] fiedl@fiedl-mbp ~/icecube/hole-ice-scripts master ⚡ 4b4a968
▶ docker-compose run icetray scripts/propagate_photons.py
```


## Manual Installation on macOS

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

## Further Resources

- Framework Repository: https://github.com/icecube/icetray
- Framework Documentation: https://docs.icecube.aq/icetray/main/

## Author and License

2022, Sebastian Fiedlschuster and the IceCube Collaboration
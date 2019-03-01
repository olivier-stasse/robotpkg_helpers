# Robotpkg Helpers

This is a python package providing tools to handle [robotpkg](http://robotpkg.openrobots.org/robotpkg/README.html).

## Creating your own install of the SoT from source:

### Creates your workspace:
```
sudo prepare_integration_dirs.py
```
This will create the directories:
```
/integration_tests/arch_distfiles
/integration_tests/archives
/integration_tests/robotpkg-test-rc
```
<b>robotpkg-test-rc</b> should be highlighted because it is mounted over a ram filesystem.
This is allowing faster access time when compiling.
Be aware that turn off your computer may make you loose all the data in this directory.
This problem is addressed in the following steps.

### Deploy a first application
'''
build_talos_simpulation.py
'''
This will build a complete installation of the packages needed to simulate the TALOS robot.
It however computes only the PAL robotics packages, the standard ROS packages are assumed to be installed previously.
The robotpkg sources are located in:
'''
/integration_tests/robotpkg-test-rc/robotpkg
'''
The wip robotpkg sources are located in:
'''
/integration_tests/robotpkg-test-rc/robotpkg/wip
'''
The installation is realized in :
'''
/integration_tests/robotpkg-test-rc/install
'''

### Make a first backup
'''
save_integration_dir.py
'''
This will save the following directories:
'''
/integration_tests/robotpkg-test-rc/robotpkg
/integration_tests/robotpkg-test-rc/install
'''
in the file called 
```
robotpkg_year_month_day_hour_sec.tgz
```
located in this directory:
```
/integration_tests/archives
```


## Tools

Set of python scripts to perform:
- [Build the ramfs and create the integration_tests directory architecture ](robotpkg_helpers/tools/prepare_integration_dirs.py)
```
sudo prepare_integration_dirs.py
```
- [Build the stack to make talos simulation](robotpkg_helpers/tools/build_talos_simulation.py)
```
build_talos_simulation.py
```
- [Build the stack to build SoT with talos](robotpkg_helpers/tools/build_talos_dev.py)
- [Remove install and robotpkg directories inside /integration_tests/](robotpkg_helpers/tools/clean_integration_dir.py)
- [Save the install and robotpkg directories inside /integration_tests/ inside archives](robotpkg_helpers/tools/save_integration_dir.py)
The format of the file is
```
/integration_tests/archives/robotpkg_year_month_day.tgz
/integration_tests/archives/robotpkg_year_month_day.txt
```
The text file record the release of each robotpkg package installed.
- [Restore the install and robotpkg directories inside /integration_tests/ from a file located in archives](robotpkg_helpers/tools/restore_dir.py)

## Tests

Set of python scripts  to perform:
- [Deployment tests for a given set of packages and specific branches in default directory (~/devel-src/robotpkg-test-rc)](robotpkg_helpers/tests/test_rc.py)
- [Deployment tests for a given set of packages and specific branches in a specified directory](robotpkg_helpers/tests/test_rc_other_path.py)
This can be useful if the defaut policy is not right for you.
- [Deployment tests using a destfiles directory and a personal fork of robotpkg](robotpkg_helpers/tests/test_distfiles.py)
- [Generate a dockerfile based on parsing a Makefile using jrl-cmakemodules](robotpkg_helpers/tests/test_gen_dockerfile.py)

## robotpkg_helpers module

### RobotpkgPackage

This class is analyzing the directory of a package and extracts information
reading the files Makefile and depend.mk

### RobotpkgSrcIntrospection

This class is analyzing a clone of the robotpkg repository and is trying
to make simple inferences on the packages dependencies

### RobotpkgTests

This class is building instance of robotpkg to make deployment tests.
It is useful for instance to test if various releases of packages are coherent
together.


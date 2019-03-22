# Robotpkg Helpers

This is a python package providing tools to handle [robotpkg](http://robotpkg.openrobots.org/robotpkg/README.html).

## Building and deploy a local install of the [stack-of-tasks](http://stack-of-tasks.github.io) from source:

### Creating your workspace:

First types:
```
sudo rpkgh_prepare_integration_dirs.py
```

This will create the directories:

```
/integration_tests/arch_distfiles
/integration_tests/archives
/integration_tests/robotpkg-test-rc
```

Creating you ramfs is optional now. It is done by:
```
sudo rpkgh_create_ramfs
```
Note: *robotpkg-test-rc* should be highlighted because it is mounted over a ram filesystem.
This is allowing faster access time when compiling.
Be aware that turn off your computer may make you lost all the data in this directory.
This problem is addressed in the following steps.

### Deploy a first application
Going into the tools directory and use:
```
./rpkgh_build_arch_rc.py ./arch_test_rc.json
```

This will build a complete installation of the packages needed to simulate the TALOS robot.
It however computes only the PAL robotics packages, the standard ROS packages are assumed to be installed.
The robotpkg sources are located in:
```
/integration_tests/robotpkg-test-rc/robotpkg
```

The wip robotpkg sources are located in:
```
/integration_tests/robotpkg-test-rc/robotpkg/wip
```

The installation is realized in :
```
/integration_tests/robotpkg-test-rc/install
```

### Make a first backup
```
rpkgh_save_integration_dir.py
```
This will save the following directories:
```
/integration_tests/robotpkg-test-rc/robotpkg
/integration_tests/robotpkg-test-rc/install
```
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

- [Build the ramfs and create the integration_tests directory architecture ](tools/rpkgh_prepare_integration_dirs.py)
```
sudo rpkgh_prepare_integration_dirs.py
```
- [Remove install and robotpkg directories inside /integration_tests/](tools/rpkgh_clean_integration_dir.py)
- [Save the install and robotpkg directories inside /integration_tests/ inside archives](tools/rpkgh_save_integration.py)
The format of the file names is
```
/integration_tests/archives/robotpkg_year_month_day.tgz
/integration_tests/archives/robotpkg_year_month_day.txt
```
The text file record the release of each robotpkg package installed.
- [Restore the install and robotpkg directories inside /integration_tests/ from a file located in archives](tools/rpkgh_restore_dir.py)
- [Deployment tests for a given set of packages and specific branches in a specified directory](tools/rpkgh_rc_other_path.py)
This file read a json file specifying the packages and the branch to build. The file <b>arch_rc.json</b> is an example of such a file:
```
[["dynamic-graph-v3", "devel"], ["sot-core-v3", "devel"], ["py-sot-core-v3", "devel"], ["sot-tools-v3","devel"],["py-sot-tools-v3","devel"],["sot-dynamic-pinocchio-v3", "devel"], ["py-sot-dynamic-pin
occhio-v3", "devel"], ["tsid", "devel"], ["parametric-curves", "devel"], ["sot-torque-control", "devel"], ["sot-talos", "master"]]
```
- [Deployment tests using a destfiles directory and a personal fork of robotpkg](tools/rpkgh_distfiles.py)
- [Generate a dockerfile based on parsing a Makefile using jrl-cmakemodules](tools/rpkgh_gen_dockerfile.py)

## JSON format

An example of release architecture to be tested and described using JSON is present in the tools directory:
[arch_test_rc.json](tools/arch_test_rc.json)

### Main fields
```
{"arch_dist_files": "arch_distfiles",
 "archives": "archives",
 "ramfs_mnt_pt": "robotpkg-test-rc", 
 "repo_robotpkg_wip": "https://git.openrobots.org/robots/robotpkg/robotpkg-wip.git",
 "repo_robotpkg_main": "https://git.openrobots.org/robots/robotpkg.git",
 "robotpkg_mng_root": "/integration_tests", 
 "rc_pkgs":
```

 - The field *arch_dist_files* tells where to store the tar ball of packages release.
They can be store here to avoid having to download them at each test.
 - The field *ramfs_mnt_pt* indicates where the pair install/robotpkg is located. It indicates
where a self-contained development environment is deployed.
 - The field *archives* stores the tar ball of the pair install/robotpkg
 - The field *repo_robotpkg_main* indicates the robotpkg repository to use. 
It is useful when you need to have a version of robotpkg slightly modify for your integration test.
 - The field *repo_robotpkg_wip* indicates the wip robotpkg repository to use.
 - The field *robotpkg_mng_root* indicates the repository where you can managed several integration tests.
 - The field *rc_pkgs* indicates the packages for which you need a special treatment.
 - The field *ssh_git_openrobots* indicates if ssh should be used for authentification when accessing the repositories when the choice
is possible. Currently this applies only to repo_robopkg_wip and repo_robotpkg_main.
As this is clearly indicated in the repo URL, it is likeley that this option will disappear.
 - The field *targetpkg* indicates to robotpkg_helper which package to compile.

### A package
```
 "rc_pkgs":
 {"dynamic-graph-v3": {"name": "dynamic-graph-v3",
		       "branch": "devel",
		       "commit": null,
		       "git_repo": "https://github.com/stack-of-tasks/dynamic-graph.git",
		       "tag": null},
```
A package inside the dictionnary *rc_pkgs* is a python dictionnary with the following supported fields:

 - *name*: The name of the robotpkg package
 - *branch*: The name of the branch you want to pull
 - *commit*: Not yet supported
 - *git_repo*: The name of the repository you want to pull your branch
 - *tag*: Not yet supported

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


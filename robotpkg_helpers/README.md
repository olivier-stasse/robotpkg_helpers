# Robotpkg Helpers

This is a python package providing tools to handle [robotpkg](http://robotpkg.openrobots.org/robotpkg/README.html).

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

## Tests

Set of python scripts using the previous classes to perform:
- [Deployment tests for a given set of packages and specific branches in default directory (~/devel-src/robotpkg-test-rc)](tests/test_rc.py)
- [Deployment tests for a given set of packages and specific branches in a specified directory](tests/test_rc_other_path.py)
This can be useful if the defaut policy is not right for you.
- [Deployment tests using a destfiles directory and a personal fork of robotpkg](tests/test_distfiles.py)
- [Generate a dockerfile based on parsing a Makefile using jrl-cmakemodules](tests/test_gen_dockerfile.py)

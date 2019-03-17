#!/usr/bin/python3
from robotpkg_helpers import RobotpkgArchitectureReleaseCandidate

a_rpkg_arch_rc = RobotpkgArchitectureReleaseCandidate()
a_rpkg_arch_rc.default_init()
a_rpkg_arch_rc.save_rc("/tmp/arch_test_rc.json")

#!/usr/bin/python3
import os
from robotpkg_helpers import RobotpkgTests, build_test_rc_robotpkg_vars


arch_release_candidates= [ ('sot-core-v3','master'),
                           ('py-sot-core-v3','master'),
                           ('sot-dynamic-pinocchio-v3','master'),
                           ('py-sot-dynamic-pinocchio-v3','master'),
                           ('roscontrol-sot','master'),
                           ('sot-talos','master')
                           ]

robotpkg_vars = build_test_rc_robotpkg_vars()
dist_files_path=robotpkg_vars['DISTFILES']
arpgtestrc =RobotpkgTests("/integration_tests")

# Perform the deployment in arpgtestrc
if arpgtestrc.perform_test_rc(arch_release_candidates,dist_files_path):
    # If it worked then compile the package talos-dev
    arpgtestrc.compile_package('talos-dev')
else:
    print("Wrong handling of packages")

#!/usr/bin/python3
import os
from robotpkg_helpers import RobotpkgTests, build_test_rc_robotpkg_vars


# arch_release_candidates= [ ('dynamic-graph-v3','devel'),
#                            ('sot-core-v3','devel'),
#                            ('py-sot-core-v3','devel'),
#                            ('sot-dynamic-pinocchio-v3','devel'),
#                            ('py-sot-dynamic-pinocchio-v3','devel'),
#                            ('tsid','devel'),
#                            ('parametric-curves','devel'),
#                            ('sot-torque-control','devel'),
#                            ('sot-talos','master')
# ]

robotpkg_vars = build_test_rc_robotpkg_vars()
dist_files_path=robotpkg_vars['DISTFILES']
arpgtestrc =RobotpkgTests("/opt/openrobots-frisbourg")

# Perform the deployment in arpgtestrc
if arpgtestrc.perform_test_rc(dist_files_path=dist_files_path):
    # If it worked then compile the package talos-dev
    arpgtestrc.compile_package('talos-dev')
else:
    print("Wrong handling of packages")

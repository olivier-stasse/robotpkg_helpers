#!/usr/bin/python3
import os
import json
from robotpkg_helpers import RobotpkgTests, build_test_rc_robotpkg_vars

with open('arch_rc.json') as f:
  arch_release_candidates=json.load(f)
  
print(arch_release_candidates)

robotpkg_vars = build_test_rc_robotpkg_vars()
dist_files_path=robotpkg_vars['DISTFILES']
arpgtestrc =RobotpkgTests("/opt/openrobots-frisbourg")

# Perform the deployment in arpgtestrc
if arpgtestrc.perform_test_rc(dist_files_path=dist_files_path):
    # If it worked then compile the package talos-dev
    arpgtestrc.compile_package('talos-dev')
else:
    print("Wrong handling of packages")

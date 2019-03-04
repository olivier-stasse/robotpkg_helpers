#!/usr/bin/python3
import os
from robotpkg_helpers import RobotpkgTests, build_test_rc_robotpkg_vars,HandlingImgs

def build_talos_simulation():
    
    aHandlingImg = HandlingImgs()
    
    robotpkg_vars = build_test_rc_robotpkg_vars()
    dist_files_path=robotpkg_vars['DISTFILES']
    arpgtestrc =RobotpkgTests("/integration_tests/robotpkg-test-rc",debug=5)

    # Perform the deployment in arpgtestrc
    if arpgtestrc.perform_test_rc(dist_files_path=dist_files_path):
        # If it worked then compile the package talos-simulation
        arpgtestrc.compile_package('talos-simulation')
    else:
        print("Wrong handling of packages")

if __name__ == "__main__":
    build_talos_simulation()


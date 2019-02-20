#!/usr/bin/python3
from robotpkg_helpers import RobotpkgTests

arch_release_candidates= [ ('dynamic-graph-v3','rc-v3.2.2'),
                           ('sot-core-v3','rc-v3.3.1'),
                           ('py-dynamic-graph-bridge-v3','rc-v3.2.3'),
                           ]


arpgtestrc =RobotpkgTests("/tmp/robotpkg-test-rc")
arpgtestrc.perform_test_rc(arch_release_candidates)
arpgtestrc.compile_package('talos-dev')

#!/usr/bin/python3
from unittest import TestCase

from robotpkg_helpers import RobotpkgSrcIntrospection, build_test_rc_robotpkg_vars
from robotpkg_helpers import init_environment_variables

robotpkg_root='/integration_tests/robotpkg-test-rc'
robotpkg_vars = build_test_rc_robotpkg_vars(robotpkg_root)

arpg_src_intros = RobotpkgSrcIntrospection(robotpkg_vars['SRC'])
init_environment_variables(arpg_src_intros,robotpkg_root)
arpg_src_intros.display()
arpg_src_intros.save('rpg_src_intros.json')

arpg_src_intros.package_dict['jrl-walkgen-v3'].is_rpkg_installed(robotpkg_vars['INSTALL'],arpg_src_intros.env)
arpg_src_intros.package_dict['pinocchio'].is_rpkg_installed(robotpkg_vars['INSTALL'],arpg_src_intros.env)
arpg_src_intros.package_dict['talos-simulation'].is_rpkg_installed(robotpkg_vars['INSTALL'],arpg_src_intros.env)

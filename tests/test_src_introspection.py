#!/usr/bin/python3
from unittest import TestCase

from robotpkg_helpers import RobotpkgSrcIntrospection
from robotpkg_helpers import init_environment_variables
from robotpkg_helpers.utils import add_robotpkg_mng_variables

robotpkg_root='/integration_tests/robotpkg-test-rc'
#robotpkg_vars = add_robotpkg_mng_variables(robotpkg_root)

arpg_src_intros = RobotpkgSrcIntrospection(ROBOTPKG_ROOT_SRC=robotpkg_root+'/robotpkg')
add_robotpkg_mng_variables(arpg_src_intros)

init_environment_variables(arpg_src_intros,robotpkg_root)
arpg_src_intros.display()
arpg_src_intros.save('rpg_src_intros.json')

arpg_src_intros.package_dict['jrl-walkgen-v3'].is_rpkg_installed(arpg_src_intros.robotpkg_mng_vars['ROBOTPKG_BASE'],arpg_src_intros.env)
arpg_src_intros.package_dict['pinocchio'].is_rpkg_installed(arpg_src_intros.robotpkg_mng_vars['ROBOTPKG_BASE'],arpg_src_intros.env)
arpg_src_intros.package_dict['talos-simulation'].is_rpkg_installed(arpg_src_intros.robotpkg_mng_vars['ROBOTPKG_BASE'],arpg_src_intros.env)

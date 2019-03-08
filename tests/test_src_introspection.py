#!/usr/bin/python3
from unittest import TestCase

from robotpkg_helpers import RobotpkgSrcIntrospection, build_test_rc_robotpkg_vars

robotpkg_vars = build_test_rc_robotpkg_vars()

arpg_src_intros = RobotpkgSrcIntrospection(robotpkg_vars['SRC'])
arpg_src_intros.display()
arpg_src_intros.save('rpg_src_intros.json')


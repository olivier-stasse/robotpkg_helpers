#!/usr/bin/python3

from robotpkg_helpers import RobotpkgGenerateDockerFile

add_robotpkg_mng_variables(robotpkg_vars)

CMakeLists_txt_path="/home/ostasse/devel-src/SoT/catkin_ws/src/roscontrol_sot/CMakeLists.txt"
arpg_gen_docker=RobotpkgGenerateDockerFile(CMakeLists_txt_path,robotpkg_vars['SRC'])
#arpg_gen_docker.build_docker()







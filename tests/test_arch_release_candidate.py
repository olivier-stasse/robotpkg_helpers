#!/usr/bin/python3
from robotpkg_helpers import RobotpkgArchitectureReleaseCandidate
from robotpkg_helpers import RobotpkgPkgReleaseCandidate

# Create a default architecture
a_rpkg_arch_rc = RobotpkgArchitectureReleaseCandidate()
a_rpkg_arch_rc.default_init()

# Populate with a release candidate
aRobotpkgPkgReleaseCandidate = \
    RobotpkgPkgReleaseCandidate(git_repo='https://github.com/stack-of-tasks/sot-core.git',
                                branch='devel',
                                name='sot-core')

a_rpkg_arch_rc.data['rc_pkgs']['sot-core']=aRobotpkgPkgReleaseCandidate.description

# Save it
a_rpkg_arch_rc.save_rc("/tmp/arch_test_rc.json")

# Read it from file
a_rpkg_arch_rc2 = RobotpkgArchitectureReleaseCandidate()
a_rpkg_arch_rc2.load_rc("/tmp/arch_test_rc.json")
a_rpkg_arch_rc2.display()

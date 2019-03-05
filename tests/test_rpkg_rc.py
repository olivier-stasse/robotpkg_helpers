#!/usr/bin/python3
from robotpkg_helpers import RobotpkgReleaseCandidate

git_repo='https://github.com/stack-of-tasks/sot-core.git'
commit='a5a8de4'
branch='devel'
tag='v4.1.0'

arpkgh_rc = RobotpkgReleaseCandidate(git_repo,commit,branch,tag)
arpkgh_rc.save('rpkgh_rc.json')

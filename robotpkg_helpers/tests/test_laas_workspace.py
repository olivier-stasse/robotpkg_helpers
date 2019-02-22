#!/usr/bin/python3
from robotpkg_helpers import RobotpkgLaasWorkspace

a_rpkg_laas_ws = RobotpkgLaasWorkspace()

a_rpkg_laas_ws.display_from_org('stack-of-tasks')
a_rpkg_laas_ws.reading_repos_from_github_for_sot()

import os
import sys
import json
from .package_release_candidate import RobotpkgPkgReleaseCandidate

class RobotpkgArchitectureReleaseCandidate:

    def __init__(self, json_filename=None):
        self.data={}
        self.data['ssh_git_openrobots']=False
        # Check if a JSON file has been provided
        if json_filename!=None:
            self.load_rc(json_filename)

    def default_init(self):
        if self.data['ssh_git_openrobots']:
            self.data['repo_robotpkg_main'] = \
                'https://git.openrobots.org/robots/robotpkg.git'
            self.data['repo_robotpkg_wip'] = \
                'ssh://git@git.openrobots.org/robots/robotpkg/robotpkg-wip'
        else:
            self.data['repo_robotpkg_main'] = \
                'https://git.openrobots.org/robots/robotpkg.git'
            self.data['repo_robotpkg_wip'] = \
                'https://git.openrobots.org/robots/robotpkg/robotpkg-wip.git'
        self.data['rc_pkgs']={}
        aRobotpkgPkgReleaseCandidate = \
            RobotpkgPkgReleaseCandidate(git_repo='https://github.com/stack-of-tasks/sot-core.git',
                                        branch='devel',
                                        name='sot-core')
        self.data['rc_pkgs']['sot-core']=aRobotpkgPkgReleaseCandidate.description
            
    def load_rc(self,filename):
        if os.path.is_file(filename):
            self.data = json.load(filename)
        else:
            print(filename + " does not exists")
        
    def save_rc(self,filename):
        f=open(filename,'w')
        json.dump(self.data,f)
        f.close()
        

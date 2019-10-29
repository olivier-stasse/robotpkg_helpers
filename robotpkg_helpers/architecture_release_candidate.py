import os
import sys
import json
from .package_release_candidate import RobotpkgPkgReleaseCandidate
from .package_release_candidate import display_description

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
        self.data['robotpkg_mng_root']='/integration_tests'
        self.data['ramfs_mnt_pt']='robotpkg-test-rc'
        self.data['arch_dist_files']='arch_distfiles'
        self.data['archives']='archives'

    def display(self):
        print("git url - robotpkg:")
        print("  "+self.data['repo_robotpkg_main'])
        print("git url - robotpkg wip:")
        print("  "+self.data['repo_robotpkg_wip'])
        for name,desc_package in self.data['rc_pkgs'].items():
            display_description(desc_package)
        # If the field targetpk exist then display the name of the package
        if 'targetpkg' in self.data:
            print("targetpkg:"+self.data['targetpkg'])
        # If the field targetpks exist then display all the packages
        if 'targetpkgs' in self.data:
            print("targetpkgs:")
            for target_name in self.data['targetpkgs']:
                print(target_name)

    def load_rc(self,filename):
        if os.path.isfile(filename):
            with open(filename) as json_filename:
                self.data = json.load(json_filename)
        else:
            print(filename + " does not exists")

    def save_rc(self,filename):
        f=open(filename,'w')
        json.dump(self.data,f)
        f.close()

    def search_for_connected_components(self,rpkg_src_introspection):
        """ This methods search the dependency of the package specified in
        'targetpkg' or 'targetpkgs' to find which package to build
        """
        list_of_target_pkg_name= {}
        if 'targetpkg' in self.data:
            list_of_target_pkg_name.appen(self.data['targetpkg'])
        if 'targetpkgs' in self.data:
            list_of_target_pkg_name.appen(self.data['targetpkgs'])

        for target_pkg_name in list_of_target_pkg_name:
            for pkg_dep in rpkg_src_introspection.package_dict[target_pkg_name].includes_depend:
                if pkg_dep in self.data['rc_pkgs'].keys():
                    self.data['rc_pkgs'][pkg_dep]['deg_con']= deg_con

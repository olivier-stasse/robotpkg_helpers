import os
import sys
import argparse
import json
from .package_release_candidate import RobotpkgPkgReleaseCandidate
from .package_release_candidate import display_description

class RobotpkgArchitectureReleaseCandidate:
    """ This class stores in a dictionnary how the deploymen structure
    is defined.

    """
    def __init__(self, json_filename=None):
        self.robotpkg_mng_vars={}
        self.robotpkg_mng_vars['ssh_git_openrobots']=False
        self.default_init()
        # Check if a JSON file has been provided
        if hasattr(self,'json_filename'):
            if json_filename!=None:
                self.load_rc(json_filename)

    def default_init(self):
        if self.robotpkg_mng_vars['ssh_git_openrobots']:
            self.robotpkg_mng_vars['repo_robotpkg_main'] = \
                'https://git.openrobots.org/robots/robotpkg.git'
            self.robotpkg_mng_vars['repo_robotpkg_wip'] = \
                'ssh://git@git.openrobots.org/robots/robotpkg/robotpkg-wip'
        else:
            self.robotpkg_mng_vars['repo_robotpkg_main'] = \
                'https://git.openrobots.org/robots/robotpkg.git'
            self.robotpkg_mng_vars['repo_robotpkg_wip'] = \
                'https://git.openrobots.org/robots/robotpkg/robotpkg-wip.git'
        self.robotpkg_mng_vars['rc_pkgs']={}
        self.robotpkg_mng_vars['robotpkg_mng_root']='/integration_tests'
        self.robotpkg_mng_vars['robotpkg_mng_base']='/integration_tests/robotpkg-test-rc/install'
        self.robotpkg_mng_vars['robotpkg_mng_src'] ='/integration_tests/robotpkg-test-rc/robotpkg'
        self.robotpkg_mng_vars['ramfs_mnt_pt']='robotpkg-test-rc'
        self.robotpkg_mng_vars['arch_dist_files']='arch_distfiles'
        self.robotpkg_mng_vars['archives']='archives'
        self.robotpkg_mng_vars['debug']='0'

    def handle_options(self):
        self.parser = argparse.ArgumentParser(
            description='Read options')

        self.parser.add_argument('json_filename', metavar="json_filename",
            action="store", nargs='+',
            help='Name of the json specifying the architecture to build')

        self.parser.add_argument("-m", "--ramfsmntpt",
            dest="ramfs_mnt_pt", action="store",
            default="robotpkg-test-rc",nargs=1,
            help='Subdirectory in ROBOTPKG_MNG_ROOT to compress \n' +
                '(default:robotpkg-test-rc)')

        self.parser.add_argument("-r", "--rpkgmngroot",
            dest="robotpkg_mng_root", action="store",
            default="/integration_tests", nargs=1,
            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n'+
                 '(default: /integration_tests)')

        self.parser.add_argument("-a", "--archdistfiles",
            dest='arch_dist_files', action='store',
            default='arch_disfiles',nargs=1,
            help='Subdirectory in ROBOTPKG_MNG_ROOT where tar balls\n'+
                 'of packages are stored\n (default: archives)')

        self.parser.add_argument("-v", "--verbosity",
            dest='verbosity', action='store',
            default='0',nargs=1,
            help='Level of verbosity\n (default: 0)')

        self.parser.parse_args(namespace=self)
        if hasattr(self,'ramfs_mnt_pt'):
            self.robotpkg_mng_vars['ramfs_mnt_pt']=self.ramfs_mnt_pt
        if hasattr(self,'robotpkg_mng_root'):
            self.robotpkg_mng_vars['robotpkg_mng_root']=self.robotpkg_mng_root
        if hasattr(self,'arch_distfiles'):
            self.robotpkg_mng_vars['arch_dist_files']=self.arch_distfiles
        if hasattr(self,'robotpkg_mng_src'):
            self.robotpkg_mng_vars['robotpkg_mng_src']=self.robotpkg_mng_src
        if hasattr(self,'robotpkg_mng_base'):
            self.robotpkg_mng_vars['robotpkg_mng_base']=self.robotpkg_mng_base
        if hasattr(self,'json_filename'):
            if os.path.isfile(self.json_filename[0]):
                self.load_rc(self.json_filename[0])
        if hasattr(self,'verbosity'):
            self.robotpkg_mng_vars['verbosity']=self.verbosity[0]

    def display(self):
        print("git url - robotpkg:")
        print("  "+self.robotpkg_mng_vars['repo_robotpkg_main'])
        print("git url - robotpkg wip:")
        print("  "+self.robotpkg_mng_vars['repo_robotpkg_wip'])
        for name,desc_package in self.robotpkg_mng_vars['rc_pkgs'].items():
            display_description(desc_package)
        # If the field targetpk exist then display the name of the package
        if 'targetpkg' in self.robotpkg_mng_vars:
            print("targetpkg:"+self.robotpkg_mng_vars['targetpkg'])
        # If the field targetpks exist then display all the packages
        if 'targetpkgs' in self.robotpkg_mng_vars:
            print("targetpkgs:")
            for target_name in self.robotpkg_mng_vars['targetpkgs']:
                print(target_name)
        print("robotpkg_mng_vars:")
        print(self.robotpkg_mng_vars)

    def load_rc(self,filename):
        if os.path.isfile(filename):
            with open(filename) as json_filename:
                self.data = json.load(json_filename)
                for ajsonkey,ajsonvalue in self.data.items():
                    self.robotpkg_mng_vars[ajsonkey] = ajsonvalue
        else:
            print(filename + " does not exists")

    def save_rc(self,filename):
        f=open(filename,'w')
        json.dump(self.robotpkg_mng_vars,f)
        f.close()

    def search_for_connected_components(self,rpkg_src_introspection):
        """ This methods search the dependency of the package specified in
        'targetpkg' or 'targetpkgs' to find which package to build
        """
        list_of_target_pkg_name= {}
        if 'targetpkg' in self.robotpkg_mng_vars:
            list_of_target_pkg_name.appen(self.robotpkg_mng_vars['targetpkg'])
        if 'targetpkgs' in self.robotpkg_mng_vars:
            list_of_target_pkg_name.appen(self.robotpkg_mng_vars['targetpkgs'])

        for target_pkg_name in list_of_target_pkg_name:
            for pkg_dep in rpkg_src_introspection.package_dict[target_pkg_name].includes_depend:
                if pkg_dep in self.robotpkg_mng_vars['rc_pkgs'].keys():
                    self.robotpkg_mng_vars['rc_pkgs'][pkg_dep]['deg_con']= deg_con

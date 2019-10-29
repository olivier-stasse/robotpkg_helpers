#!/usr/bin/python3
import os
import sys
import argparse
from robotpkg_helpers import RobotpkgTests,build_test_rc_robotpkg_vars
from robotpkg_helpers import HandlingImgs,RobotpkgArchitectureReleaseCandidate

class RpkghBuildArchReleaseCandidate:

    def __init__(self):

        self.RED =  '\033[0;31m'
        self.GREEN= '\033[0;32m'
        self.PURPLE='\033[0;35m'
        self.NC =   '\033[0m'

        self.handle_options()
        self.build_release_candidate()

    def build_release_candidate(self):

        # Load the arch distribution file.
        anArchitectureReleaseCandidate = RobotpkgArchitectureReleaseCandidate()
        if self.json_filename!=None:
            if os.path.isfile(self.json_filename[0]):
                anArchitectureReleaseCandidate.load_rc(self.json_filename[0])
            else:
                print('File '+self.json_filename[0]+' does not exists.')
                sys.exit(-1)

        # Reading rpkg_mng_root
        # On line command has priority
        if not hasattr(self,'robotpkg_mnt_root'):
            # over file
            if 'robotpkg_mng_root' in anArchitectureReleaseCandidate.data.keys():
                self.rpkgmngroot = anArchitectureReleaseCandidate.data['robotpkg_mng_root']

        # Reading ramfsmntpot
        # On line command has priority
        if not hasattr(self,'ramfsmntpt'):
            if 'ramfs_mnt_pt' in anArchitectureReleaseCandidate.data.keys():
                self.sub_ramfsmntpt = anArchitectureReleaseCandidate.data['ramfs_mnt_pt']

        # Reading verbosity
        # Define the debug level
        if not hasattr(self,'verbosity'):
            if 'verbosity' in anArchitectureReleaseCandidate.data.keys():
                self.verbosity = anArchitectureReleaseCandidate.data['verbosity']

        # Reading arch_dist_files
        # On line commans has priority
        if not hasattr(self,'arch_dist_files'):
            if 'arch_dist_files' in anArchitectureReleaseCandidate.data.keys():
                self.arch_dist_files = anArchitectureReleaseCandidate.data['arch_dist_files']
            else:
                print("No arch_dist_files in json file")

        aHandlingImg = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot,
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt,
            sub_arch_dist_files = self.arch_dist_files,
            debug=int(self.verbosity[0])
        )

        # Perform the deployment in arpgtestrc
        arpgtestrc = \
            RobotpkgTests(aHandlingImg.robotpkg_mng_vars['ROBOTPKG_ROOT'],
                          debug=int(self.verbosity[0]))
        if arpgtestrc.perform_test_rc(arch_release_candidates=anArchitectureReleaseCandidate):
            # If it worked then compile the package specified in targetpkg
            if 'targetpkg' in anArchitectureReleaseCandidate.data:
                # Test if this is a list or not
                if isinstance(anArchitectureReleaseCandidate.data['targetpkg'],str) :
                    arpgtestrc.compile_package(anArchitectureReleaseCandidate.data['targetpkg'])
                else:
                    print(self.RED + "ERROR: In json file targetpkg is not a string" + self.NC)
                    if isinstance(anArchitectureReleaseCandidate.data['targetpkg'],list) :
                        print(self.RED + "use targetpkgs instead" + self.NC)
            else:
                # If we have a list of package to compile
                if 'targetpkgs' in anArchitectureReleaseCandidate.data:
                    for pkg_name in anArchitectureReleaseCandidate.data['targetpkgs']:
                        arpgtestrc.compile_package(pkg_name)

        else:
            print("Wrong handling of packages")

    def handle_options(self):
        parser = argparse.ArgumentParser(
            description='Build an integration tests from filename.')
        parser.add_argument('json_filename', metavar="json_filename",
            action="store", nargs='+',
            help='Name of the json specifying the architecture to build')

        parser.add_argument("-m", "--ramfsmntpt",
            dest="sub_ramfsmntpt", action="store",
            default="robotpkg-test-rc",nargs=1,
            help='Subdirectory in ROBOTPKG_MNG_ROOT to compress \n' +
                '(default:robotpkg-test-rc)')

        parser.add_argument("-r", "--rpkgmngroot", dest="rpkgmngroot", action="store",
                            default="/integration_tests", nargs=1,
                            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n(default: /integration_tests)')

        parser.add_argument("-a", "--archdistfiles", dest='sub_arch_dist_files', action='store',
                            default='arch_disfiles',nargs=1,
                            help='Subdirectory in ROBOTPKG_MNG_ROOT where tar balls of packages are stored\n (default: archives)')

        parser.add_argument("-t", "--targetpkg", dest='targetpkg', action='store',
                            default='talos-dev',nargs=1,
                            help='Package to compile\n (default: talos-dev)')

        parser.add_argument("-v", "--verbosity", dest='verbosity', action='store',
                            default='0',nargs=1,
                            help='Level of verbosity\n (default: 0)')

        parser.parse_args(namespace=self)

if __name__ == "__main__":
    arpkgh_build_arch_rc = RpkghBuildArchReleaseCandidate()

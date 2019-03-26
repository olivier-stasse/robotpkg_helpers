#!/usr/bin/python3
import os
import sys
from robotpkg_helpers import HandlingImgs

class RpkghCleanIntegrationDirs:

    def __init__(self):
        self.handle_options()
        self.build_release_candidate()

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

        parser.parse_args(namespace=self)

    def clean_integration_directory():
        aHandlingImgs = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot,
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt,
            sub_archives=self.sub_archives)

        aHandlingImgs.clean_integration_directory()


if __name__ == "__main__":
    clean_integration_directory()

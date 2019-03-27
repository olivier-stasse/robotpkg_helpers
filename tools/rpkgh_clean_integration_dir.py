#!/usr/bin/python3
import os
import sys
from robotpkg_helpers import HandlingImgs
import argparse

class RpkghCleanIntegrationDirs:

    def __init__(self):
        self.handle_options()
        self.clean_integration_directory()

    def handle_options(self):
        parser = argparse.ArgumentParser(
            description='Build an integration tests from filename.')

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

    def clean_integration_directory(self):
        aHandlingImgs = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot,
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt)

        aHandlingImgs.clean_integration_directory()


if __name__ == "__main__":
    arpkgh_clean_integ_dirs = RpkghCleanIntegrationDirs()

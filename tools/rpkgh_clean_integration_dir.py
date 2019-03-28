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


        parser.parse_args(namespace=self)

        if isinstance(self.sub_ramfsmntpt,list):
            self.sub_ramfsmntpt=self.sub_ramfsmntpt[0]

        if isinstance(self.rpkgmngroot,list):
            self.rpkgmngroot=self.rpkgmngroot[0]

    def clean_integration_directory(self):
        aHandlingImgs = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot,
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt)

        aHandlingImgs.clean_integration_directory()


if __name__ == "__main__":
    arpkgh_clean_integ_dirs = RpkghCleanIntegrationDirs()

#!/usr/bin/python3
import os
import argparse
from robotpkg_helpers import HandlingImgs

class RpkghCreateRamfsDir():

    def __init__(self):
        self.handle_options()
        self.create_ramfs_dir()
        

    def handle_options(self):
        parser = argparse.ArgumentParser(description='Create a ramfs mounting point (default: /integration_tests/robotpkg-test-rc)')

        parser.add_argument("-m", "--ramfsmntpt", dest="sub_ramfsmntpt", action="store",
                            default="robotpkg-test-rc",nargs=1,
                            help='Subdirectory in ROBOTPKG_MNG_ROOT to compress \n(default:robotpkg-test-rc)')

        parser.add_argument("-r", "--rpkgmngroot", dest="rpkgmngroot", action="store",
                            default="/integration_tests", nargs=1,
                            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n(default: /integration_tests)')

        parser.parse_args(namespace=self)

    def create_ramfs_dir(self):
        aHandlingImgs = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot[0],
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt[0])

        aHandlingImgs.create_ramfs_dir()


if __name__ == "__main__":
    aRpkghCreateRamfsDir = RpkghCreateRamfsDir()


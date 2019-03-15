#!/usr/bin/env python3
import os
import sys
from robotpkg_helpers import HandlingImgs
import argparse

class RpkghRestoreDir():

    def __init__(self):
        self.handle_options()
        print(self.filename[0])
        self.restore_dir(self.filename[0])

    def handle_options(self):
        parser = argparse.ArgumentParser(description='Restore an install/robotpkg directory.')
        parser.add_argument('filename', metavar="filename",
                            action="store", nargs=1,
                            help='File to uncompress')

        parser.add_argument("-m", "--ramfsmntpt", dest="sub_ramfsmntpt", action="store",
                            default="robotpkg-test-rc",nargs='?',
                            help='Subdirectory in ROBOTPKG_MNG_ROOT where to uncompress ')

        parser.add_argument("-r", "--rpkgmngroot", dest="rpkgmngroot", action="store",
                            default="/integration_tests", nargs='?',
                            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n(default: /integration_tests)')

        parser.add_argument("-a", "--archives", dest='sub_archives', action='store',
                            default='archives',nargs='?',
                            help='Subdirectory in ROBOTPKG_MNG_ROOT where archives are stored')

        parser.parse_args(namespace=self)

    def restore_dir(self,filename):
        aHandlingImgs = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot,
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt,
            sub_archives=self.sub_archives)

        aHandlingImgs.restore_from_backup_dir(tar_file_name=filename)

if __name__ == "__main__":
    aRpkghRestoreDir = RpkghRestoreDir()

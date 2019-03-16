#!/usr/bin/python3
import os
import argparse

from robotpkg_helpers import HandlingImgs

class RpkghSaveIntegration():

    def __init__(self):
        self.handle_options()
        defaultName= True
        if hasattr(self,'filename'):
            if self.filename!=None:
                self.save_integration(self.filename[0])
                defaultName=False
        if defaultName:
            self.save_integration()
        

    def handle_options(self):
        parser = argparse.ArgumentParser(description='Save an install/robotpkg directory.')
        parser.add_argument('filename', metavar="filename",
                            action="store", nargs='?',
                            help='Name of the archive to build')

        parser.add_argument("-m", "--ramfsmntpt", dest="sub_ramfsmntpt", action="store",
                            default="robotpkg-test-rc",nargs=1,
                            help='Subdirectory in ROBOTPKG_MNG_ROOT to compress \n(default:robotpkg-test-rc)')

        parser.add_argument("-r", "--rpkgmngroot", dest="rpkgmngroot", action="store",
                            default="/integration_tests", nargs=1,
                            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n(default: /integration_tests)')

        parser.add_argument("-a", "--archives", dest='sub_archives', action='store',
                            default='archives',nargs=1,
                            help='Subdirectory in ROBOTPKG_MNG_ROOT where archives are stored\n (default: archives)')

        parser.parse_args(namespace=self)

    def save_integration(self,filename=None):
        aHandlingImgs = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot,
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt,
            sub_archives=self.sub_archives)

        aHandlingImgs.backup_rpkg_dir(tar_file_name=filename)

if __name__ == "__main__":
    aRpkghSaveIntegration = RpkghSaveIntegration()


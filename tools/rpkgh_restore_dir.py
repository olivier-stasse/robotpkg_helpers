#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import argcomplete, argparse
from pathlib import Path

from robotpkg_helpers import HandlingImgs

class TestCompleter(object):
    def __init__(self,choices):
        self.choices = choices

    def __call__(self, parsed_args, **kwargs):
        argcomplete.warn("toto")
        argcomplete.warn(parsed_args)
        argcomplete.warn(self.choices)
        return self.choices

class FilenameCompleter(object):
    def __init__(self):
        argcomplete.warn("FilenameCompleter: init")
        p = Path('/integration_tests/archives2/')
        list_tgz = list(p.glob('**/*.tgz'))
        list_tgz=sorted(list_tgz)
        self.choices = list_tgz
        
    def __call__(self, parsed_args, **kwargs):
        lstr = parsed_args.rpkgmngroot+'/'+ parsed_args.sub_archives
        p = Path(lstr)
        list_tgz = list(p.glob('**/*.tgz'))
        list_tgz=sorted(list_tgz)
        final_choices=[]
        for atgz in list_tgz:
            final_choices.append(atgz.name)
        return final_choices
                
    
class RamfsmntptCompleter(object):

    def __init__(self,choices):
        argcomplete.warn('RamfsmntptCompleter:init')
        self.choices = choices
        
    def __call__(self, parsed_args, **kwargs):
        argcomplete.warn("going through call")
        # p = Path(parser_args.rpkgmngroot+'/')
        # argcomplete.warn(p)
        # self.choices=['test','test2']        
        # for child in p.iterdir():
        #     self.choices.append(child)
        #     argcomplete.warn(child)
        return self.choices

class DirrpkgmngrootCompleter(object):

    def __init__(self):
        argcomplete.warn("DirrpkgmngrootCompleter")
        
    def __call__(self, parsed_args, **kwargs):
        #argcomplete.warn("DirrpkgmngrootCompleter")
        lstr=parsed_args.rpkgmngroot+'/'
        #argcomplete.warn(lstr)
        choices=[]
        p = Path(lstr)
        for x in p.iterdir():
            #argcomplete.warn(str(x))
            if x.is_dir():
                choices.append(x.name)
        return choices
    
# print(parsed_args)
# argcomplete.warn("toto")
# return "test"

class RpkghRestoreDir():

    def __init__(self):
        self.handle_options()
        print(self.filename[0])
        self.restore_dir(self.filename[0])

    def handle_options(self):
        parser = argparse.ArgumentParser(description='Restore an install/robotpkg directory.')

        parser.add_argument('filename',
                            metavar="filename",
                            action="store", nargs=1,
                            help='File to uncompress'
        ).completer = FilenameCompleter()

        parser.add_argument("-m", "--ramfsmntpt", dest="sub_ramfsmntpt", action="store",
                             default="robotpkg-test-rc",nargs=1,
                            help='Subdirectory in ROBOTPKG_MNG_ROOT where to uncompress \n(default:robotpkg-test-rc)'
        ).completer = TestCompleter(('robotpkg-test-rc','RR'))
        
        parser.add_argument("-r", "--rpkgmngroot", dest="rpkgmngroot", action="store",
                            default="/integration_tests", nargs=1,
                            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n(default: /integration_tests)'
        ).completer = TestCompleter(('toto','tata'))

        parser.add_argument("-a", "--archives", dest='sub_archives', action='store',
                            default='archives',nargs=1,
                            help='Subdirectory in ROBOTPKG_MNG_ROOT where archives are stored\n (default: archives)'
        ).completer = DirrpkgmngrootCompleter()

        argcomplete.autocomplete(parser)
        parser.parse_args(namespace=self)
        
        if isinstance(self.sub_ramfsmntpt,list):
            self.sub_ramfsmntpt=self.sub_ramfsmntpt[0]

        if isinstance(self.rpkgmngroot,list):
            self.rpkgmngroot=self.rpkgmngroot[0]

        if isinstance(self.sub_archives,list):
            self.sub_archives=self.sub_archives[0]

    def restore_dir(self,filename):
        aHandlingImgs = HandlingImgs(
            ROBOTPKG_MNG_ROOT=self.rpkgmngroot,
            sub_ramfs_mnt_pt=self.sub_ramfsmntpt,
            sub_archives=self.sub_archives)

        aHandlingImgs.restore_from_backup_dir(tar_file_name=filename)


if __name__ == "__main__":
        
    aRpkghRestoreDir = RpkghRestoreDir()
    


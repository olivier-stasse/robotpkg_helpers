#!/usr/bin/python3
import os
import argparse
from robotpkg_helpers import RobotpkgSrcIntrospection

class RpkghAnalyzeOrganization:

    def __init__(self):
        self.handle_options()
        self.analyze_organization()
        
    def analyze_organization(self):
        # Reading rpkg_mng_root
        # On line command has priority
        ROBOTPKG_ROOT_SRC=self.rpkgmngroot+'/'+self.sub_ramfsmntpt+'/robotpkg'
        arpkg_src_intro = RobotpkgSrcIntrospection(ROBOTPKG_ROOT_SRC)

        org_pkgs = arpkg_src_intro.provides_org_version(self.organization_name[0])
        print(str(len(org_pkgs)))
        for a_pack,a_value in sorted(org_pkgs.items()):
            print(str(a_pack)+':'+str(a_value))

    def handle_options(self):
        parser = argparse.ArgumentParser(
            description='Inspect packages in robotpkg folder and provide the list of packages related to a specific organization.')
        
        parser.add_argument('organization_name', metavar="organization_name",
            action="store", nargs='+',
            help='Name of the organization providing packages in robotpkg')

        parser.add_argument("-m", "--ramfsmntpt",
            dest="sub_ramfsmntpt", action="store",
            default="robotpkg-test-rc",nargs=1,
            help='Subdirectory in ROBOTPKG_MNG_ROOT to inspect \n' +
                '(default:robotpkg-test-rc)')

        parser.add_argument("-r", "--rpkgmngroot", dest="rpkgmngroot",
                            action="store",
                            default="/integration_tests", nargs=1,
                            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n(default: /integration_tests)')


        parser.parse_args(namespace=self)
        
        if isinstance(self.sub_ramfsmntpt,list):
            self.sub_ramfsmntpt=self.sub_ramfsmntpt[0]

        if isinstance(self.rpkgmngroot,list):
            self.rpkgmngroot=self.rpkgmngroot[0]

        
if __name__ == "__main__":
    arpkgh_analyze_org = RpkghAnalyzeOrganization()


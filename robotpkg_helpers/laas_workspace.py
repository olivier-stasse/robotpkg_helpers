# Author: O. Stasse
# See LICENSE.txt in root
# Copyright CNRS

import os
import re
from .src_introspection import add_robotpkg_src_introspection

class RobotpkgLaasWorkspace:
    """ This class creates a Laas workspace environment to have repositories
    readily available on the computer for development.

    None specified repos are installed directly from robotpkg.
    Packages specified are clone and set inside the src directory.
    """
    
    def __init__(self,root_dir=None,ROBOTPKG_ROOT=None):
        if root_dir==None:
            env_vars=os.environ.copy()
            self.root_laas_ws=env_vars["HOME"]+'/laas_ws'
            self.user=env_vars["USER"]

        # Add ROBOTPKG_ROOT, ROBOTPKG_ROOT_SRC and robotpkg_src_intro to self
        add_robotpkg_src_introspection(self,ROBOTPKG_ROOT)
            
        
    def create_main_dir(self):
        """ Method to create a directory structure to store repositories
        and compiled environment

        laas_ws is the whole directory
        src is the place to store repositories
        install is the place to install and test the software.
        """

        set_of_dirs= [ self.root_laas_ws,
                       self.root_laas_ws+'/src',
                       self.root_laas_ws+'/install']
        
        # Creates set_of_dirs if they do not exist
        for a_dir in list_of_dirs:
            if not os.path(a_dir).is_dir():
                os.makedirs(a_dir,0o777,True)

    def display_from_org(self,org_name):
        for key,package in self.robotpkg_src_intro.package_dict.items():
            if hasattr(package,'org_name'):
                if not len(package.org_name)==0:
                    if package.org_name[0]==org_name:
                        print(package.name+':'+package.org_name[0])
            

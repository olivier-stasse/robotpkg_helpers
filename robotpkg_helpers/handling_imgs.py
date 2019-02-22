# Author: O. Stasse
# See LICENSE.txt in root
# Copyright CNRS

import os

from  .utils import execute,execute_call
from .src_introspection import add_robotpkg_variables

def add_robotpkg_mng_variables(anObject, ROBOTPKG_MNG_ROOT=None):
    """ This function adds robotpkg_mng_vars to the object based on ROBOTPKG_MNG_ROOT
    if provided.

    It creates a directory where the RobotpkgTests class can be deployed
    It stores distfiles which can reused for subsequent test of robotpkgs.
    It stores tar file of robotpkg for specific configuration.

    All of this is done for intermediate build when working on release candidates
    and speed up deployment tests.
    
    TODO: Test over a solution an integrative solution with dockerfile and 
    intermediate binary build.
    """
    if ROBOTPKG_MNG_ROOT==None:
        anObject.ROBOTPKG_MNG_ROOT='/integration_tests'
    else:
        anObject.ROBOTPKG_MNG_ROOT=ROBOTPKG_MNG_ROOT
        
    anObject.robotpkg_mng_vars={}
    anObject.robotpkg_mng_vars['ROOT'] = anObject.ROBOTPKG_MNG_ROOT
    anObject.robotpkg_mng_vars['ARCH_DISTFILES']=robotpkg_mng_vars['ROOT']+'/arch_distfiles'
    anObject.robotpkg_mng_vars['RAMFS_MNT_PT']=robotpkg_mng_vars['ROOT']+'/robotpkg-test-rc'
    anObject.robotpkg_mng_vars['ARCHIVES']=robotpkg_mng_vars['ROOT']+'/archives'

class HandlingImgs:
    """ The main idea of this class is to handle the backup of directories
    which contains specific build point of robotpkg.

    The main idea is to keep part which are static in tar ball.
    Deploy them when restarting integration tests in a ramdisk.

    Caution: you may lose data if you do not decouple your source code
    and the one deployed for integration test.
    """
    
    def __init__(self,ramfs_dir=None,ROBOTPKG_ROOT=None,debug=0):
        
        # Populate the object with field ROBOTPKG_ROOT
        add_robotpkg_variables(self,ROBOTPKG_ROOT)

        # Copy the environment variables
        self.env = os.environ.copy()

        # Initialize ramfs_dir
        self.ramfs_dir=ramfs_dir

        # Debug level
        self.debug=debug

    def create_ramfs_dir(self):
        """ If the ramfs dir does not exist create it
        """
        if not os.path.isdir(self.ramfs_dir):
            os.makedirs(self.ramfs_dir,0o777,True)
            
        bashCmd="mount -t tmpfs -o size=4096m new_ram_disk "+self.ramfs_dir
        execute(bashCmd,self.env,self.debug)

    def backup_dir(self,backup_dir):
        """ Backup the build directory in a specific backup directory
        """
        basenamedir=os.path.basename(self.ROBOTPKG_ROOT)
        bashCmd="tar -czvf "+backup_dir+"/"++ ".tgz " + self.ROBOTPKG_ROOT;
        execute(bashCmd,self.env,self.debug)

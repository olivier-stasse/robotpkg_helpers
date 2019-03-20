# Author: O. Stasse
# See LICENSE.txt in root
# Copyright CNRS

import os
import datetime

from .utils import execute,execute_call,add_robotpkg_mng_variables
from .utils import init_environment_variables,execute_capture_output

from .src_introspection import add_robotpkg_variables


class HandlingImgs:
    """ The main idea of this class is to handle the backup of directories
    which contains specific build point of robotpkg and deploy it in a subdirectory.
    This subdirectory can be mounted on a ramfs when appropriate.

    First idea: Maintain a coherent deployment structure handling tar ball,
    source code and binaries
    Second idea: handling parts which are static in tar balls.
    Thrid idea: Deploy them when restarting integration tests in a ramdisk.

    Caution: When using a ramdisk you may lose data if you do not decouple your source code
    and the one deployed for integration test.
    ramfs_dir :          Full path to ramfs_dir (default: None)
    ROBOTPKG_MNG_ROOT:   Full path to the root integration directory
                         (default: '/integration_tests')
    sub_ramfs_mnt_pt:    Subdirectory inside ROBOTPKG_MNT_ROOT
                         (default: 'robotpkg-test-rc')
    sub_arch_dist_files: Subdirectory where to store packages releases
                         (default: 'arch_distfiles')
    archives:            Subdirectory where to store install/robotpkg sub directories
                         (default: 'archives')
    """

    def __init__(self,
                 ramfs_dir=None,
                 ROBOTPKG_MNG_ROOT='/integration_tests',debug=0,
                 sub_ramfs_mnt_pt='robotpkg-test-rc',
                 sub_arch_dist_files='arch_distfiles',
                 sub_archives='archives'):

        self.RED =  '\033[0;31m'
        self.GREEN= '\033[0;32m'
        self.PURPLE='\033[0;35m'
        self.NC =   '\033[0m'

        if ramfs_dir==None:
            ramfs_dir=ROBOTPKG_MNG_ROOT+'/'+sub_ramfs_mnt_pt

        # Initialize ramfs_dir
        self.ramfs_dir=ramfs_dir

        # Populate the object with management field
        add_robotpkg_mng_variables(self,
                                   ROBOTPKG_MNG_ROOT=ROBOTPKG_MNG_ROOT,
                                   sub_ramfs_mnt_pt=sub_ramfs_mnt_pt,
                                   sub_arch_dist_files = sub_arch_dist_files,
                                   sub_archives = sub_archives )

        # Populate the object with field ROBOTPKG_ROOT
        add_robotpkg_variables(self,
                               ROBOTPKG_ROOT=self.robotpkg_mng_vars['ROBOTPKG_ROOT'])

        # Populate the object with the robotpkg environment variables
        init_environment_variables(self,self.robotpkg_mng_vars['ROBOTPKG_ROOT'])

        # Extract the user name even in case of sudo
        self.user_name = self.extract_user_name()

        # Extract the user name even in case of sudo
        self.group_name = self.extract_group_name()

        # Debug level
        self.debug=debug


    def checking_rams_fs_mnt_pt_dir(self):
        # If directory where we are suppose to install everything
        # is empty then return True, because the link must be created.
        ramfs_mnt_pt = self.robotpkg_mng_vars['RAMFS_MNT_PT']
        if os.path.exists(ramfs_mnt_pt) and os.path.isdir(ramfs_mnt_pt):
            if not os.listdir(ramfs_mnt_pt):
                if not os.path.islink(ramfs_mnt_pt):
                    os.rmdir(self.robotpkg_mng_vars['RAMFS_MNT_PT'])
                else:
                    return False
            else:
                print("WARNING !\n"+ramfs_mnt_pt+ " is not empty")
                print("Cannot mount ramfs")
                return False
        return True

    def create_ramfs_dir(self):
        """ If the ramfs dir does not exist then creates it
        NOTE: Launching this method requires to have sudo access.
        """
        print("create_ramfs_dir :"+self.ramfs_dir)

        # Test if the mount point exits and creates it if not
        if not os.path.isdir(self.ramfs_dir):
            print("Directory "+self.ramfs_dir+" does not exists.")
            os.makedirs(self.ramfs_dir,0o777,True)
            print("Directory "+self.ramfs_dir+" created.")

        # Mount RAMS FS at the ramfs dir if it does not already exists
        if not os.path.ismount(self.ramfs_dir):
            bashCmd="mount -t tmpfs -o size=4096m new_ram_disk "+self.ramfs_dir
            outputdata,error = execute(bashCmd,self.env,self.debug)
            if outputdata!=None:
                for stdout_line in outputdata.splitlines():
                    str_cmp = stdout_line.decode('utf-8')
                    print(stdout_line)
            if error!=None:
                for stderr_line in error.splitlines():
                    str_cmp = stderr_line.decode('utf-8')
                    print(self.RED+"ERR:"+str_cmp+self.NC)
        else:
            print(self.ramfs_dir + " already mounted")

        # checking the ram FS mounting point directory
        bashCmd="chown "+ self.user_name + '.' + \
            self.group_name + ' ' + self.ramfs_dir+ " "
        outputdata,error = execute(bashCmd,self.env,self.debug)


    def prepare_mng_dirs(self):
        """ Create the directories for managing integration tests
        New behavior do not create ramfs by default.
        This should be done by the user using
        rpkgh_create_ramfs.py
        """

        # First step: check that all directories exists
        lmng_dirs=['ROOT','ARCH_DISTFILES','ARCHIVES']
        for amng_dir in lmng_dirs:
            mng_dir_name = self.robotpkg_mng_vars[amng_dir]
            print("Test: "+mng_dir_name)
            if not os.path.isdir(mng_dir_name):
                os.makedirs(mng_dir_name,0o777,True)


    def build_tar_file_name(self,backup_dir):
        """ Build the name of the tar ball according to the following pattern:
        robotpkg_year_month_day_hours_seconds.tgz
        """
        # Build name of the tar ball.
        current_date = datetime.datetime.now()
        str_cur_date = current_date.strftime("%Y_%m_%d")
        str_cur_time = current_date.strftime("%H_%M")
        tar_file_name = backup_dir+"/robotpkg_"+ \
                        str_cur_date +'_'+ \
                        str_cur_time + \
                        ".tgz "
        return tar_file_name

    def build_description_file(self,tar_file_name,backup_dir=None):
        """ Build a file to describe the contains of the tar file.
        """
        if backup_dir==None:
            backup_dir = self.robotpkg_mng_vars['ARCHIVES']

        str_base_name = os.path.basename(tar_file_name)
        str_base_name_root,str_base_name_ext = os.path.splitext(str_base_name)
        description_file_name = backup_dir+ '/' + str_base_name_root +'.txt'

        bashCmd=self.robotpkg_mng_vars['ROBOTPKG_BASE']+ \
           "/sbin/robotpkg_info "
        print(bashCmd)
        execute_capture_output(bashCmd,description_file_name,self.env,self.debug)

    def backup_rpkg_dir(self,backup_dir=None,tar_file_name=None):
        """ Backup the build directory in a specific backup directory
        """
        # Storing the current path
        current_path=os.getcwd()

        if backup_dir==None:
            backup_dir = self.robotpkg_mng_vars['ARCHIVES']

        if tar_file_name==None:
            tar_file_name = self.build_tar_file_name(backup_dir)

        # Getting the name of the root directory
        basename_rpkg_root_dir=os.path.basename(self.ROBOTPKG_ROOT)

        bashCmd="tar -czf "+ tar_file_name + ' ' + basename_rpkg_root_dir
        print(bashCmd)

        # Going inside ROBOTPKG_MNG_ROOT
        os.chdir(self.ROBOTPKG_MNG_ROOT)

        # Creating the tarball.
        execute(bashCmd,self.env,self.debug)

        # Save description file
        self.build_description_file(tar_file_name)

        # Going back to where we were
        os.chdir(current_path)

    def restore_from_backup_dir(self,backup_dir=None,tar_file_name=None):
        """ Restore integration directory from a backup file
        """
        # Storing the current path
        current_path=os.getcwd()

        if backup_dir==None:
            backup_dir = self.robotpkg_mng_vars['ARCHIVES']

        if tar_file_name==None:
            print("You should specified the tar_file_name")
            return

        # Going inside ROBOTPKG_MNG_ROOT
        os.chdir(self.ROBOTPKG_MNG_ROOT)
        print("Going into "+self.ROBOTPKG_MNG_ROOT)

        # Extracting from the tarball.
        bashCmd="tar -xzvf "+ backup_dir+'/'+tar_file_name +\
            ' --directory ' + self.robotpkg_mng_vars['ROOT']
        print("Executing :\n"+bashCmd)
        outputdata,error = execute(bashCmd,self.env,self.debug)
        if error!=None:
            firstLine= True
            for stdout_line in error.splitlines():
                if firstLine:
                    print(self.RED+"Error:")
                    firstLine= False
                print(self.RED+stdout_line.decode('utf-8')+self.NC)

        if outputdata!=None:
            for stdout_line in outputdata.splitlines():
                print(stdout_line.decode('utf-8'))

        # Going back to where we were
        os.chdir(current_path)

    def extract_user_name(self):
        """ Extraction the username
        This creates the field user_name
        """
        bashCmd="logname"
        output_data,error=execute(bashCmd,self.env,debug=0)
        nb_line=0
        for stdout_line in output_data.splitlines():
            if nb_line==0:
                user_name=stdout_line.decode('utf-8')
                break
            nb_line=nb_line+1

        return user_name

    def extract_group_name(self):
        """ Extraction the main group of the user
        This creates the field group_name
        """
        if not hasattr(self,'user_name'):
            self.extract_user_name()
        else:
            if self.user_name==None:
                self.extract_user_name()

        bashCmd="groups "+self.user_name
        output_data,error =execute(bashCmd,self.env,debug=0)

        group_name=''
        nb_line=0
        for stdout_line in output_data.splitlines():
            if nb_line==0:
                group_names=stdout_line.decode('utf-8').split(' ')
                # First and second fields are:
                # ['username'.':']
                group_name=group_names[2]
                break
            nb_line=nb_line+1

        return group_name

    def clean_integration_directory(self):
        """ Remove the contains of ROBOTPKG_ROOT/robotpkg-test-rc
        """
        # Storing the current path
        current_path=os.getcwd()

        # Going inside ROBOTPKG_MNG_ROOT
        os.chdir(self.robotpkg_mng_vars['ROBOTPKG_ROOT'])

        print(os.getcwd())
        bashCmd="rm -rf robotpkg"
        print(bashCmd)
        res=input('Execute ? [y/n]')
        if res=='y':
            output_data=execute(bashCmd,self.env,debug=0)

        bashCmd="rm -rf install"
        print(bashCmd)
        res=input('Execute ? [y/n]')
        if res=='y':
            output_data=execute(bashCmd,self.env,debug=0)

        # Going back to where we were
        os.chdir(current_path)

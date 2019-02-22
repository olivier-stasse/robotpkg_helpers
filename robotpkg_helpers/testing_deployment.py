#!/usr/bin/python3
import os
import sys
from pathlib import Path
import socket

from .utils import execute, execute_call
from .src_introspection import RobotpkgPackage,RobotpkgSrcIntrospection
from .src_introspection import add_robotpkg_variables,add_robotpkg_src_introspection

class RobotpkgTests:

    def __init__(self,ROBOTPKG_ROOT=None,debug=5):
        """ Install and compile a robotpkg infrastructure

        Arguments:
        ROBOTPKG_ROOT: The directory where the whole robotpkg install takes place.
        debug: debug level
        """

        # Add ROBOTPKG_ROOT, ROBOTPKG_ROOT_SRC to self
        add_robotpkg_variables(self,ROBOTPKG_ROOT)
        if not hasattr(self,'ROBOTPKG_ROOT_SRC'):
            print('add_robotpkg_variables is not doing what it is suppose to be doing\n')
            sys.exit()
            
        self.init_colors()
        # Prepare the environment variables to compile with robotpkg 
        self.init_environment_variables(self.ROBOTPKG_ROOT)
        # Prepare the robotpkg.conf
        self.init_robotpkg_conf_add()

        self.debug = debug
        self.ssh_git_openrobots = False
        
    def init_colors(self):
        """ Initialize colors for beautification
        
        The following variables are available: 
        REG, GREEN, PURPLE, NC (no color)
        """
        self.RED =  '\033[0;31m'
        self.GREEN= '\033[0;32m'
        self.PURPLE='\033[0;35m'
        self.NC =   '\033[0m'

    def execute(self,bashCommand):
        return execute(bashCommand,self.env,self.debug)

    def execute_call(self,bashCommand):
        return execute_call(bashCommand,self.debug)
        
    def init_environment_variables(self, ROBOTPKG_ROOT):
        """Prepare the environment variables.
        
        Specifies the environment when starting bash commands
        """
        self.ROBOTPKG_ROOT = ROBOTPKG_ROOT
        self.env = os.environ.copy()
        ROBOTPKG_BASE = self.ROBOTPKG_ROOT+'/install'
        self.env["ROBOTPKG_BASE"] = ROBOTPKG_BASE
        # Imposes bash as the shell
        self.env["SHELL"] = "/usr/bin/bash"
        # For binaries
        self.env["PATH"] = ROBOTPKG_BASE+'/sbin:' + \
            ROBOTPKG_BASE+'/bin:'+self.env["PATH"]
        
        # For libraries
        prev_LD_LIBRARY_PATH=''
        if "LD_LIBRARY_PATH" in self.env:
            prev_LD_LIBRARY_PATH = self.env["LD_LIBRARY_PATH"]
        self.env["LD_LIBRARY_PATH"] = ROBOTPKG_BASE+'/lib:' \
            +ROBOTPKG_BASE+'/lib/plugin:' \
            +ROBOTPKG_BASE+'/lib64:' \
            +prev_LD_LIBRARY_PATH
        
        # For python
        prev_PYTHON_PATH=''
        if "PYTHON_PATH" in self.env:
            prev_PYTHON_PATH = self.env["PYTHON_PATH"]
        self.env["PYTHON_PATH"]=ROBOTPKG_BASE+'/lib/python2.7/site-packages:' \
            +ROBOTPKG_BASE+'/lib/python2.7/dist-packages:' \
            +prev_PYTHON_PATH
        
        # For pkgconfig
        prev_PKG_CONFIG_PATH=''
        if "PKG_CONFIG_PATH" in self.env:
            prev_PKG_CONFIG_PATH = self.env["PKG_CONFIG_PATH"]

        self.env["PKG_CONFIG_PATH"]=ROBOTPKG_BASE+'/lib/pkgconfig:' \
            +prev_PKG_CONFIG_PATH
        
        # For ros packages
        prev_ROS_PACKAGE_PATH=''
        if "ROS_PACKAGE_PATH" in self.env:
            prev_ROS_PACKAGE_PATH = self.env["ROS_PACKAGE_PATH"]
        
        self.env["ROS_PACKAGE_PATH"]=ROBOTPKG_BASE+'/share:' \
            +ROBOTPKG_BASE+'/stacks' \
            +prev_ROS_PACKAGE_PATH
        
        # For cmake
        prev_CMAKE_PREFIX_PATH=''
        if "CMAKE_PREFIX_PATH" in self.env:
            prev_CMAKE_PREFIX_PATH = self.env["CMAKE_PREFIX_PATH"]
            
        self.env["CMAKE_PREFIX_PATH"]=ROBOTPKG_BASE+':'+prev_CMAKE_PREFIX_PATH

    def init_robotpkg_conf_add(self):
        self.robotpkg_conf_lines = [
            'ACCEPTABLE_LICENSES+=openhrp-grx-license',
            'ACCEPTABLE_LICENSES+=cnrs-hpp-closed-source',
            'ACCEPTABLE_LICENSES+=gnu-gpl',
            'ACCEPTABLE_LICENSES+=motion-analysis-license',
            'PREFER_ALTERNATIVE.c-compiler=ccache-gcc gcc',
            'PREFER_ALTERNATIVE.c++-compiler=ccache-g++ g++',
            '# By default, cache will save files in $HOME/.cccache.',
            '# With NFS, this can be a bit slow. The next line make',
            '# ccache save files in ${ROBOTPKG_ROOT}/install/.ccache',
            'HOME.env='+self.ROBOTPKG_ROOT+'/install',
            'PREFER.gnupg=system',
            'PREFER.urdfdom=system',
            'PREFER.urdfdom-headers=system',
	    'PREFER.ros-catkin = system',
	    'PREFER.ros-comm = system',
	    'PREFER.ros-genlisp = system',
	    'PREFER.ros-message-generation = system',
	    'PREFER.ros-std-msgs = system',
	    'PREFER.ros-rospack = system',
	    'PREFER.ros-message-runtime = system',
	    'PREFER.ros-roscpp-core = system',
	    'PREFER.ros-xacro = system',
	    'PREFER.ros-common-msgs = system',
	    'PREFER.ros-lint = system',
	    'PREFER.ros-com-msgs = system',
	    'PREFER.ros-com-msgs = system',
	    'PREFER.bullet = system',
	    'PREFER.ros-ros = system',
	    'PREFER.ros-cmake-modules = system',
	    'PREFER.ros-dynamic-reconfigure = system',
	    'PREFER.ros-realtime-tools = system',
	    'PREFER.ros-control-toolbox = system',
	    'PREFER.ros-bond-core = system',
	    'PREFER.ros-class-loader = system',
	    'PREFER.ros-pluginlib = system',
	    'PREFER.ros-rqt = system',
	    'PREFER.ros-humanoid-msgs = system',
	    'PREFER.ros-genmsg = system',
	    'PREFER.ros-actionlib = system',
	    'PREFER.ros-geometry = system',
	    'PREFER.collada-dom = system',
	    'PREFER.orocos-kdl = system',
            'PREFER.octomap = system',
	    'PREFER.ros-angles  = system',
	    'PREFER.ros-console-bridge = system',
	    'PREFER.ros-eigen-stl-containers = system',
	    'PREFER.ros-random-numbers = system',
	    'PREFER.ros-resource-retriever = system',
	    'PREFER.ros-shape-tools = system',
	    'PREFER.ros-geometric-shapes = system',
	    'PREFER.ros-srdfdom = system',
	    'PREFER.ros-robot-model = system',
	    'PREFER.ros-orocos-kdl = system',
	    'PREFER.assimp=system',
            'ACCEPTABLE_LICENSES+=pal-license',
            'ROS_PACKAGE_PATH='+self.ROBOTPKG_ROOT+'/install/share:$ROS_PACKAGE_PATH']

    def is_robotpkg_present(self,wip_repository):
        """ Check if there is already a robotpkg directory with wip
        """
        robotpkg_candidate_dir = self.ROBOTPKG_ROOT+'/robotpkg'
        if not os.path.isdir(robotpkg_candidate_dir):
            return False
        robotpkg_wip_candidate_dir = self.ROBOTPKG_ROOT+'/robotpkg/wip'
        if not os.path.isdir(robotpkg_wip_candidate_dir):
            return False
        return True
        
    def prepare_robotpkg(self,wip_repository):
        """ 
        Prepare the robotpkg environment

        Make robotpkg directoriers, clone it with wip, bootstrap and add 
        information in the file ${ROBOTPKG_ROOT}/install/etc/robotpkg.conf
        """
        self.make_robotpkg_dirs()
        self.cloning_robotpkg_main()
        self.cloning_robotpkg_wip(wip_repository)
        self.bootstrap_robotpkg()
        self.complete_robotpkg_conffile()
        
    def make_robotpkg_dirs(self):
        """Create directories for robotpkg

        ROBOTPKG_ROOT
        ROBOTPKG_ROOT/install
        """
        print(self.GREEN+'Creating the repositories'+self.NC)
        dirname=self.ROBOTPKG_ROOT+'/'
        os.makedirs(dirname,0o777,True)
        dirname=self.ROBOTPKG_ROOT+'/install'
        os.makedirs(dirname,0o777,True)
        
    def cloning_robotpkg_main(self):
        """Clones the main robotpkg repository"""
        print(self.GREEN+'Cloning robotpkg'+self.NC+'\n')
        os.chdir(self.ROBOTPKG_ROOT)
        self.execute("git clone https://git.openrobots.org/robots/robotpkg.git")

    def cloning_robotpkg_wip(self,wip_repository):
        """Clones the wip robotpkg repository"""
        os.chdir(self.ROBOTPKG_ROOT+'/robotpkg')
        print(self.GREEN+'Cloning robotpkg/wip'+self.NC+'\n')
        self.execute("git clone "+wip_repository)

    def bootstrap_robotpkg(self):
        """ bootstrap robotpkg
        
        This method calls:
        bootstrap --prefix=${ROBOTPKG_ROOT}/install
        only if there is no
        ${ROBOTPKG_ROOT}/install/etc/robotpkg.conf
        already present.
        """
        # Test if a file in ROBOTPKG_ROOT/install/etc/robotpkg.conf already exists
        rpkg_conf_filename=self.ROBOTPKG_ROOT+'/install/etc/robotpkg.conf'
        rpkg_conf_file = Path(rpkg_conf_filename)
        if rpkg_conf_file.is_file():
            print(self.PURPLE+rpkg_conf_filename+self.NC+' already exists\n')
            return
        os.chdir(self.ROBOTPKG_ROOT+'/robotpkg/bootstrap')
        print(self.GREEN+'Boostrap robotpkg'+self.NC+'\n')
        self.execute('./bootstrap --prefix='+self.ROBOTPKG_ROOT+'/install')

    def complete_robotpkg_conffile(self):
        """Add the contents of robotpkg_conf_lines in robotpkg.conf file

        Avoid to add two times the same information.
        """
        os.chdir(self.ROBOTPKG_ROOT+'/install/etc')
        print(self.GREEN+'Adding information to '+self.ROBOTPKG_ROOT+'/install/etc/robotpkg.conf\n')
        
        # Open the file, read it and stores it in file_robotpkg_contents
        file_robotpkgconf = open("robotpkg.conf",'r')
        file_robotpkgconf_contents = file_robotpkgconf.read()
        file_robotpkgconf.close()

        # Add new lines at the end of robotpkg.conf file.
        file_robotpkgconf = open("robotpkg.conf",'a')
        for stdout_line in self.robotpkg_conf_lines:
            if file_robotpkgconf_contents.find(stdout_line)==-1:
                file_robotpkgconf.write(stdout_line+'\n')
        file_robotpkgconf.close()

    def build_rpkg_checkoutdir_pkg_path(self,packagename):
        """ Execute bashcmd in the working directory of packagename"""
        # Going into the repository directory
        hostname = socket.gethostname()
        group = self.robotpkg_src_intro.package_dict[packagename].group
        pathname = self.ROBOTPKG_ROOT+'/robotpkg/'+group+'/'+packagename+'/work.'+hostname
        return pathname
        
    def apply_rpkg_checkout_package(self,packagename,branchname):
        """ Performs a make checkout in packagename directory
        
        packagename: The name of package in which the git clone will be perfomed.
        branchname: The name of the branch used in the repository.

        The location of the repository is specified in the robotpkg Makefile.
        """
        if not packagename in self.robotpkg_src_intro.package_dict.keys():
            print(packagename + " not in robotpkg. Please check the name")
            return False
        
        group = self.robotpkg_src_intro.package_dict[packagename].group
        print(self.GREEN+'Checkout '+ packagename +' in robotpkg/'+group+self.NC+'\n')
        # Checking if we need to clean or not the package

        # First check if the working directory exists
        directory_to_clean=True
        checkoutdir_pkg_path=self.build_rpkg_checkoutdir_pkg_path(packagename)

        # If it does
        if os.path.isdir(checkoutdir_pkg_path):
            if self.debug>3:
              print('Going into :\n'+checkoutdir_pkg_path)

            # Then go inside it
            os.chdir(checkoutdir_pkg_path)

            # If it does then maybe this is not a git directory
            folders=[f.path for f in os.scandir(checkoutdir_pkg_path) if f.is_dir()]
            for folder in folders:
                if self.debug>3:
                    print("Going into: "+folder)
                os.chdir(folder)
                # Check if there is a git folder
                git_folder=folder+'/.git'
                if os.path.isdir(git_folder):
                    if self.debug>3:
                        print('Git folder found:'+git_folder)
                    # Now that we detected a git folder
                    # Check the branch
                    outputdata =self.execute("git symbolic-ref --short -q HEAD")
                    if outputdata != None:
                        for stdout_line in outputdata.splitlines():
                            lstr = str(stdout_line.decode('utf-8'))
                            if lstr != branchname:
                                print(self.RED+' Wrong branch name: '+lstr+' instead of '+branchname+self.NC)
                            else:
                                finaldirectory=folder
                                directory_to_clean=False
                    else:
                        print(self.RED +"Could not find the branch of the git repository ! Wrong git call"+self.NC)

        if self.debug>3:
            print('Directory to clean: '+str(directory_to_clean))
        if directory_to_clean:
            # Going into the directory of the package
            os.chdir(self.ROBOTPKG_ROOT+'/robotpkg/'+group+'/'+packagename)
            self.execute("make clean confirm")
            self.execute("make checkout")
        else:
            os.chdir(finaldirectory)
            # Remove all the files which may have been modified.
            self.execute("git reset --hard")
            # Pull all the modification push upstream.
            self.execute("git pull origin "+branchname+':'+branchname)
            self.execute("git submodule update")

    def apply_git_checkout_branch(self,packagename,branchname):
        """
        Changes the branch of a git repository in robotpkg.

        The method first detects that the package working directory is 
        really a git repository. Then it performs the branch switch.
        """
        bashcmd='git checkout '+branchname
        checkoutdir_pkg_path=self.build_rpkg_checkoutdir_pkg_path(packagename)
        folders=[f.path for f in os.scandir(checkoutdir_pkg_path) if f.is_dir()]
        for folder in folders:
           if self.debug>3:
             print("Going into: "+folder)
           os.chdir(folder)
           git_folder=folder+'/.git'
           if os.path.isdir(git_folder):
               self.execute(bashcmd)


    def compile_package(self,packagename):
        """ Performs make replace confirm in package working directory
        """
        # Going into the directory of the package
        group = self.robotpkg_src_intro.package_dict[packagename].group
        os.chdir(self.ROBOTPKG_ROOT+'/robotpkg/'+group+'/'+packagename)
        print(self.GREEN+'Compile '+ packagename +' in robotpkg/'+group+self.NC+'\n')
        
        # Compiling the repository
        checkoutdir_pkg_path=self.build_rpkg_checkoutdir_pkg_path(packagename)
        # If the installation has already been done
        if os.path.isdir(checkoutdir_pkg_path):
            self.execute("make update confirm")
        else:
            self.execute("make install")

    def handle_package(self,packagename,branchname):
        """Compile and install packagename with branch branchname
        
        First performs the proper make checkout and git operation to get the branch
        Then compile the package with make replace.
        Do not use make update confirm, this install the release version (the tar file).
        """
        if not packagename in self.robotpkg_src_intro.package_dict.keys():
            print(packagename + " not in robotpkg. Please check the name")           
            return False
        
        if not branchname==None:
            self.apply_rpkg_checkout_package(packagename,branchname)
            self.apply_git_checkout_branch(packagename,branchname)
        self.compile_package(packagename)
        return True

    def verify_list_of_packages(self,arch_release_candidates):
        """ Verify the list given by arch_release_candidates
        and check if this is in the robotpkg list
        """
        if arch_release_candidates != None:
            for package_name,branch_name in arch_release_candidates:
                if not package_name in self.robotpkg_src_intro.package_dict.keys():
                    print(self.RED + package_name + " not in robotpkg.\nPlease check the name"+self.NC)        
                    return False;
        return True;

    def perform_test_rc(self,arch_release_candidates=None,dist_files_path=None,wip_repository=None):
        """Install packages specified by arch_release_candidates using the associated branchnames.
        If available the set of archives in dist_files_path will be used.
        If specified, then use wip_repository instead of the official robotpkg repository. 

        arch_release_candidates: tuple of list [ ('package_name','branch_name','group'), ... ]
        """

        
        if wip_repository==None:
            if self.ssh_git_openrobots==True:
                wip_repository="ssh://git@git.openrobots.org/robots/robotpkg/robotpkg-wip wip"
            else:
                wip_repository="https://git.openrobots.org/robots/robotpkg/robotpkg-wip.git wip"
            
        # Create the robotpkg structure.
        self.prepare_robotpkg(wip_repository)

        # Add robotpkg_src_intro to self
        add_robotpkg_src_introspection(self)

        if not self.verify_list_of_packages(arch_release_candidates):
            print(self.RED+
                  "perform_test_rc : One of the package mentionned is not correct. Please fix it by looking at previous message"
                  +self.NC)
            return False

        # Copy dist files if specified
        self.copy_test_dist_files(dist_files_path)

            
        # Download and install each package
        handling_package_properly_done = True
        if arch_release_candidates != None:
            for package_name,branch_name in arch_release_candidates:
                if not self.handle_package(package_name,branch_name):
                    handling_package_properly_done=False
        return handling_package_properly_done

    def copy_test_dist_files(self,dist_files_path):
        """ Method to copy the distfiles from the specified directory to the targeted one.
        """
        if dist_files_path!=None:
            dest_dist_files_path=self.ROBOTPKG_ROOT+"/robotpkg/distfiles/"
            os.makedirs(dest_dist_files_path,0o777,True)
            bashcmd="cp -r "+dist_files_path+"/* "+dest_dist_files_path
            print("bashcmd: "+bashcmd)
            self.execute_call(bashcmd)

    def status_of_packages(self,arch_release_candidates=None):
        """ Display the status of the packages provided.
        More precisely they checked if the current package is the one currently released by robotpkg
        or if it is checkout
        """
        # Check if the list is consistent with robotpkg
        if not self.verify_list_of_packages(arch_release_candidates):
            print(self.RED+
                  "perform_test_rc : One of the package mentionned is not correct. Please fix it by looking at previous message"
                  +self.NC)
            return

        # Iterating over the list
        for package_name,branch_name in arch_release_candidates:
            checkoutdir_pkg_path=build_rpkg_checkoutdir_pkg_path(self,packagename)
            
        

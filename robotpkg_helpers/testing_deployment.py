#!/usr/bin/python3
import os
import sys
from pathlib import Path
import socket

from .utils import execute_call,init_environment_variables,add_colors
from .src_introspection import RobotpkgPackage,RobotpkgSrcIntrospection
from .src_introspection import add_robotpkg_variables,add_robotpkg_src_introspection
from .logging import RobotpkghLogging

class RobotpkgTests:

    def __init__(self,
                 ROBOTPKG_ROOT=None,
                 debug=0,
                 ROBOTPKG_MNG_ROOT=None):
        """ Install and compile a robotpkg infrastructure

        Arguments:
        ROBOTPKG_ROOT: The directory where the whole robotpkg install takes place.
        debug: debug level
        """

        # Add Logging capabilities
        self.logger = RobotpkghLogging("testing_deployment")

        # Add ROBOTPKG_ROOT, ROBOTPKG_ROOT_SRC to self
        add_robotpkg_variables(self,ROBOTPKG_ROOT)

        # Set ROBOTPKG_MNG_ROOT
        if ROBOTPKG_MNG_ROOT!=None:
            self.ROBOTPKG_MNG_ROOT=ROBOTPKG_MNG_ROOT
        else:
            self.ROBOTPKG_MNG_ROOT=ROBOTPKG_ROOT+'/..'

        if not hasattr(self,'ROBOTPKG_ROOT_SRC'):
            self.logger.print_err_log('add_robotpkg_variables is not doing what it is suppose to be doing\n')
            sys.exit()

        add_colors(self)

        # Prepare the environment variables to compile with robotpkg
        init_environment_variables(self,self.ROBOTPKG_ROOT)

        # Prepare the robotpkg.conf
        self.init_robotpkg_conf_add()

        self.debug = debug
        self.ssh_git_openrobots = False


    def execute(self,bashCommand):
        return self.logger.execute(bashCommand,self.env,self.debug)

    def execute_call(self,bashCommand):
        return self.logger.execute_call(bashCommand,self.debug)

    def add_robotpkg_conf_pkg_info(self,arch_release_candidate):
        """ This method add the repository for each package listed in robotpkg.conf
        """
        for package_name,package_rc in arch_release_candidate.data['rc_pkgs'].items():
            if 'git_repo' in package_rc.keys():
                pkg_repo_str = 'REPOSITORY.'+package_rc['name']+'=git '+package_rc['git_repo']
            self.robotpkg_conf_lines.append(pkg_repo_str)


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
            '# ccache save files in ${ROBOTPKG_MNG_ROOT}/.ccache',
            'HOME.env='+self.ROBOTPKG_MNG_ROOT+'/',
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
            'ROS_PACKAGE_PATH='+self.env["ROS_PACKAGE_PATH"],
            'PKG_CONFIG_DIRS='+self.env["PKG_CONFIG_PATH"]
        ]

        env=os.environ.copy()
        if 'JRL_FTP_USER' in env.keys():
            jrl_ftp_user = 'JRL_FTP_USER='+env['JRL_FTP_USER']
            self.robotpkg_conf_lines.append(jrl_ftp_user)
        if 'JRL_FTP_PASSWD' in env.keys():
            jrl_ftp_passwd = 'JRL_FTP_PASSWD='+env['JRL_FTP_PASSWD']
            self.robotpkg_conf_lines.append(jrl_ftp_passwd)


    def is_robotpkg_present(self):
        """ Check if there is already a robotpkg directory with wip
        """
        robotpkg_candidate_dir = self.ROBOTPKG_ROOT+'/robotpkg'
        if not os.path.isdir(robotpkg_candidate_dir):
            return False
        robotpkg_wip_candidate_dir = self.ROBOTPKG_ROOT+'/robotpkg/wip'
        if not os.path.isdir(robotpkg_wip_candidate_dir):
            return False
        return True

    def prepare_robotpkg(self,arch_release_candidate):
        """
        Prepare the robotpkg environment

        Make robotpkg directoriers, clone it with wip, bootstrap and add
        information in the file ${ROBOTPKG_ROOT}/install/etc/robotpkg.conf
        """
        wip_rpkg_repository = arch_release_candidate.data['repo_robotpkg_wip']
        main_rpkg_repository = arch_release_candidate.data['repo_robotpkg_main']
        self.make_robotpkg_dirs()
        self.cloning_robotpkg_main(main_rpkg_repository)
        self.cloning_robotpkg_wip(wip_rpkg_repository)
        self.bootstrap_robotpkg()
        self.add_robotpkg_conf_pkg_info(arch_release_candidate)
        self.complete_robotpkg_conffile()

    def make_robotpkg_dirs(self):
        """Create directories for robotpkg

        ROBOTPKG_ROOT
        ROBOTPKG_ROOT/install
        """
        msg = self.GREEN+'Creating the repositories'+self.NC
        self.logger.print_log(msg)
        dirname=self.ROBOTPKG_ROOT+'/'
        os.makedirs(dirname,0o777,True)
        dirname=self.ROBOTPKG_ROOT+'/install'
        os.makedirs(dirname,0o777,True)

    def cloning_robotpkg_repo(self,dirpath,repo):
        """Clones the repository repo in dirpath """
        os.chdir(dirpath)

        ldebug = self.debug
        self.debug=0
        outputdata,error,p_status = self.execute("git clone --depth 1 --no-single-branch "+repo)
        self.debug=ldebug

        if outputdata!=None:
            for stdout_line in outputdata.splitlines():
                self.logger.print_log(stdout_line.decode('utf-8'))

        if error!=None:
            self.logger.print_log("There is an error")
            for stdout_line in error.splitlines():
                str_cmp = stdout_line.decode('utf-8')
                str2_cmp='fatal: destination path \'robotpkg\' already exists and is not an empty directory.'

                if str_cmp==str2_cmp:
                    msg= 'robotpkg already exists -> update the repository '
                    self.logger.print_log(msg)
                    outputdata,error,p_status = self.execute("git pull origin master:master")
                else:
                    self.logger.print_log(str2_cmp)

    def cloning_robotpkg_main(self,main_repository=None):
        """ Build path to main repository and perform cloning
        """
        dirpath = self.ROBOTPKG_ROOT
        if (main_repository==None):
            main_repository = 'https://git.openrobots.org/robots/robotpkg.git'
        msg=self.GREEN+'Cloning robotpkg'+self.NC+' in ' + self.ROBOTPKG_ROOT + '\n'
        self.logger.print_log(msg)
        self.cloning_robotpkg_repo(dirpath,main_repository)

    def cloning_robotpkg_wip(self,wip_repository):
        """Clones the wip robotpkg repository"""
        dirpath=self.ROBOTPKG_ROOT+'/robotpkg'
        msg= self.GREEN+'Cloning robotpkg/wip'+self.NC+'\n'
        self.logger.print_log(msg)
        wip_repository = wip_repository + ' wip'
        self.cloning_robotpkg_repo(dirpath,wip_repository)

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
            # It alredy exists
            msg=self.PURPLE+rpkg_conf_filename+self.NC+' already exists\n'
            self.logger.print_err_log(msg)
            return
        os.chdir(self.ROBOTPKG_ROOT+'/robotpkg/bootstrap')

        # Creating bootstrap
        msg=self.GREEN+'Boostrap robotpkg'+self.NC+'\n'
        self.logger.print_log(msg)
        self.execute('./bootstrap --prefix='+self.ROBOTPKG_ROOT+'/install')

    def complete_robotpkg_conffile(self):
        """Add the contents of robotpkg_conf_lines in robotpkg.conf file

        Avoid to add two times the same information.
        """
        os.chdir(self.ROBOTPKG_ROOT+'/install/etc')
        msg = self.GREEN+'Adding information to '+self.ROBOTPKG_ROOT+'/install/etc/robotpkg.conf\n'
        self.logger.print_log(msg)

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

    def apply_rpkg_checkout_package(self,packagename,package_rc):
        """ Performs a make checkout in packagename directory

        packagename: The name of package in which the git clone will be perfomed.
        branchname: The name of the branch used in the repository.

        The location of the repository is specified in the robotpkg Makefile.
        """
        if not packagename in self.robotpkg_src_intro.package_dict.keys():
            self.logger.print_err_log(packagename + " not in robotpkg. Please check the name")
            return False

        group = self.robotpkg_src_intro.package_dict[packagename].group
        self.logger.print_log(self.GREEN+'Checkout '+ packagename +' in robotpkg/'+group+self.NC+'\n')
        # Checking if we need to clean or not the package

        # First check if the working directory exists
        directory_to_clean=True
        checkoutdir_pkg_path=self.build_rpkg_checkoutdir_pkg_path(packagename)
        branchname = package_rc['branch']

        # If it does
        if os.path.isdir(checkoutdir_pkg_path):
            if self.debug>3:
              self.logger.print_log('Going into :\n'+checkoutdir_pkg_path)

            # Then go inside it
            os.chdir(checkoutdir_pkg_path)

            # If it does then maybe this is not a git directory
            folders=[f.path for f in os.scandir(checkoutdir_pkg_path) if f.is_dir()]
            for folder in folders:
                if self.debug>3:
                    self.logger.print_log("Going into: "+folder)
                os.chdir(folder)
                # Check if there is a git folder
                git_folder=folder+'/.git'
                if os.path.isdir(git_folder):
                    if self.debug>3:
                        self.logger.print_log('Git folder found:'+git_folder)
                    # Now that we detected a git folder
                    # Check the branch
                    stdOutput,errOutput,p_status =self.execute("git symbolic-ref --short -q HEAD")
                    if stdOutput != None:
                        for stdout_line in stdOutput.splitlines():
                            lstr = str(stdout_line.decode('utf-8'))
                            if lstr != branchname:
                                self.logger.print_log(self.RED+' Wrong branch name: '+lstr+' instead of '+branchname+self.NC)
                                # Switch to upstream branch.
                                self.execute("git checkout -b remotes/origin/"+branchname)
                                # Give it the name of the branch
                                self.execute("git checkout -b "+branchname)
                                self.execute("git submodule update")
                                directory_to_clean=False
                                finaldirectory=folder
                            else:
                                finaldirectory=folder
                                directory_to_clean=False
                    else:
                        self.logger.print_err_log(self.RED +"Could not find the branch of the git repository ! Wrong git call"+self.NC)

        if self.debug>3:
            self.logger.print_log('Directory to clean: '+str(directory_to_clean))
        if directory_to_clean:
            # Going into the directory of the package
            os.chdir(self.ROBOTPKG_ROOT+'/robotpkg/'+group+'/'+packagename)
            self.execute("make clean confirm")
            self.execute("make checkout")
        else:
            os.chdir(finaldirectory)
            # Remove all the files which may have been modified.
            self.execute("git reset --hard")
            # Pull all the modification from upstream.
            self.execute("git pull origin "+branchname+':'+branchname)
            self.execute("git submodule update")

    def apply_git_checkout_branch(self,packagename,branchname):
        """
        Changes the branch of a git repository in robotpkg.

        The method first detects that the package working directory is
        really a git repository. Then it performs the branch switch.
        """
        checkoutdir_pkg_path=self.build_rpkg_checkoutdir_pkg_path(packagename)
        if self.debug>3:
            self.logger.print_log(checkoutdir_pkg_path)
        folders=[f.path for f in os.scandir(checkoutdir_pkg_path) if f.is_dir()]
        for folder in folders:
           if self.debug>3:
             self.logger.print_log("Going into: "+folder)
           os.chdir(folder)
           git_folder=folder+'/.git'
           if os.path.isdir(git_folder):
               bashcmd='git checkout '+branchname
               if self.debug>3:
                   self.logger.print_log(bashcmd)
               self.execute(bashcmd)
               bashcmd='git submodule update'
               if self.debug>3:
                   self.logger.print_log(bashcmd)
               self.execute(bashcmd)


    def update_compile_package(self, packagename):
        stdOutput, errOutput,p_status=self.execute("make update confirm")
        for line in stdOutput.splitlines():
            self.logger.print_log(line.decode('utf-8'))
        if errOutput!=None:
            for stdout_line in errOutput.splitlines():
                str_cmp = stdout_line.decode('utf-8')
                self.logger.print_log("make update confirm:"+str_cmp)

                # If there is a problem related
                if str_cmp == "ERROR: Files from unknown package:":
                    self.logger.print_log(self.RED+"Confirm the installation"+self.NC)
                    stdOutput, errOutput,p_status=self.execute("make install confirm")
                    break

    def compile_package(self,packagename):
        """ Performs make replace confirm in package working directory
        """
        # Going into the directory of the package
        group = self.robotpkg_src_intro.package_dict[packagename].group
        os.chdir(self.ROBOTPKG_ROOT+'/robotpkg/'+group+'/'+packagename)
        self.logger.print_log(self.GREEN+'Compile '+ packagename +' in robotpkg/'+group+self.NC+'\n')

        # Compiling the repository
        checkoutdir_pkg_path=self.build_rpkg_checkoutdir_pkg_path(packagename)
        # If the installation has already been done
        if self.robotpkg_src_intro.package_dict[packagename].is_rpkg_installed(self.ROBOTPKG_BASE,
                                                                               self.env):
            # do nothing for now
            # self.update_compile_package(packagename)
            self.logger.print_log("Do nothing")
        else:
            stdOutput,errOutput,p_status =self.execute("make install")
            if errOutput!=None:
                line =0
                for stdout_line in errOutput.splitlines():
                    str_cmp = stdout_line.decode('utf-8')
                    self.logger.print_log(str_cmp)
                    if line==2:
                        if str_cmp=="ERROR: overwrite already installed files.":
                            self.logger.print_err_log("Error state: overwrite_files")


    def prepare_package(self,package_name,package_rc):
        """ Performs the proper make checkout and git operation to get the branch
        """
        if not package_name in self.robotpkg_src_intro.package_dict.keys():
            self.logger.print_err_log(package_name + " not in robotpkg. Please check the name")
            return False

        if not package_rc==None:
            self.apply_rpkg_checkout_package(package_name,package_rc)
            self.apply_git_checkout_branch(package_name,package_rc['branch'])
        return True

    def handle_package(self,package_name,package_rc):
        """Compile and install packagename with branch branchname

        Compile the package with make replace.
        Do not use make update confirm, this install the release version (the tar file).

        """
        return True

    def verify_list_of_packages(self,arch_release_candidates):
        """ Verify the list given by arch_release_candidates
        and check if this is in the robotpkg list
        """
        if arch_release_candidates != None:
            self.logger.print_log("arch_release_candidates: ")
            arch_release_candidates.display()
            for package_name in arch_release_candidates.data['rc_pkgs'].keys():
                if not package_name in self.robotpkg_src_intro.package_dict.keys():
                    self.logger.print_err_log(self.RED + package_name + " not in robotpkg.\nPlease check the name"+self.NC)
                    return False;
        return True;

    def perform_test_rc(self,
                        arch_release_candidates=None,
                        dist_files_path=None):
        """Install packages specified by arch_release_candidates using the associated branchnames.
        If available the set of archives in dist_files_path will be used.
        If specified, then use wip_repository instead of the official robotpkg repository.

        arch_release_candidates: tuple of list [ ('package_name','branch_name','group'), ... ]
        """

        # Create the robotpkg structure.
        self.prepare_robotpkg(arch_release_candidates)

        # Add robotpkg_src_intro to self
        add_robotpkg_src_introspection(self)

        if not self.verify_list_of_packages(arch_release_candidates):
            self.logger.print_err_log(self.RED+
                  "perform_test_rc : One of the package mentionned is not correct." +
                  "Please fix it by looking at previous message"
                  +self.NC)
            return False

        # Copy dist files if specified
        self.copy_test_dist_files(dist_files_path)

        # Download and install each package
        handling_package_properly_done = True
        if arch_release_candidates != None:
            for package_name,package_rc in arch_release_candidates.data['rc_pkgs'].items():
                if not self.prepare_package(package_name,package_rc):
                    handling_package_properly_done=False

            for package_name,package_rc in arch_release_candidates.data['rc_pkgs'].items():
                if not self.handle_package(package_name,package_rc):
                    handling_package_properly_done=False
        return handling_package_properly_done

    def copy_test_dist_files(self,dist_files_path):
        """ Method to copy the distfiles from the specified directory to the targeted one.
        """
        if dist_files_path!=None:
            dest_dist_files_path=self.ROBOTPKG_ROOT+"/robotpkg/distfiles/"
            os.makedirs(dest_dist_files_path,0o777,True)
            bashcmd="cp -r "+dist_files_path+"/* "+dest_dist_files_path

            msg = "bashcmd: "+bashcmd
            self.logger.print_log(msg)
            self.execute_call(bashcmd)

    def status_of_packages(self,arch_release_candidates=None):
        """ Display the status of the packages provided.
        More precisely they checked if the current package is the one currently released by robotpkg
        or if it is checkout
        """
        # Check if the list is consistent with robotpkg
        if not self.verify_list_of_packages(arch_release_candidates):
            msg = self.RED + \
                  "perform_test_rc : One of the package mentionned is not correct. Please fix it by looking at previous message" \
                  +self.NC
            self.logger.print_err_log(msg)
            return

        # Iterating over the list
        for package_name,branch_name in arch_release_candidates:
            checkoutdir_pkg_path=build_rpkg_checkoutdir_pkg_path(self,packagename)

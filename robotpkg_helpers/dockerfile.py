#!/usr/bin/python3
import glob
import inspect
import os
import re
from shutil import copy
import stat
import subprocess
import sys
from .utils import execute, execute_call
from .src_introspection import RobotpkgSrcIntrospection,RobotpkgPackage

def valid_name(name):
    return name.replace('_', ' ').replace('-', ' ').lower()

class RobotpkgGenerateDockerFile:

    def __init__(self,CMakeLists_txt_path,ROBOTPKG_ROOT_SRC, dst_dir="/tmp/robotpkg_docker",debug=0):
        """ Creates a docker file from a CMakeLists.txt file

        Arguments:
        CMakeLists_txt_path: The path to the CMakeLists.txt to analyze.
        ROBOTPKG_ROOT_SRC: The path to robotpkg sources.
        dst_dir: The path where the files should be generated
        """

        # Set debug mode (default set to 0)
        self.debug=debug
        # Set the path to the CMakeLists.txt of the repository to analyze.
        self.CMakeLists_txt_path = CMakeLists_txt_path
        # Set the path where generating the Dockerfiles and copy the robotpkg_helpers
        self.dst_dir = dst_dir
        # Create dst_dir if needed
        self.check_dst_dir()
        self.prepare_dst_dir()
        # Create the object analyzing robotpkg
        self.robotpkg_src_intro = RobotpkgSrcIntrospection(ROBOTPKG_ROOT_SRC)
        # Analyzes the CMakeLists.txt file
        if not self.cmake():
            return
        # Check which packages are provided by robotpkg and which are provided by the OS
        # This part is still very fragile and error prone.
        self.filter_robotpkg_packages()
        # Display the packages found and split them into robotpkg and OS.
        self.display_packages()
        # Generates the python script to compile the necessary packages and their release version
        self.generate_test_rc()
        # Generates the docker files
        self.generate_docker_file_for_img()
        self.generate_docker_file_for_test()
        #if debug>3:
        #self.robotpkg_src_intro.display()
        
        
    def init_colors(self):
        """ Initialize colors for beautification
        
        The following variables are available: 
        REG, GREEN, PURPLE, NC (no color)
        """
        self.RED =  '\033[0;31m'
        self.GREEN= '\033[0;32m'
        self.PURPLE='\033[0;35m'
        self.NC =   '\033[0m'
        
    def check_dst_dir(self):
        """ This methods check if the destination directory exists and if not creates it
        """
        if not os.path.isdir(self.dst_dir):
            os.mkdir(self.dst_dir)
            os.mkdir(self.dst_dir+'/robotpkg_helpers')

    def prepare_dst_dir(self):
        """ This methods copy the robotpkg_helpers module necessary to create the docker image
        """
        current_py_file= (inspect.getfile(inspect.currentframe()) ) # script filename (usually with path)
        # Find path where this current python script is located
        src_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script director
        list_py = glob.glob(src_dir+ "/*py")
        for apy_file in list_py:
            copy(apy_file,self.dst_dir+'/robotpkg_helpers')

    def jrl_cmake_module_analysis(self,cmake_content):
        """ This methods extracts from the file CMakeLists.txt of the repository to analyze 
        useful informations
        """
        # Search for ADD_[REQUIRED|OPTIONAL]_DEPENDENCY and put it in the list of files
        for project_name in re.findall(r'SET\s*\(\s*PROJECT\_NAME\s*([^\s>="\')]+)\s*\)',
                                       cmake_content, re.I):
            self.project_name=project_name
            print("Project name:" +self.project_name)
        
    def cmake(self):
        # Read CMake file
        filename = self.CMakeLists_txt_path
        self.dict_robot_pkgs={}
        self.dict_os_pkgs=[]
        if not os.path.isfile(filename):
            print("The file specified "+filename+" does not exists")
            return False
        
        with open(filename,"r") as f:
          content = f.read()

          self.jrl_cmake_module_analysis(content)
          
          # Search for ADD_[REQUIRED|OPTIONAL]_DEPENDENCY and put it in the list of files
          for dependency,version in re.findall(r'ADD_[A-Z]+_DEPENDENCY\s*\(["\']?([^\s>="\')]+)\s*[>=]*\s*([\d|.]*)["\']?\)', content, re.I):
              self.dict_robot_pkgs[dependency]=version

          for dependency,version in re.findall(r'ADD_[A-Z]+_DEPENDENCY\s*\(["\']?([^\s>="\')]+)\s*[>=]*\s*([\d|.]*)["\']?\)', content, re.I):
              self.dict_robot_pkgs[dependency]=version

          if self.debug>1:
              print("CMakeLists.txt needs the following packages:")
              print(self.dict_robot_pkgs)
        f.close()
        return True

    def filter_robotpkg_packages(self):
        """ This methods remove from the dictionnary dict_robot_pkgs the packages not handled by robotpkg.
        The removed packages are put inside the dict_os_pkgs dictionary.
        """
        # Need to use the keys() method to iterate
        # as we are removing from the dictionnary using key.
        if self.debug>1:
            print("Filter packages")
        self.tree_of_includes_os = set()
        new_dict_robot_pkgs = dict(self.dict_robot_pkgs)
        for pkg_name in self.dict_robot_pkgs.keys():
            r = self.robotpkg_src_intro.is_pkg_present(pkg_name)
            if not r:
                del new_dict_robot_pkgs[pkg_name]
                self.dict_os_pkgs.append(pkg_name)
            else:
                if self.debug>3:
                    print("\n**********************\nFound pkg " + pkg_name + " in robotpkg")
                found_pkg = self.robotpkg_src_intro.package_dict[pkg_name]
                found_pkg.read_package_info()
                self.robotpkg_src_intro.build_tree_of_dependencies(found_pkg)
                self.tree_of_includes_os = self.tree_of_includes_os.union(found_pkg.tree_of_includes_os)
                    
        self.dict_robot_pkgs = new_dict_robot_pkgs

    def display_packages(self):
        """ Display the packages detected by analyzing only the repository
        """
        for pkg_name,pkg_version in self.dict_robot_pkgs.items():
            print("Package name:" + pkg_name + " " + pkg_version)
        for pkg_name in self.tree_of_includes_os:
            print("OS package name:" + pkg_name)

    def display_tree_of_dependencies(self):
        """ Display all the packages known in robotpkg needed to compile the analyzed repository
        """
        print("Display tree of dependencies:")
        for an_include_mk in self.tree_of_includes_mk:
            print(an_include_mk)
            
    def generate_test_rc(self):
        """ This method generates a python file to compile the packages using robotpkg inside the dockerfile.
        """
        # Generate python file
        filename = self.dst_dir + "/robotpkg_for_docker_file.py"
        with open(filename,"w") as f:
            f.write("#!/usr/bin/python3\n")
            f.write("from robotpkg_helpers import RobotpkgTests \n")
            f.write("dict_robot_pkgs= [ \n")
            for key in  self.dict_robot_pkgs:
                #print(key)
                if len(self.robotpkg_src_intro.package_dict[key].master_repository)==0 :
                    f.write("  (\'"+ key +"\', None), \n")
                else:
                    f.write("  (\'"+ key +"\',\'" + self.dict_robot_pkgs[key] + "\'), \n")
            f.write("]\n")
            f.write("arpgtestrc =RobotpkgTests()\n")
            f.write("arpgtestrc.perform_test_rc(dict_robot_pkgs)\n")
        f.close()
        os.chmod(filename,stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |stat.S_IROTH | stat.S_IXOTH )

    def generate_docker_file_for_img(self):
        """ This methods generates the dockerfile to compile robotpkg and test the the repository being analyzed.
        """
        filename = self.dst_dir + "/Dockerfile"
        with open(filename,"w") as f:
            f.write("FROM ubuntu:16.04 as " + self.project_name+ "_img\n")
            f.write("RUN apt-get update\n")
            f.write("RUN apt-get install -yyq python3 python3-dev git g++ make ccache  libssl-dev libncurses-dev pax tar\n")
            f.write("RUN apt-get install -yyq libboost-dev libboost-date-time-dev libboost-filesystem-dev\n")
            f.write("RUN apt-get install -yyq libboost-system-dev libboost-thread-dev cmake\n")
            f.write("RUN apt-get install -yyq libeigen3-dev pkg-config apt-utils doxygen \n")
            # Add packages found as an OS dependency in the packages
            for an_os_pkg in self.tree_of_includes_os:
                f.write('RUN apt-get install -y '+an_os_pkg+'\n')
            for an_os_pkg in self.dict_os_pkgs:
                f.write('RUN apt-get install -y '+an_os_pkg+'\n')
            f.write("RUN mkdir -p /workdir\n")
            f.write("WORKDIR /workdir\n")
            f.write("COPY . /workdir\n")
            f.write("RUN ls /workdir\n")
            f.write("RUN ls . \n")            
            f.write("RUN /usr/bin/python3 ./robotpkg_for_docker_file.py\n")
            f.write("\n")
        f.close()

    def generate_docker_file_for_test(self):
        """ This methods generates a file named Dockerfile to test the repository being analyzed.
        It is done using the image created by the file Dockerfile created by generate_docker_file_for_img()
        This Dockerfile assumes a clean repository.
        """
        filename = self.dst_dir + "/Dockerfile_" + self.project_name
        with open(filename,"w") as f:
            f.write("FROM "+ self.project_name + "_img")
            f.write("COPY . /app")
            f.write("RUN mkdir /app/build")
            f.write("RUN cmake -DCMAKE_BUILD_TYPE=DEBUG --build /app/build /app")
            f.write("RUN make --directory=/app/build")
        f.close()
        
    def build_docker(self):
        print("Build docker file")
        self.env = os.environ.copy()
        bash_cmd = "docker build -f " + self.dst_dir + "/Dockerfile "+self.dst_dir + " --tag=" + self.project_name + "_img"
        execute(bash_cmd, self.env,3)

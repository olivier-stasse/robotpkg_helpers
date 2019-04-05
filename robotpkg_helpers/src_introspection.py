import os
import re
import json
import sys
from .package import RobotpkgPackage
from .utils import build_test_rc_robotpkg_vars, add_colors

def add_robotpkg_variables(anObject,ROBOTPKG_ROOT=None):
    """ This function adds ROBOTPKG_ROOT, ROBOTPKG_ROOT_SRC and robotpkg_src_intro
    if they do exist.
    It also adds robotpkg_vars
    robotpkg_src_intro provides information on robotpkg
    """

    if ROBOTPKG_ROOT is None:
        anObject.robotpkg_vars = build_test_rc_robotpkg_vars()
        anObject.ROBOTPKG_ROOT= anObject.robotpkg_vars['ROOT']
    else:
        anObject.ROBOTPKG_ROOT=ROBOTPKG_ROOT

    anObject.ROBOTPKG_ROOT_SRC=anObject.ROBOTPKG_ROOT + '/robotpkg'
    anObject.ROBOTPKG_BASE=anObject.ROBOTPKG_ROOT + '/install'

def add_robotpkg_src_introspection(anObject,ROBOTPKG_ROOT=None):
    if hasattr(anObject,'robotpkg_src_intro'):
        return

    if not hasattr(anObject,'ROBOTPKG_ROOT_SRC'):
        add_robotpkg_variables(anObject,ROBOTPKG_ROOT)

    # Analysis the robotpkg src structure
    anObject.robotpkg_src_intro= RobotpkgSrcIntrospection(anObject.ROBOTPKG_ROOT_SRC)


# This class handles the analysis of a robotpkg directory
class RobotpkgSrcIntrospection:

    def __init__(self, ROBOTPKG_ROOT_SRC=None,debug=0):
        """ Class to perform robotpkg introspection

        Arguments:
        ROBOTPKG_ROOT_SRC: The directory where the whole robotpkg source is located.
        """
        add_colors(self)
        self.debug=debug
        self.ROBOTPKG_ROOT_SRC= ROBOTPKG_ROOT_SRC
        self.build_list_of_packages()
        
    def create_new_pkg_description(self,group,pkg_name,dirname,subgroup=None):
        """ Create a package object.
        group: Given by the directory in which is the package
        subgroup: Some groups have another level of hierarchy (mk for instance)
        pkg_name: Name of the package here the directory in which the package
        is described
        """
        if self.debug>5:
            print(dirname + '/' + pkg_name)
        self.package_dict[pkg_name]=RobotpkgPackage(pkg_name,
                                                    dirname + '/' + pkg_name,
                                                    group,subgroup)
        # Analyzes the file Makefile
        self.package_dict[pkg_name].read_makefile()
        # Analyzes the file depend.mk
        self.package_dict[pkg_name].read_depend_mk()
        #print(dirname+'/'+pkg_name)

    def handling_subpkg_dir(self,adir,asubdir,dirname):
        """ Build list of packages in a sub directory of robotpkg
        """
        if os.path.isdir(asubdir):
            os.chdir(asubdir)
            # Special treatment is asubdir is mk
            # There is another level of hierarchy
            if adir=="mk":
                subtwodirs = os.listdir()
                for asubtwodir in subtwodirs:
                    if os.path.isdir(asubtwodir):
                        os.chdir(asubtwodir)
                        self.create_new_pkg_description(adir,
                                                        asubdir,
                                                        dirname,
                                                        subgroup=asubtwodir)
                        os.chdir(dirname+'/'+asubdir)
            else:
                self.create_new_pkg_description(adir,asubdir,dirname)
            os.chdir(dirname)

    def build_list_of_packages(self):
        """ Class to perform robotpkg introspection

        This functions uses  ROBOTPKG_ROOT_SRC: 
        The directory where the whole robotpkg source is located.
        """
        # Keep current directory.
        current_path=os.getcwd()
        self.package_dict={}

        # Explore robotpkg src direction
        if not os.path.isdir(self.ROBOTPKG_ROOT_SRC):
            print(self.RED+"ROBOTPKG_ROOT_SRC:"+self.NC)
            print(self.RED+self.ROBOTPKG_ROOT_SRC+" does not exists"+self.NC)
            sys.exit(-1)

        dirs=os.listdir(self.ROBOTPKG_ROOT_SRC)
        for adir in dirs:
            # Ignore distfiles directory.
            if adir=='distfiles':
                continue

            # General repo
            dirname = self.ROBOTPKG_ROOT_SRC+'/'+adir
            if os.path.isdir(dirname):
                os.chdir(dirname)

                # In each subgroup search for package
                subdirs= os.listdir()
                for asubdir in subdirs:
                    self.handling_subpkg_dir(adir,asubdir,dirname)
            os.chdir(self.ROBOTPKG_ROOT_SRC)
        # Going back to where we were
        os.chdir(current_path)


    def is_pkg_present(self,package_name):
        """ Check if a given package is in the list of robotpkg packages
        """
        if package_name in self.package_dict.keys():
            return True
        else:
            return False

    def display(self):
        """ Display the list of packages
        """
        for pkg_name,a_rpkg in self.package_dict.items():
            a_rpkg.display()

    def build_tree_of_dependencies(self,a_rpkg):
        """ This methods is looking for the whole set of dependencies inside robotpkg

        It creates a python set called tree_of_includes_dep which is giving the set
        of packages needed by the package a_rpkg.
        For Ubuntu and Debian if available it provides a system equivalent.
        """
        if self.debug>3:
            print("Build tree of dependencies " + a_rpkg.name)
        a_rpkg.tree_of_includes_os=set()
        a_rpkg.tree_of_includes_dep=set()

        # Check if the package is having an OS equivalent.
        if self.debug>3:
            print("Checking depend_mk_system_pkg")
            print(a_rpkg.depend_mk_system_pkg)

        if not len(a_rpkg.depend_mk_system_pkg)==0:
            a_rpkg.tree_of_includes_os.add(a_rpkg.depend_mk_system_pkg[0][1])
            return

        # Deal with direct robotpkg dependencies
        for lincludes_dep_group,lincludes_dep_name in a_rpkg.includes_depend:

            # If the package was found
            if lincludes_dep_name in self.package_dict.keys():
                # Includes robotpkg dependencies
                self.build_tree_of_dependencies(self.package_dict[lincludes_dep_name])

                if len(self.package_dict[lincludes_dep_name].tree_of_includes_os)==0:
                    a_rpkg.tree_of_includes_dep.add(lincludes_dep_name)

                a_rpkg.tree_of_includes_dep = \
                  a_rpkg.tree_of_includes_dep.union(self.package_dict[lincludes_dep_name].tree_of_includes_dep)
                a_rpkg.tree_of_includes_os = \
                  a_rpkg.tree_of_includes_os.union(self.package_dict[lincludes_dep_name].tree_of_includes_os)
            else:
                print("Did not find "+lincludes_dep_name)


        if self.debug>3:
            print("build_tree_of_dependencies: " +a_rpkg.name)
            print("robotpkg dep:")
            print(a_rpkg.tree_of_includes_dep)
            print("OS dep:")
            print(a_rpkg.tree_of_includes_os)

    def save(self,filename):
        """ Save list of packages with information in JSON format.
        """
        f=open(filename,'w')
        for pkg_name,a_rpkg in self.package_dict.items():
            a_rpkg.save(f)
        f.close()

    def provides_org_version(self,organization_name):
        """ This function returns a list of packages for a given organization
        More precisely each node contains a package name and a version number
        """
        dict_for_org={}
        # Iterates over the dictionnary of package
        for a_pack in self.package_dict.values():
            # If it has the org_name field
            if hasattr(a_pack,'org_name'):
                # If it is not empty
                if len(a_pack.org_name)!=0:
                    # Check the organization name
                    if organization_name==a_pack.org_name[0]:
                        # If the package has a version field
                        if hasattr(a_pack,'version'):
                            # If the version field is not empty
                            if len(a_pack.version)!=0:
                                dict_for_org[a_pack.name]= \
                                    [ a_pack.version[0] ]
                            else:
                                dict_for_org[a_pack.name].version = ""
                        else:
                            dict_for_org[a_pack.name].version = ""
                    # The organization is not present
                # org_name is empty
            # No org_name
        return dict_for_org

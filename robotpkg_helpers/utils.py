import os
import subprocess

def execute_capture_output(bashCommand,filename,lenv,debug=0):
    """ Execute baschCommand 
    
    Keyword arguments:
    bashCommand -- the bashCommand to be run in a bash script
    
    It returns a list of binary string that can be iterate 
    and decode.
    
    """
    # TODO: Handle error
    if debug>3:
        print("execute bash command: "+bashCommand)
    with open(filename,'w') as output:
        process = subprocess.check_call(bashCommand.split(),
                    stdout=output,
                    env=lenv)
    return ""

def execute(bashCommand, lenv, debug=0):
    """ Execute baschCommand 
    
    Keyword arguments:
    bashCommand -- the bashCommand to be run in a bash script
    
    It returns a list of binary string that can be iterate 
    and decode.
    
    """
    # TODO: Handle error
    if debug>3:
        print("execute bash command: "+bashCommand)
    process = subprocess.Popen(bashCommand.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               env=lenv)
    outputdata, error = process.communicate()
    if debug>3:
        for stdout_line in outputdata.splitlines():
            print(stdout_line.decode('utf-8'))
    return outputdata,error

def execute_call(bashCommand, debug=0):
    """ Execute baschCommand 
        
    Keyword arguments:
    bashCommand -- the bashCommand to be run in a bash script
    
    It returns a list of binary string that can be iterate 
    and decode.
    
    """
    if debug>3:
        print("execute bash command: "+bashCommand)
    return subprocess.call(bashCommand,shell=True)

def build_test_rc_robotpkg_vars(ROBOTPKG_ROOT=None):
    """ Build a dictionnary of basic robotpkg variables for a standard test_rc setup
    """
    import os
    if ROBOTPKG_ROOT==None:
        env_vars=os.environ.copy()
        ROBOTPKG_ROOT=env_vars["HOME"]+'/devel-src/robotpkg-test-rc'
        user=env_vars["USER"]


    robotpkg_vars={}
    robotpkg_vars['ROOT']=ROBOTPKG_ROOT
    robotpkg_vars['SRC']=robotpkg_vars['ROOT']+'/robotpkg'
    robotpkg_vars['ROOT']=robotpkg_vars['ROOT']+'/install'
    robotpkg_vars['DISTFILES']=robotpkg_vars['SRC']+'/distfiles'
    return robotpkg_vars

def add_robotpkg_mng_variables(anObject, ROBOTPKG_MNG_ROOT=None):
    """ This function adds robotpkg_mng_vars to the object based on ROBOTPKG_MNG_ROOT
    if provided.

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
    anObject.robotpkg_mng_vars['ARCH_DISTFILES']=anObject.robotpkg_mng_vars['ROOT']+'/arch_distfiles'
    anObject.robotpkg_mng_vars['RAMFS_MNT_PT']=anObject.robotpkg_mng_vars['ROOT']+'/robotpkg-test-rc'
    anObject.robotpkg_mng_vars['ROBOTPKG_ROOT']=anObject.robotpkg_mng_vars['RAMFS_MNT_PT']
    anObject.robotpkg_mng_vars['ARCHIVES']=anObject.robotpkg_mng_vars['ROOT']+'/archives'
    anObject.robotpkg_mng_vars['ROBOTPKG_BASE']=anObject.robotpkg_mng_vars['RAMFS_MNT_PT']+'/install'
    anObject.robotpkg_mng_vars['ROBOTPKG_SRC']=anObject.robotpkg_mng_vars['RAMFS_MNT_PT']+'/robotpkg'


def init_environment_variables(anObject, ROBOTPKG_ROOT):
    """ Populate the object with the environment variables.
    
    Specifies the environment when starting bash commands
    """
    anObject.ROBOTPKG_ROOT = ROBOTPKG_ROOT
    anObject.env = os.environ.copy()
    ROBOTPKG_BASE = anObject.ROBOTPKG_ROOT+'/install'
    anObject.env["ROBOTPKG_BASE"] = ROBOTPKG_BASE
    # Imposes bash as the shell
    anObject.env["SHELL"] = "/usr/bin/bash"
    # For binaries
    anObject.env["PATH"] = ROBOTPKG_BASE+'/sbin:' + \
                       ROBOTPKG_BASE+'/bin:'+anObject.env["PATH"]
    
    # For libraries
    prev_LD_LIBRARY_PATH=''
    if "LD_LIBRARY_PATH" in anObject.env:
        prev_LD_LIBRARY_PATH = anObject.env["LD_LIBRARY_PATH"]
    anObject.env["LD_LIBRARY_PATH"] = ROBOTPKG_BASE+'/lib:' \
        +ROBOTPKG_BASE+'/lib/plugin:' \
        +ROBOTPKG_BASE+'/lib64:' \
        +prev_LD_LIBRARY_PATH
        
    # For python
    prev_PYTHON_PATH=''
    if "PYTHON_PATH" in anObject.env:
        prev_PYTHON_PATH = anObject.env["PYTHON_PATH"]
    anObject.env["PYTHON_PATH"]=ROBOTPKG_BASE+'/lib/python2.7/site-packages:' \
        +ROBOTPKG_BASE+'/lib/python2.7/dist-packages:' \
        +prev_PYTHON_PATH
        
    # For pkgconfig
    prev_PKG_CONFIG_PATH=''
    if "PKG_CONFIG_PATH" in anObject.env:
        prev_PKG_CONFIG_PATH = anObject.env["PKG_CONFIG_PATH"]

    anObject.env["PKG_CONFIG_PATH"]=ROBOTPKG_BASE+'/lib/pkgconfig:' \
        +prev_PKG_CONFIG_PATH
        
    # For ros packages
    prev_ROS_PACKAGE_PATH=''
    if "ROS_PACKAGE_PATH" in anObject.env:
        prev_ROS_PACKAGE_PATH = anObject.env["ROS_PACKAGE_PATH"]
        
    anObject.env["ROS_PACKAGE_PATH"]=ROBOTPKG_BASE+'/share:' \
        +ROBOTPKG_BASE+'/stacks' \
        +prev_ROS_PACKAGE_PATH
        
    # For cmake
    prev_CMAKE_PREFIX_PATH=''
    if "CMAKE_PREFIX_PATH" in anObject.env:
        prev_CMAKE_PREFIX_PATH = anObject.env["CMAKE_PREFIX_PATH"]
            
    anObject.env["CMAKE_PREFIX_PATH"]=ROBOTPKG_BASE+':'+prev_CMAKE_PREFIX_PATH

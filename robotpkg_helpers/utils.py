import subprocess

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
                               env=lenv)
    outputdata, error = process.communicate()
    if debug>3:
        for stdout_line in outputdata.splitlines():
            print(stdout_line.decode('utf-8'))
    return outputdata

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



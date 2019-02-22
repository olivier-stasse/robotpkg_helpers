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

def build_test_rc_robotpkg_vars():
    """ Build a dictionnary of basic robotpkg variables for a standard test_rc setup
    """
    import os
    env_vars=os.environ.copy()
    root_devel_src=env_vars["HOME"]+'/devel-src/robotpkg_ws'
    user=env_vars["USER"]

    robotpkg_vars={}
    robotpkg_vars['ROOT']=root_devel_src+'/robotpkg-test-rc'
    robotpkg_vars['SRC']=robotpkg_vars['ROOT']+'/robotpkg'
    robotpkg_vars['DISTFILES']=robotpkg_vars['SRC']+'/distfiles'
    return robotpkg_vars


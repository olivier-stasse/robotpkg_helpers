# Author: O. Stasse
# See LICENSE.txt in root
# Copyright CNRS

import os
import datetime

class AnalyzeComputer:
    """ Analyzes the computer and extract the OS version
    """ 

    def __init__(self):
        self.find_and_analyze_lsb_release()
        self.lookup_ros_distrib()
        
    def find_and_analyze_lsb_release(self):
        """ This method reads the file /etc/lsb-release
        and creates a dictionary of all present variables
        """
        # Search for lsb-release file
        lsb_release_str="/etc/lsb-release"
        if os.path.exists(lsb_release_str):
            # If it exists 
            self.lsb_release = {}
            with open(lsb_release_str) as f:
                content = f.readlines()
                # Read the variables inside it
                for aline in content:
                    varname, varvalue = aline.split('=')
                    self.lsb_release[varname] = varvalue.replace('\n','')
            f.close()

    def lookup_ros_distrib(self):
        """ This method lookup the ros distrib with the ubuntu distrib
        """
        if 'DISTRIB_CODENAME' in self.lsb_release:
            ubuntu_distrib=self.lsb_release['DISTRIB_CODENAME']
            # Following REP 3 http://wiki.ros.org/Distributions
            if ubuntu_distrib=='xenial':
                self.ros_distrib='kinetic'
            elif ubuntu_distrib=='bionic':
                self.ros_distrib='melodic'
                
            

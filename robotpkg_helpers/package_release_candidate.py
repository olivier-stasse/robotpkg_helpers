# Author: O. Stasse
# See LICENSE.txt in root
# Copyright CNRS

import os
import json

class RobotpkgPkgReleaseCandidate:

    def __init__(self, name=None,
                 git_repo=None, commit=None, branch=None,tag=None):
        self.description={}
        self.description['git_repo']=git_repo
        self.description['commit']=commit
        self.description['branch']=branch
        self.description['tag']=tag
        self.description['name']=name

    def save(self,filename):
        f=open(filename,'w')
        json.dump(self.description,f)
        f.close()

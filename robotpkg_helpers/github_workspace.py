# Author: O. Stasse
# See LICENSE.txt in root
# Copyright CNRS
import os

from github import Github


class ReportsFromGithub:

    def __init__(self):
        env_vars=os.environ.copy()
        self.g = Github(env_vars["GITHUB_PRIVATE_TOKEN"])
        self.github_dict_of_repos={}
        
    def reading_repos_from_github_for_sot(self):
        # Using an access token
        print(dir(self.g))
        for repo in self.g.get_user().get_repos():
            print(repo.name)
            #self.github_dict_of_repos[repo.name]


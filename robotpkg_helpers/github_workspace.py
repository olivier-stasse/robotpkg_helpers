# Author: O. Stasse
# See LICENSE.txt in root
# Copyright CNRS


from github import Github

class ReportsFromGithub:

    def __init__(self):
        
    def reading_repos_from_github_for_sot(self):
        # Using an access token
        env_vars=os.environ.copy()
        g = Github(env_vers["GITHUB_PRIVATE_TOKEN"])
        print(dir(g))
        for repo in g.get_repos.list(user='stack-of-tasks').all():
            print(repo.name)
            self.github_dict_of_repos[repo.name]
            print(dir(repo))


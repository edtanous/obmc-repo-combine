#!/usr/bin/env python3
from github import Github
import os
import pygit2
import join_git_repos

# g = Github("access_token")

g = Github()

try:
    os.mkdir("repos")
except FileExistsError:
    pass


class MyRemoteCallbacks(pygit2.RemoteCallbacks):
    def transfer_progress(self, stats):
        print(f"{stats.indexed_objects}/{stats.total_objects}")


denylist = ["linux", "u-boot", "openbmc"]
repolist = []
for repo in g.get_organization("openbmc").get_repos():
    if repo.name in denylist:
        continue
    repodir = os.path.join("repos", repo.name)
    if not os.path.exists(repodir):
        pygit2.clone_repository(repo.clone_url, repodir, callbacks=MyRemoteCallbacks())
    print(repo.name)
    repolist.append(repodir)

no_subdirs = False
join_git_repos.main("repos/dbus-sensors", no_subdirs, ["repos/bmcweb"], "output")

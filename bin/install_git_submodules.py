import os
import re
import subprocess

configuration = open(os.path.join(os.environ.get('BUILD_DIR'), '.gitmodules'))

class module:
    name = ""
    path = ""
    url = ""

    def is_defined(self):
        return (self.name and self.path and self.url)

    def clear(self):
        self.name = ""
        self.path = ""
        self.url = ""

    def load(self):
        ps = subprocess.Popen(["git", "clone", "-q", self.url, self.path],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.environ.get('BUILD_DIR'),
                              shell=False)
        result, stderr = ps.communicate()
        if stderr:
            print("-----> " + stderr.decode('utf-8', errors='ignore'))
            print("\tSkipping submodule '{}' import".format(self.name))
        else:
            # Removing submodule .git folder"
            os.system('rm -rf ' + os.path.join(os.environ.get('BUILD_DIR'), self.path, '.git'))

submodule = module()
for line in configuration:
    submodule_search = re.search('^\[submodule\s"(.+)"', line)
    if submodule_search:
        submodule.name = submodule_search.group(1)
    else:
        path_search = re.search('\s*path.\s*=\s*(.*)', line)
        if path_search:
            submodule.path = path_search.group(1)
        else:
            url_search = re.search('\s*url.\s*=\s*(.*)', line)
            if url_search:
                submodule.url = url_search.group(1)
    if submodule.is_defined():
        print("-----> Loading submodule " + submodule.name)
        submodule.load()
        submodule.clear()
configuration.close()
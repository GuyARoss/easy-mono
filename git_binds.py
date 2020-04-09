import subprocess

def git_addall(path):
    p = subprocess.Popen("cd ./{}".format(path).split(), stdout=subprocess.PIPE)
    p = subprocess.Popen("git add .".format(path).split(), stdout=subprocess.PIPE)
    p = subprocess.Popen("git status".format(path).split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    sha = out.strip()

def git_commit(msg):
    p = subprocess.Popen('git commit -m {}'.format(msg).split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    sha = out.strip()

def git_push(branch):
    p = subprocess.Popen("git push origin {}".format(branch).split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    sha = out.strip()
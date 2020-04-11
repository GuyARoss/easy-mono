#!/usr/bin/python

'''
Fetches, unzips & reorgs the repos.
'''
import os, json, requests, shutil, zipfile, glob, resource

import git

# create structure
def build_directories(schema, base_path, paths = {}):
    for f in schema:
        if type(f) is dict:
            for k in f:
                paths = build_directories(f[k], "{}/{}".format(base_path,k), paths)
        else:
            paths[f] = "{}/{}".format(base_path, f)

    return paths

def load_manifest():
    with open('manifest.json', 'r') as myfile:
        data = myfile.read()

    return json.loads(data)

def download(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

def move_create_dir(src, dst):
    if os.path.isdir(dst) == False:
        if "." in dst:
            ea = dst.split('/')
            for i in range(len(ea) - 1):
                t = "/".join(ea[0:i + 1])

                if not os.path.exists(t):
                    os.mkdir(t)

    shutil.move(src, dst)

def create_repo(man, paths):
    # we get the files first
    for proj in man['projects']:
        archive_link = "{}/archive/master.zip".format(proj['url']) # @@ different branches
        
        b_path = "temp/{}".format(proj['key'])
        download(archive_link, b_path) # @@ replace this for a git process, that returns the repos in an arr.

        # we reorg by unzippn
        with zipfile.ZipFile(b_path, 'r') as zip_ref:
            zip_ref.extractall("temp")

        os.remove(b_path)
    
        key = ""
        if bool(proj["shallow"]) is False:
            key = paths[proj['key']]
        else:
            key = "temp2"

        sp_url = proj['url'].split('/')

        src = "temp/{}-master".format(sp_url[len(sp_url) -1]) # @@ support 4 branch

        files = os.listdir(src)
        for f in files:
            np = key + "/"+ f
            move_create_dir("{}/{}".format(src, f), np)

def main():
    man = load_manifest()

    repo = git.Repo.clone_from(man['remote'], 'temp2')
    cleanup_gitdir("temp2")

    pths = build_directories(man['schema'], "temp2")
    create_repo(man, pths) # build da mono repo.

    repo.git.add('--all')
    repo.index.commit("mono repo mirror commit") # @@? 
    origin = repo.remote(name='origin')
    origin.push()

    # temp cleanup
    for f in os.listdir("temp"):
        if ".git" not in f :
            fp = "temp/{}".format(f)
            if os.path.isfile(fp):
                os.remove(fp)
            else: 
                shutil.rmtree(fp)

    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000 / 1000) # meg
            
def cleanup(temp_partition):
    for p in temp_partition:
        if os.path.exists(p):
            shutil.rmtree(p)

def cleanup_gitdir(path):
    for f in os.listdir(path):
        if ".git" not in f :
            fp = "{}/{}".format(path, f)
            if os.path.isfile(fp):
                os.remove(fp)
            else: 
                shutil.rmtree(fp)

if __name__ == "__main__":
    temp_partition = ['temp', 'temp2']
    cleanup(temp_partition) 

    for p in temp_partition:
        if not os.path.exists(p):
            os.mkdir(p)

    main()

    # cleanup(temp_partition)
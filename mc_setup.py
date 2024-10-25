import urllib.request
import zipfile
import os
import shutil
import stat
import re
import subprocess

def unzip_server(file):
    print ("Unzipping Server")
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall("./server/")
    return

def download_server(url, destination):
    print ("Downloading the latestd Minecraft Bedrock Server")
    urllib.request.urlretrieve (url, destination)
    return

def setup_files(data_dir):
    print("Setting up files")
    os.chmod("./server/bedrock_server", 0o755)
    os.makedirs("./server/worlds", exist_ok=True)
    os.makedirs(data_dir+"/level", exist_ok=True)
    os.makedirs(data_dir+"/backups/", exist_ok=True)

    if not os.path.islink("./server/worlds/Bedrock level"):
        os.symlink(data_dir+"/level", "./server/worlds/Bedrock level")

    if not os.path.exists(data_dir+"/server.properties"):
        print("Moving server.properties into data directory")
        shutil.move("./server/server.properties", data_dir+"/server.properties")
    else:
        os.remove("./server/server.properties")

    os.symlink(data_dir+"/server.properties", "./server/server.properties")

def report_ids(msg):
    print ('uid, gid = %d, %d; %s' % (os.getuid(), os.getgid(), msg))

def demote(user_uid, user_gid):
    report_ids('starting demotion')
    os.setgid(user_gid)
    os.setuid(user_uid)
    report_ids('finished demotion')

def grab_download_url(download_page):

    html = subprocess.run(['./version.sh', download_page], stdout=subprocess.PIPE, encoding="utf-8").stdout
    print ("read : ")
    #print (html)
    urlMatcher = re.search("(https://www.minecraft.net/bedrockdedicatedserver/bin-linux/[^\"]*)", html)
    if urlMatcher is None:
        print("Cannot find the version url - maybe download failed?")
        print (html)
    return urlMatcher.group()

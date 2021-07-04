import urllib.request
import zipfile
import os
import shutil
import stat
import re

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
    req = urllib.request.Request(
        download_page, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        urlMatcher = re.search("(https://minecraft.azureedge.net/bin-linux/[^\"]*)", html)
        if urlMatcher is None:
            print("Cannot find the version url - maybe download failed?")
            print (html)
        return urlMatcher.group()

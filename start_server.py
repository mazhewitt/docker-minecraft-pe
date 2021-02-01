#!/usr/bin/python3

import urllib.request
import zipfile
import os
import shutil
import stat

def unzip_server(file):
    print ("Unzipping Server")
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall("./server/")
    return

def download_server(url, destination):
    print ("Downloading the latestd Minecraft Bedrock Server")
    urllib.request.urlretrieve (url, destination)
    return


download_url = "https://minecraft.azureedge.net/bin-linux/bedrock-server-1.16.201.02.zip"
server_zip = "downloads/server.zip"
data_dir = "/mc-data"

if os.path.exists("./server"):
    shutil.rmtree("./server")
    os.makedirs("./server")

download_server(download_url, server_zip)
unzip_server(server_zip)

print("Setting up files")

os.chmod("./server/bedrock_server", 0o755)

os.makedirs("./server/worlds", exist_ok=True)
os.makedirs(data_dir+"/level", exist_ok=True)

if not os.path.islink("./server/worlds/Bedrock level"):
    os.symlink(data_dir+"/level", "./server/worlds/Bedrock level")

if not os.path.exists(data_dir+"/server.properties"):
    print("Moving server.properties into data directory")
    os.rename("./server/server.properties", data_dir+"/server.properties")
else:
    os.remove("./server/server.properties")

os.symlink(data_dir+"/server.properties", "./server/server.properties")

os.environ["LD_LIBRARY_PATH"] = "./server"
print("Starting Server")
os.chdir("./server/")
os.execl("./bedrock_server", "./bedrock_server")
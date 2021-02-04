#!/usr/local/bin/python3

import urllib.request
import zipfile
import os
import shutil
import stat
import re
import mc_setup

download_url = mc_setup.grab_download_url("https://www.minecraft.net/en-us/download/server/bedrock/")
server_zip = "downloads/server.zip"
data_dir = "/mc-data"

if os.path.exists("./server"):
    shutil.rmtree("./server")
os.makedirs("./server")

stat = os.stat(data_dir)
uid = stat.st_uid
gid = stat.st_gid
os.chown("./server", uid, gid)
os.chown("./downloads", uid, gid)
mc_setup.demote(uid, gid)

mc_setup.download_server(download_url, server_zip)
mc_setup.unzip_server(server_zip)
mc_setup.setup_files(download_url, server_zip, data_dir)

os.environ["LD_LIBRARY_PATH"] = "$LD_LIBRARY_PATH:./server"
print("Starting Server")
os.chdir("./server/")

os.execl("./bedrock_server", "./bedrock_server")
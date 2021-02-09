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
server_dir = "./server"
download_dir = "./downloads"

if os.path.isfile(server_zip):
    shutil.rmtree(server_zip)

if os.path.exists(server_dir):
    shutil.rmtree(server_dir)
os.makedirs(server_dir)

os.system("/usr/sbin/cron&")

stat = os.stat(data_dir)
uid = stat.st_uid
gid = stat.st_gid
os.chown(server_dir, uid, gid)
os.chown(download_dir, uid, gid)
mc_setup.demote(uid, gid)

mc_setup.download_server(download_url, server_zip)
mc_setup.unzip_server(server_zip)
mc_setup.setup_files(data_dir)

os.environ["LD_LIBRARY_PATH"] = "$LD_LIBRARY_PATH:./server"
print("Starting Server")
os.chdir(server_dir)

os.execl("./bedrock_server", "./bedrock_server")
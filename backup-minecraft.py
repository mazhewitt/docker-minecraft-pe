#!/usr/local/bin/python3

import os
import time
import tarfile
import datetime
import mc_setup

def make_tarfile(filename, source_dir):
    with tarfile.open(filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def removẹ_OldFiles(path):
    now = time.time()
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.stat(f).st_mtime < now - 7 * 86400:
            if os.path.isfile(f):
                os.remove(f)


minecraft_dir = "/mc-data/"
backup_dir = minecraft_dir+"/backups/"
stat = os.stat(backup_dir)
uid = stat.st_uid
gid = stat.st_gid

mc_setup.demote(uid, gid)

now = datetime.datetime.now()
filename = now.strftime("%Y.%m.%d.%H.%M.%S.tar.gz")
backup_name = backup_dir + filename
make_tarfile(backup_name, minecraft_dir + "/level/")
removẹ_OldFiles(backup_dir)







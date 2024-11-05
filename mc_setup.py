import requests
from tqdm import tqdm
import zipfile
import os
import shutil

import re
import subprocess
import certifi

def unzip_server(file):
    print ("Unzipping Server")
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall("./server/")
    return

def download_server(url, destination):
    print(f"Starting download from: {url}")

    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        # Adding headers to the request to mimic a web browser
        with requests.get(url, stream=True, headers=headers, verify=False) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024  # 1 Kilobyte
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    progress_bar.update(len(chunk))
                    f.write(chunk)

            progress_bar.close()
            print(f"Download completed: {destination}")

    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}")

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

# To use:

*  Download the docker image
*  Add a user to run the server as
*  Start the server
*  The server will download the latest minecraft pe from MS
*  The data files will be kept in /home/minecraft/server

```
docker pull mazhewitt/docker-minecraft-pe
sudo useradd -m minecraft
sudo mkdir /home/minecraft/server
sudo chown -r minecraft:minecraft /home/minecraft/server
docker run --name minecraft_server --restart unless-stopped -dit  -p 19132:19132/udp -v /home/minecraft/server:/mc-data mazhewitt/docker-minecraft-pe:1.0
```
The server by default will start a server in Easy Survival


To change the mode:
* Stop the server 

```
docker stop minecraft_server
```

* Edit the "/home/minecraft/server/server.properties" file, change survival to creative, or easy to hard
**do not change the level name**
* Start the server again

```
docker start minecraft_server
```

* The server is backed up to the backups folder ever 4 hours
* To restore a backup:
    * Stop the server
    * Remove the contents of the level directory
    * restore the archive into the level directory

```
sudo su minecraft
tar -zxvf /home/minecraft/server/backups/2021.01.20.00.00.01.tar.gz /home/minecraft/server/level
```

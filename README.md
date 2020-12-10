# Python cloud storage
This improved version of https://github.com/MaEvGoR/python_cloud_storage with architectural changes.

## Running
To launch DFS, you should specify addresses and ports for client, namenode and datanodes in python files, and then you can launch Docker images.\
Client
```
sudo docker run -p 1234:1234 -p 9899:9899 -p 20002:20002 dmmc123/client:v9
```
Namenode
```
docker run -p 2345:2345 -p 20001:20001 -p 20002:20002 dmmc123/namenode:v13
```
Datanode 1
```
docker run -p 20001:20001 -p 20002:20002 -p 9899:9899 dmmc123/datanode1:v16
```
Datanode 2
```
docker run -p 20003:20003 -p 20004:20004 -p 9899:9899 dmmc123/datanode2:v2
```
echo -e "\nStopping containers ....."
docker stop $(docker ps -a | grep kafka1 | cut -d ' ' -f 1)
docker stop $(docker ps -a | grep kafka2 | cut -d ' ' -f 1)
docker stop $(docker ps -a | grep kafka3 | cut -d ' ' -f 1)
docker stop $(docker ps -a | grep zookeeper | cut -d ' ' -f 1)
docker stop $(docker ps -a | grep akhq | cut -d ' ' -f 1)
docker rm kafka1
docker rm kafka2
docker rm kafka3
docker rm zookeeper
docker rm akhq
rm -rf kafka1
rm -rf kafka2
rm -rf kafka3
mkdir kafka1
mkdir kafka2
mkdir kafka3
chmod 777 kafka1
chmod 777 kafka2
chmod 777 kafka3
echo -e "\nAll Containers stopped."
echo -e "\nStopping containers ....."
docker stop $(docker ps -a | grep kafka | cut -d ' ' -f 1)
docker stop $(docker ps -a | grep zookeeper | cut -d ' ' -f 1)
docker stop $(docker ps -a | grep akhq | cut -d ' ' -f 1)
docker rm kafka
docker rm zookeeper
docker rm akhq
rm -rf kafka
mkdir kafka
chmod 777 kafka
echo -e "\nAll Containers stopped."
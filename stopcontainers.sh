echo -e "\nStopping containers ....."
docker stop $(docker ps -a | grep zookeeper | cut -d ' ' -f 1)
docker stop $(docker ps -a | grep akhq | cut -d ' ' -f 1)
docker rm zookeeper
docker rm akhq
for i in 1 2 3; do
  docker stop $(docker ps -a | grep broker$i | cut -d ' ' -f 1)
  docker rm broker$i
  rm -rf broker$i
  mkdir broker$i
  chmod 777 broker$i
done
echo -e "\nAll Containers stopped."
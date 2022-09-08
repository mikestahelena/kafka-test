echo -e "\nStarting containers ....."
rm -rf kafka1
rm -rf kafka2
rm -rf kafka3
mkdir kafka1
mkdir kafka2
mkdir kafka3
chmod 777 kafka1
chmod 777 kafka2
chmod 777 kafka3
docker compose up -d
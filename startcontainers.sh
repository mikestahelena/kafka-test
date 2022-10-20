echo -e "\nStarting containers ....."
for i in 1 2 3; do
  rm -rf broker$i
  mkdir broker$i
  chmod 777 broker$i
done
docker compose up -d

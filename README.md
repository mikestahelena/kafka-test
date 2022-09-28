# kafka-tests

## _Projeto para explorar as funcionalidades do Kafka com Python_

# Parte 1 - kafka cli #


Conceder permissão de escrita para o diretório do kafka
```bash
sudo chmod 777 -R kafka/
```

Subir container
```bash
docker compose up -d
```

Listar os containers
```bash
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}'
```

Versão do Kafka
```bash
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 --version
```

Alternativamente pode abrir o bash no container e executar os comandos diretamente nele
```bash
docker-compose exec kafka bash
```

Criar tópico
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic message-tests --if-not-exists
```

Abrir [AKHQ][akhq] e verificar o tópico criado 

Describe do tópico
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic message-tests
```

Listar tópicos
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list
```

Conectar no Zookeeper pelo script do kafka
```bash
docker exec kafka zookeeper-shell zookeeper:2181
```
Exemplos de comandos do zookeeper:
* id do cluster do Kafka - get /cluster/id
* listar brokers - ls /brokers/ids
* listar tópicos - ls /brokers/topics
* detalhes de um tópico - get /brokers/topics/message-tests

Alterar tópico message-tests para 3 partições
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --alter --topic message-tests --partitions=3
```

Alterar configuração de retenção do tópico para 1 minuto = 60000 milissegundos (gambiarra para expurgar o tópico) / 1 hora = 3600000 milissegundos
```bash
docker exec kafka kafka-configs --bootstrap-server localhost:9092 --alter --entity-type topics \
  --entity-name message-tests \
  --add-config retention.ms=60000
```

Deletar configuração de retenção do tópico (gambiarra para expurgar o tópico)
```bash
docker exec kafka kafka-configs --bootstrap-server localhost:9092 --alter --entity-type topics \
  --entity-name message-tests \
  --delete-config retention.ms
```

Listar os tópicos com alteração na configuração
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --describe --topics-with-overrides
```

Describe de um tópico específico com alteração na configuração
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --describe --entity-type topics --entity-name message-tests
```

Criar producer
```bash
docker exec --interactive --tty kafka kafka-console-producer --bootstrap-server localhost:9092 --topic message-tests \
  --property parse.key=true \
  --property key.separator=":"
``` 

Publicar mensagem no tópico message-tests a partir de arquivo
```bash
docker-compose exec kafka bash -c \
  "cat /etc/kafka/data/data1.txt | kafka-console-producer --bootstrap-server localhost:9092 --topic message-tests \
  --property parse.key=true \
  --property key.separator=:"
```

Criar consumer
```bash
docker exec --interactive --tty kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic message-tests \
  --from-beginning \
  --formatter kafka.tools.DefaultMessageFormatter \
  --property "print.timestamp=true" \
  --property "print.offset=true" \
  --property "print.partition=true" \
  --property "print.key=true" \
  --property "print.value=true"
```

Mostrar o offset do tópico message-tests
```bash
docker exec kafka kafka-run-class kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic message-tests
```

Criar consumer definindo o consumer group (abrir 3 terminais e executar o comando abaixo em cada um)
```bash
docker exec --interactive --tty kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic message-tests \
  --from-beginning \
  --group message-tests-consumers \
  --formatter kafka.tools.DefaultMessageFormatter \
  --property "print.timestamp=true" \
  --property "print.offset=true" \
  --property "print.partition=true" \
  --property "print.key=true" \
  --property "print.value=true"
```

Listar consumer groups
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list
```

Reset offset to the earliest
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --group message-tests-consumers \
  --reset-offsets \
  --all-topics \
  --to-earliest \
  --execute
```

Reset offset to date time
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --group message-tests-consumers \
  --reset-offsets \
  --all-topics \
  --to-datetime 2022-07-08T15:00:00.000 \
  --execute
```

Describe a consumer group for topic message-tests
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group message-tests-consumers
```

Describe all consumer groups
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --all-groups
```

Rebalance topic partition message-tests consumer-group message-tests-consumers (corrigir)
```bash
docker exec kafka kafka-reassign-partitions --bootstrap-server localhost:9092 --execute \
  --reassignment-json-file ./reassignment.json \
  --throttle 1000
``` 

Deletar tópico
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --delete --topic message-tests
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. 
There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
[akhq]: <http://localhost:8080>

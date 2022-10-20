# kafka-tests

# Parte 1 - kafka cli #


Criar diretórios para armazenar os dados do Kafka, conceder permissão de escrita e subir os containers
```bash
sudo ./startcontainers.sh
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
docker exec broker1 kafka-broker-api-versions --bootstrap-server localhost:9092 --version
```

Alternativamente pode abrir o bash no container e executar os comandos diretamente nele
```bash
docker-compose exec broker1 bash
```

Criar tópico
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --create --topic message-tests
```

Listar tópicos
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --list
```

Abrir [AKHQ][akhq] e verificar o tópico criado 

Describe do tópico
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --describe --topic message-tests
```
- ***PartitionCount***: Quantidade de partições do tópico (paralelismo)
- ***ReplicationFactor***: Quantidade de réplicas do tópico (redundância)
- ***Leader***: Node responsável por ler e escrever as operações de uma determinada partição
- ***Replicas***: Lista de brokers replicando os dados deste tópico
- ***Isr***: Lista de nodes que são réplicas sincronizadas (in-sync replicas)

Alterar tópico message-tests para 3 partições (paralelismo)
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --alter --topic message-tests --partitions=3
```

Alterar tópico message-tests para 3 réplicas (redundância)
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --alter --topic message-tests --partitions=3 --replication-factor=3
```
***Erro***: 
> Option "[replication-factor]" can't be used with option "[alter]"

Depois de criado o tópico, o número de réplicas só pode ser alterado via reatribuição de partições

Aumentar o número de réplicas para 3 através de reatribuição de partições
```bash
docker exec broker1 kafka-reassign-partitions --bootstrap-server localhost:29092 --execute \
  --reassignment-json-file /etc/kafka/data/increase-replication-factor.json \
  --throttle 1000
``` 

Criar tópico com 3 partições e 3 réplicas
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --create --topic redundancy-tests3 \
  --partitions 3 --replication-factor 5
```
***Erro***:
> Error while executing topic command : Replication factor: 5 larger than available brokers: 3.

O valor máximo de replicações é o número de brokers


Alterar configuração de retenção do tópico para 1 minuto = 60000 milissegundos (gambiarra para expurgar o tópico) / 1 hora = 3600000 milissegundos
```bash
docker exec broker1 kafka-configs --bootstrap-server localhost:29092 --alter --entity-type topics \
  --entity-name message-tests \
  --add-config retention.ms=60000
```

Deletar configuração de retenção do tópico (gambiarra para expurgar o tópico)
```bash
docker exec broker1 kafka-configs --bootstrap-server localhost:29092 --alter --entity-type topics \
  --entity-name message-tests \
  --delete-config retention.ms
```

Listar os tópicos com alteração na configuração
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --describe --topics-with-overrides
```

Describe de um tópico específico com alteração na configuração
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --describe --entity-type topics --entity-name message-tests
```

Criar producer
```bash
docker exec --interactive --tty broker1 kafka-console-producer --bootstrap-server localhost:29092 --topic message-tests \
  --property parse.key=true \
  --property key.separator=":"
``` 

Publicar mensagem no tópico message-tests a partir de arquivo
```bash
docker exec broker1 bash -c \
  "cat /etc/kafka/data/data1.txt | kafka-console-producer --bootstrap-server localhost:29092 --topic message-tests \
  --property parse.key=true \
  --property key.separator=:"
```

Criar consumer
```bash
docker exec --interactive --tty broker1 kafka-console-consumer --bootstrap-server localhost:29092 --topic message-tests \
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
docker exec broker1 kafka-run-class kafka.tools.GetOffsetShell --broker-list localhost:29092 --topic message-tests
```

Criar consumer definindo o consumer group (abrir 3 terminais e executar o comando abaixo em cada um)
```bash
docker exec --interactive --tty broker1 kafka-console-consumer --bootstrap-server localhost:29092 --topic message-tests \
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
docker exec broker1 kafka-consumer-groups --bootstrap-server localhost:29092 --list
```

Reset offset to the earliest
```bash
docker exec broker1 kafka-consumer-groups --bootstrap-server localhost:29092 --group message-tests-consumers \
  --reset-offsets \
  --all-topics \
  --to-earliest \
  --execute
```

Reset offset to date time
```bash
docker exec broker1 kafka-consumer-groups --bootstrap-server localhost:29092 --group message-tests-consumers \
  --reset-offsets \
  --all-topics \
  --to-datetime 2022-07-08T15:00:00.000 \
  --execute
```

Describe a consumer group for topic message-tests
```bash
docker exec broker1 kafka-consumer-groups --bootstrap-server localhost:29092 --describe --group message-tests-consumers
```

Describe all consumer groups
```bash
docker exec broker1 kafka-consumer-groups --bootstrap-server localhost:29092 --describe --all-groups
```

Rebalance topic partition message-tests consumer-group message-tests-consumers
```bash
docker exec broker1 kafka-reassign-partitions --bootstrap-server localhost:29092 --execute \
  --reassignment-json-file /etc/kafka/data/reassignment.json \
  --throttle 1000
``` 

```bash
docker exec broker1 kafka-reassign-partitions --bootstrap-server localhost:29092 --verify \
  --reassignment-json-file /etc/kafka/data/reassignment.json
```
```bash
docker exec broker1 kafka-reassign-partitions --bootstrap-server localhost:29092 --broker-list 29092, 29093, 29094 --generate \
  --topics-to-move-json-file /etc/kafka/data/reassignment.json
```

Deletar tópico
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --delete --topic message-tests
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. 
There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
[akhq]: <http://localhost:8080>

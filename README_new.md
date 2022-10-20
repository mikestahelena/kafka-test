Abrir [AKHQ][akhq] e verificar o cluster

Criar tópico
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --create --topic message-tests
```

Listar tópicos
```bash
docker exec broker1 kafka-topics --bootstrap-server localhost:29092 --list
```

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

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. 
There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
[akhq]: <http://localhost:8080>
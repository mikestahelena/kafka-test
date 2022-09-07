# kafka-tests

## _Projeto para explorar as funcionalidades do Kafka com Python_

# Parte 2 #

Criar virtualenv e instalar dependências
```bash
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

Criar novo tópico com 3 partições 
```bash
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic customer-registration --partitions 3 --replication-factor 1
```



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. 
[//]: # (There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. 
There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
[akhq]: <http://localhost:8080>
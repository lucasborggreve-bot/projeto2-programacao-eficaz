# Projeto 2 - Programação Eficaz

## Feito por Lucas Borggreve e Rafael Duarte

Para acessar a api:

http://3.93.196.154

## Rotas

Listar todos os imóveis com todos os seus atributos:
```'/imoveis'``` (GET)

Listar um imóvel específico pelo seu id com todos os seus atributos:
```'/imoveis/<id>'``` (GET)

Adicionar um novo imóvel:
```'/imoveis'``` (POST)
enviar um json

Atualizar um imóvel existente:
```'imoveis/<id>'``` (PUT)
enviar o novo json


Remover um imóvel existente:
```'/imoveis/<id>'``` (DELETE)

Buscar imóveis por tipo (casa, apartamento, terreno, etc) com todos os seus atributos:
```'/imoveis/tipo/<escreva aqui>'``` (GET)

Buscar imóveis por cidade com todos os seus atributos:
```'/imoveis/cidade/<escreva aqui>'``` (GET)
# Ponderada 1 - Implementação de uma API

Este repositório contém a implementação de uma API para a Ponderada 1 do modulo 10 de EC.

## Collections do Insomnia para testar a API

Para facilitar o teste e a interação com a API, foram criadas collections do Insomnia. As collections contêm requisições pré-configuradas para as principais operações da API. Você pode importar o  arquivo 'insomnia-collections' e começar a testar imediatamente.

## YAML do OpenAPI (Swagger) para documentar a API

A documentação da API está disponível em formato YAML do OpenAPI (Swagger), no arquivo 'swagger-endpoint'. Nele há descrito os endpoints disponíveis, os parâmetros necessários e as respostas esperadas para cada operação da API.

## Código fonte da API

O código fonte da API se encontra na pasta 'src'

## Instruções para executar a API

Para executar a API localmente:

- Após clonar o repositório vá até a pasta src
- Instale todas as dependencias com o comando abaixo:
  ```
  python -m pip install -r requirements.txt
  ```
- Execute o arquivo main:
  ```
  python -m flask --app main run
  ```
- Uma vez que o servidor esteja em execução, você pode enviar requisições para os endpoints especificados na documentação.

## 2° Parte da Atividade - Desenvolvimento de API Assincrona

Para esse Backend assincrono, que tem o mesmo objetivo do primeiro desenvolvido, gerenciar um sistema de To-Dos. Porém nessa aplicaçõa foi utilizado FastAPI com chamadas asincronas

## Instruções para executar a API

Para executar a API localmente, execute o comando na mesma pasta que se encontra o Dockerfile da aplicaçao assincrona:

```
docker build -t ponderada1 .
docker run --rm -p 8000:8000 ponderada1
```
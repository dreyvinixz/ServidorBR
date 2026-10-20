# Requisitos do Projeto — ServidorBR

## 1. Visão Geral

O **ServidorBR** é uma aplicação Full Stack destinada à consulta de informações de servidores ativos e aposentados do Poder Executivo Federal.

A aplicação utilizará dados públicos disponibilizados pelo **Portal Brasileiro de Dados Abertos — dados.gov.br**, armazenando e processando essas informações em um banco de dados PostgreSQL.

O sistema deverá permitir consultas por nome, cargo, unidade federativa e órgão/instituição, além de buscas combinadas e buscas por similaridade.

O projeto será desenvolvido em equipe utilizando práticas de desenvolvimento colaborativo, versionamento com Git/GitHub, metodologia ágil e arquitetura baseada em containers Docker.

---

# 2. Objetivos

O projeto possui como principais objetivos:

- desenvolver uma aplicação Full Stack;
- implementar uma API REST utilizando Python e Flask;
- disponibilizar uma interface Web para consulta dos dados;
- utilizar PostgreSQL como banco de dados;
- utilizar Docker para modularizar os serviços;
- permitir consultas rápidas em grandes volumes de dados;
- implementar busca por similaridade;
- proteger a aplicação contra entradas inválidas e ataques comuns;
- suportar múltiplas requisições simultâneas;
- utilizar GitHub durante todo o processo de desenvolvimento;
- documentar tarefas, commits e evolução do projeto;
- realizar testes funcionais e testes de carga.

---

# 3. Fontes de Dados

A aplicação utilizará os seguintes conjuntos de dados disponibilizados pelo Governo Federal:

## 3.1 Gestão de Pessoas do Executivo Federal — Aposentados

Fonte:

```text
https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados
```

## 3.2 Gestão de Pessoas do Executivo Federal — Carreiras/Cargos

Fonte:

```text
https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---carreiras--cargos
```

Os dados deverão ser analisados de acordo com seus respectivos dicionários de dados antes da importação.

---

# 4. Arquitetura

A aplicação deverá ser composta por três serviços principais.

```text
┌───────────────────┐
│     Frontend      │
│ React / Web App   │
└─────────┬─────────┘
          │ HTTP
          ▼
┌───────────────────┐
│      Backend      │
│ Flask + Gunicorn  │
└─────────┬─────────┘
          │ SQL
          ▼
┌───────────────────┐
│    PostgreSQL     │
│    db-server      │
└───────────────────┘
```

Os três serviços deverão ser executados utilizando Docker.

Containers obrigatórios:

```text
frontend
backend
db
```

---

# 5. Tecnologias

## 5.1 Backend

Tecnologias obrigatórias:

- Python;
- Flask;
- Gunicorn;
- API REST;
- JSON.

Tecnologias adicionais previstas:

- SQLAlchemy;
- Psycopg;
- Flask-Limiter;
- Pytest.

---

## 5.2 Banco de Dados

Banco obrigatório:

- PostgreSQL.

Recursos previstos:

- índices B-Tree;
- índices GIN;
- extensão `pg_trgm`;
- consultas parametrizadas;
- pool de conexões;
- timeout de consultas;
- normalização dos campos pesquisáveis.

---

## 5.3 Frontend

Tecnologias:

- HTML;
- CSS;
- JavaScript;
- React;
- Vite.

O frontend deverá consumir exclusivamente a API disponibilizada pelo backend.

---

## 5.4 Infraestrutura

- Docker;
- Docker Compose;
- Dockerfile;
- Git;
- GitHub.

---

# 6. Estrutura Esperada

A estrutura mínima do projeto deverá seguir:

```text
projeto/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
│
├── db/
│   ├── init/
│   ├── etl/
│   ├── data/
│   └── Dockerfile
│
├── docs/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── REQUISITOS.md
```

---

# 7. Requisitos Funcionais

## RF01 — Busca por Nome Exato

O sistema deverá permitir pesquisar um servidor utilizando seu nome.

Exemplo:

```http
GET /api/servidores?nome=JOAO DA SILVA
```

O sistema deverá retornar os registros encontrados em formato JSON.

---

## RF02 — Busca por Similaridade de Nome

O sistema deverá permitir pesquisar servidores utilizando correspondência parcial ou similaridade textual.

Exemplos:

```text
%JOAO%SILVA%
JOAO SILVA%
JOAO%SILVA
```

Endpoint esperado:

```http
GET /api/servidores?similar=JOAO SILVA&limit=100
```

O sistema deverá aceitar um limite máximo de resultados.

O limite máximo permitido deverá ser:

```text
100 registros
```

---

## RF03 — Busca por Cargo ou Profissão

O sistema deverá permitir pesquisar servidores pelo cargo ou profissão.

Exemplo:

```http
GET /api/servidores?cargo=PROFESSOR
```

---

## RF04 — Busca por Unidade Federativa

O sistema deverá permitir pesquisar servidores por Unidade Federativa.

Exemplo:

```http
GET /api/servidores?uf=RS
```

Somente UFs brasileiras válidas deverão ser aceitas.

---

## RF05 — Busca por Órgão ou Instituição

O usuário deverá poder pesquisar registros associados a determinado órgão ou instituição.

Exemplo:

```http
GET /api/servidores?orgao=UNIVERSIDADE
```

---

## RF06 — Busca Combinada

O sistema deverá permitir combinar múltiplos filtros.

Exemplo:

```http
GET /api/servidores?cargo=PROFESSOR&uf=RS
```

Também deverão ser permitidas consultas como:

```http
GET /api/servidores?nome=JOAO&cargo=PROFESSOR&uf=RS
```

ou:

```http
GET /api/servidores?orgao=UNIVERSIDADE&uf=RS
```

---

## RF07 — Paginação

Quando houver múltiplos registros, os resultados deverão ser paginados.

Exemplo:

```http
GET /api/servidores?cargo=PROFESSOR&page=2&per_page=25
```

A resposta deverá conter informações sobre a paginação.

Exemplo:

```json
{
  "data": [],
  "pagination": {
    "page": 2,
    "per_page": 25,
    "total": 183,
    "pages": 8
  }
}
```

---

## RF08 — Exibição de Resultado Único

Caso uma consulta retorne apenas um registro, o frontend deverá apresentar suas informações de maneira detalhada.

---

## RF09 — Exibição de Múltiplos Resultados

Quando houver múltiplos registros, o frontend deverá apresentar os resultados de forma organizada e paginada.

---

## RF10 — API JSON

Todos os endpoints da API deverão responder utilizando JSON.

Exemplo:

```json
{
  "data": [
    {
      "id": 1,
      "nome": "JOAO DA SILVA",
      "cargo": "PROFESSOR",
      "uf": "RS",
      "orgao": "UNIVERSIDADE FEDERAL"
    }
  ]
}
```

---

# 8. Requisitos do Backend

## RB01 — Python

O backend deverá ser desenvolvido obrigatoriamente utilizando Python.

---

## RB02 — Flask

O framework web utilizado no backend deverá ser obrigatoriamente Flask.

---

## RB03 — Gunicorn

A aplicação Flask deverá ser executada utilizando o servidor WSGI Gunicorn.

Exemplo de configuração:

```bash
gunicorn \
  --workers 2 \
  --threads 4 \
  --worker-class gthread \
  --timeout 15 \
  --bind 0.0.0.0:8000 \
  "app:create_app()"
```

O servidor de desenvolvimento interno do Flask não deverá ser utilizado como servidor principal da aplicação final.

---

## RB04 — Concorrência

O Gunicorn deverá utilizar workers e/ou threads para possibilitar atendimento simultâneo de múltiplas requisições.

---

## RB05 — Validação dos Parâmetros

Todos os parâmetros recebidos pela API deverão ser validados antes da execução da consulta.

Deverão ser validados:

- nome;
- cargo;
- órgão;
- UF;
- página;
- quantidade por página;
- limite;
- parâmetros de similaridade.

---

## RB06 — Parâmetros Desconhecidos

Parâmetros não suportados pela API deverão gerar resposta de erro apropriada.

Exemplo:

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Parâmetro de busca inválido."
  }
}
```

---

# 9. Requisitos do Banco de Dados

## RDB01 — PostgreSQL

O banco de dados deverá utilizar obrigatoriamente PostgreSQL.

---

## RDB02 — Persistência

O container PostgreSQL deverá utilizar volume Docker para impedir perda dos dados quando o container for reiniciado.

---

## RDB03 — Importação dos Dados

A equipe deverá desenvolver um processo de ETL para:

1. carregar os arquivos provenientes do Portal de Dados Abertos;
2. validar os dados;
3. remover ou tratar registros inválidos;
4. normalizar campos;
5. importar os dados para PostgreSQL.

---

## RDB04 — Normalização de Texto

Campos utilizados para pesquisa deverão possuir versões normalizadas.

Exemplo:

```text
Entrada:

José da Silva Júnior

Normalizado:

JOSE DA SILVA JUNIOR
```

A normalização poderá incluir:

- remoção de acentos;
- conversão para maiúsculas;
- remoção de espaços duplicados;
- remoção de espaços no início/fim.

---

## RDB05 — Índices

O banco deverá utilizar índices para melhorar o desempenho das pesquisas.

Deverão ser considerados índices para:

- nome;
- cargo;
- UF;
- órgão;
- combinações de filtros.

---

## RDB06 — Busca por Similaridade

O PostgreSQL deverá utilizar mecanismos eficientes de similaridade textual.

Será utilizada preferencialmente a extensão:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

Poderá ser utilizado índice GIN.

Exemplo:

```sql
CREATE INDEX idx_servidor_nome_trgm
ON servidores
USING GIN (nome_normalizado gin_trgm_ops);
```

---

# 10. Segurança

## RS01 — Proteção Contra SQL Injection

Todas as consultas SQL deverão utilizar parâmetros.

Não será permitido concatenar diretamente dados fornecidos pelo usuário em comandos SQL.

Incorreto:

```python
query = f"SELECT * FROM servidores WHERE nome = '{nome}'"
```

Correto:

```python
query = """
SELECT *
FROM servidores
WHERE nome_normalizado = :nome
"""
```

---

## RS02 — Validação de UF

Somente UFs brasileiras válidas serão aceitas.

```text
AC AL AP AM BA CE DF ES GO MA
MT MS MG PA PB PR PE PI RJ RN
RS RO RR SC SP SE TO
```

---

## RS03 — Limite de Resultados

A API deverá limitar a quantidade máxima de registros retornados por requisição.

```text
MAX_LIMIT = 100
```

---

## RS04 — Rate Limiting

O backend deverá possuir mecanismo para limitar excesso de requisições realizadas por um mesmo cliente.

Caso o limite seja excedido, deverá retornar:

```http
HTTP 429 Too Many Requests
```

---

## RS05 — Timeout

Consultas que ultrapassarem o tempo máximo configurado deverão ser interrompidas.

O backend deverá tratar essa situação sem bloquear permanentemente workers do servidor.

---

## RS06 — Tratamento de Erros

Erros internos não deverão apresentar informações sensíveis.

Não deverão ser retornados ao usuário:

- stack trace;
- credenciais;
- connection strings;
- senha do banco;
- variáveis internas;
- detalhes da infraestrutura.

---

# 11. Códigos HTTP

A API deverá utilizar códigos HTTP adequados.

| Situação                         | Código |
| -------------------------------- | -----: |
| Requisição realizada com sucesso |    200 |
| Parâmetro inválido               |    400 |
| Página/recurso inexistente       |    404 |
| Limite de requisições excedido   |    429 |
| Timeout temporário               |    503 |
| Erro interno                     |    500 |

Uma busca válida sem resultados poderá retornar:

```http
200 OK
```

com:

```json
{
  "data": [],
  "pagination": {
    "total": 0
  }
}
```

---

# 12. Requisitos do Frontend

## RFE01 — Interface Web

A aplicação deverá possuir uma interface Web moderna utilizando HTML, CSS e JavaScript.

---

## RFE02 — Consumo da API

O frontend deverá obter os dados por meio de requisições HTTP ao backend Flask.

---

## RFE03 — Formulário de Busca

O sistema deverá possuir campos para:

- nome;
- cargo;
- UF;
- órgão;
- similaridade.

---

## RFE04 — Busca Avançada

O usuário deverá poder combinar diferentes filtros simultaneamente.

---

## RFE05 — Resultados

Os resultados deverão apresentar, quando disponíveis:

- nome;
- cargo;
- profissão;
- UF;
- órgão;
- instituição;
- demais informações relevantes provenientes da base.

---

## RFE06 — Paginação

O frontend deverá permitir navegar entre páginas de resultados.

Exemplo:

```text
Anterior | 1 | 2 | 3 | 4 | Próxima
```

---

## RFE07 — Responsividade

A interface deverá funcionar adequadamente em diferentes tamanhos de tela.

---

## RFE08 — Estados da Interface

O frontend deverá possuir estados visuais para:

- carregamento;
- sucesso;
- nenhum resultado;
- erro;
- timeout;
- excesso de requisições.

---

# 13. Docker

## RD01 — Containers

Deverão existir no mínimo três containers:

```text
frontend
backend
db
```

---

## RD02 — Dockerfile Backend

O backend deverá possuir seu próprio:

```text
backend/Dockerfile
```

---

## RD03 — Dockerfile Frontend

O frontend deverá possuir seu próprio:

```text
frontend/Dockerfile
```

---

## RD04 — Docker Compose

A raiz do projeto deverá possuir:

```text
docker-compose.yml
```

---

## RD05 — Inicialização

Todo o ambiente deverá ser inicializado utilizando:

```bash
docker compose up --build
```

Após a execução desse comando, os serviços necessários deverão iniciar automaticamente.

---

## RD06 — Comunicação Interna

Os containers deverão se comunicar utilizando a rede gerenciada pelo Docker Compose.

O backend deverá acessar o banco utilizando o nome do serviço do PostgreSQL, e não `localhost`.

Exemplo:

```text
postgresql://usuario:senha@db:5432/servidorbr
```

---

## RD07 — Healthcheck

Deverão ser utilizados healthchecks sempre que possível.

O backend deverá aguardar o banco estar disponível antes de iniciar sua operação normal.

---

# 14. Requisitos de Desempenho

## RP01 — Consultas Indexadas

As consultas principais deverão utilizar índices do PostgreSQL sempre que possível.

---

## RP02 — Paginação Obrigatória

Consultas que possam retornar grande quantidade de registros não deverão retornar todos os dados em uma única requisição.

---

## RP03 — Testes de Carga

A equipe deverá executar testes de carga simulando múltiplos clientes simultâneos.

Sugestão de cenários:

```text
10 usuários
25 usuários
50 usuários
100 usuários
200 usuários
```

---

## RP04 — Métricas

Durante os testes deverão ser observadas métricas como:

- requisições por segundo;
- latência média;
- P50;
- P95;
- P99;
- número de erros;
- número de timeouts;
- uso de CPU;
- uso de memória.

---

## RP05 — Proteção Contra Sobrecarga

O sistema deverá possuir mecanismos para impedir que requisições excessivas provoquem indisponibilidade completa da aplicação.

---

# 15. Testes

## RT01 — Testes do Backend

Deverão existir testes para:

- busca por nome;
- busca por cargo;
- busca por UF;
- busca por órgão;
- busca combinada;
- busca por similaridade;
- paginação.

---

## RT02 — Testes de Validação

Deverão existir testes para:

- UF inválida;
- limite inválido;
- página inválida;
- parâmetros desconhecidos;
- strings excessivamente grandes;
- parâmetros vazios.

---

## RT03 — Testes de Segurança

Deverão ser testadas entradas contendo possíveis tentativas de SQL Injection.

Exemplos:

```text
' OR 1=1 --
```

```text
'; DROP TABLE servidores; --
```

A aplicação deverá interpretar esses valores apenas como dados de entrada, sem executar comandos SQL provenientes do usuário.

---

## RT04 — Testes de Carga

A API deverá ser submetida a testes concorrentes antes da entrega.

Ferramentas sugeridas:

- Locust;
- Apache Bench;
- k6.

---

# 16. Git e GitHub

## RG01 — Versionamento

O uso do GitHub é obrigatório durante todo o desenvolvimento.

---

## RG02 — Histórico de Commits

Cada integrante deverá realizar commits utilizando sua própria conta.

Os commits deverão representar trabalho real realizado durante o projeto.

---

## RG03 — Padronização de Commits

Preferencialmente utilizar Conventional Commits.

Exemplos:

```text
feat(api): add search by state

feat(db): add trigram index for employee names

feat(frontend): implement advanced search form

fix(api): validate invalid UF parameter

test(api): add combined filter tests

docs: update project requirements
```

---

## RG04 — Branches

Sugestão de branches:

```text
main
develop

feat/database-schema
feat/data-import
feat/api-search
feat/api-similarity
feat/frontend-search
feat/docker

test/load-testing
```

---

## RG05 — Pull Requests

Mudanças significativas deverão preferencialmente passar por Pull Request antes de serem integradas à branch principal.

---

# 17. Metodologia Ágil

O desenvolvimento deverá utilizar uma metodologia ágil.

Deverão ser registradas:

- tarefas;
- responsáveis;
- status;
- estimativas;
- dificuldades;
- impedimentos.

Status sugeridos:

```text
Backlog
Todo
In Progress
Review
Done
```

---

# 18. Burndown

As tarefas poderão receber Story Points.

Exemplo inicial:

| Atividade              | Pontos |
| ---------------------- | -----: |
| Modelagem do banco     |      5 |
| ETL                    |      8 |
| Importação dos dados   |      5 |
| API base               |      5 |
| Filtros                |      8 |
| Busca por similaridade |      5 |
| Segurança              |      5 |
| Docker                 |      5 |
| Frontend               |     13 |
| Testes                 |      8 |
| Documentação           |      5 |

A quantidade de pontos restantes deverá ser registrada durante o desenvolvimento para geração do gráfico de burndown.

---

# 19. Documentação

O projeto deverá possuir documentação contendo:

- descrição do projeto;
- arquitetura;
- tecnologias utilizadas;
- instruções de instalação;
- instruções de execução;
- estrutura do banco;
- endpoints;
- exemplos de requisições;
- exemplos de respostas;
- estratégia de segurança;
- testes realizados;
- divisão das tarefas;
- dificuldades encontradas;
- limitações do sistema.

---

# 20. Endpoint de Health Check

O backend deverá disponibilizar um endpoint para verificar se a aplicação está operacional.

```http
GET /api/health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

Opcionalmente:

```json
{
  "status": "ok",
  "database": "connected",
  "service": "servidorbr-api"
}
```

---

# 21. Variáveis de Ambiente

Credenciais e configurações sensíveis não deverão ser armazenadas diretamente no código.

Deverá existir um arquivo:

```text
.env.example
```

Exemplo:

```env
POSTGRES_DB=servidorbr
POSTGRES_USER=servidorbr
POSTGRES_PASSWORD=change_me

DATABASE_URL=postgresql://servidorbr:change_me@db:5432/servidorbr

FLASK_ENV=production
API_PORT=8000
```

O arquivo `.env` real deverá estar presente no `.gitignore`.

---

# 22. Critérios de Aceitação

O projeto será considerado funcional quando:

- [ ] `docker compose up --build` iniciar toda a aplicação;
- [ ] o container PostgreSQL iniciar corretamente;
- [ ] o container backend iniciar utilizando Gunicorn;
- [ ] o container frontend iniciar corretamente;
- [ ] o frontend conseguir se comunicar com a API;
- [ ] a busca por nome funcionar;
- [ ] a busca por similaridade funcionar;
- [ ] a busca por cargo funcionar;
- [ ] a busca por UF funcionar;
- [ ] a busca por órgão funcionar;
- [ ] filtros combinados funcionarem;
- [ ] paginação funcionar;
- [ ] a API retornar JSON válido;
- [ ] entradas inválidas forem tratadas;
- [ ] tentativas de SQL Injection forem neutralizadas;
- [ ] houver limitação de requisições;
- [ ] houver timeout configurado;
- [ ] forem realizados testes de carga;
- [ ] os principais endpoints possuírem testes;
- [ ] o histórico do GitHub demonstrar participação da equipe;
- [ ] o relatório apresentar a divisão das tarefas;
- [ ] existir gráfico de burndown;
- [ ] a documentação explicar como executar o projeto.

---

# 23. Funcionalidade Adicional

Após todos os requisitos obrigatórios estarem concluídos, poderá ser desenvolvida uma aplicação Desktop utilizando:

- Python;
- PyQt;
- PySide;
- Tkinter;
- Toga/BeeWare.

A aplicação Desktop deverá consumir a mesma API Flask utilizada pelo frontend Web.

O desenvolvimento Desktop será considerado uma funcionalidade adicional e não deverá comprometer a implementação dos requisitos obrigatórios.

---

# 24. Prioridades

## P0 — Obrigatório

- PostgreSQL;
- Flask;
- Gunicorn;
- Docker;
- Docker Compose;
- API;
- filtros;
- similaridade;
- paginação;
- validação;
- frontend;
- GitHub;
- testes básicos.

## P1 — Importante

- rate limiting;
- testes de carga;
- healthcheck;
- métricas;
- otimização de índices;
- CI.

## P2 — Adicional

- aplicativo Desktop;
- dashboards administrativos;
- métricas avançadas;
- funcionalidades que não façam parte diretamente do escopo obrigatório.

---

# 25. Definição de Pronto — Definition of Done

Uma tarefa será considerada concluída quando:

1. estiver implementada;
2. estiver funcional;
3. não quebrar funcionalidades existentes;
4. possuir testes quando aplicável;
5. tiver sido commitada no Git;
6. estiver associada a uma Issue ou tarefa;
7. estiver revisada;
8. tiver documentação atualizada quando necessário;
9. estiver integrada à aplicação principal.

---

## Projeto

**ServidorBR**

Aplicação Full Stack para consulta de informações de servidores do Poder Executivo Federal.

## Prazo de entrega

```text
13/10/2026
```

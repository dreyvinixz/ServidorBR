# ServidorBR

Aplicação full stack para consulta de informações públicas de servidores ativos e aposentados do Poder Executivo Federal.

O projeto será desenvolvido por uma equipe de três integrantes, com Python/Flask/Gunicorn no backend, PostgreSQL no banco e React no frontend. A execução final utilizará Docker Compose com os serviços `frontend`, `backend` e `db`.

> Status atual: planejamento e especificações concluídos. A implementação será iniciada conforme as tasks e sprints documentadas; os comandos de execução abaixo só estarão disponíveis após a conclusão da infraestrutura da Sprint 1.

## Objetivos

- Consultar servidores por nome, cargo/profissão, UF e órgão/instituição.
- Permitir filtros combinados, paginação e busca por similaridade de nome.
- Proteger a API com validação, consultas parametrizadas, rate limiting e timeout.
- Manter dados tratados em PostgreSQL, com índices para buscas eficientes.
- Oferecer uma interface responsiva que consome exclusivamente a API REST.

## Arquitetura planejada

```text
Navegador
    |
    v
Frontend (React + Vite + Nginx) --- /api ---> Backend (Flask + Gunicorn)
                                                    |
                                                    v
                                      PostgreSQL + pg_trgm (container db)
```

## Tecnologias

| Camada | Tecnologias |
| --- | --- |
| Frontend | React, Vite, HTML, CSS, JavaScript, Nginx |
| Backend | Python, Flask, Gunicorn, SQLAlchemy |
| Banco de dados | PostgreSQL, `pg_trgm`, índices B-Tree e GIN |
| Infraestrutura | Docker, Docker Compose, GitHub Actions |
| Qualidade | Pytest, Locust, Pull Requests e revisão de código |

## Funcionalidades previstas

- Busca exata por nome;
- busca parcial e por similaridade, limitada a 100 registros;
- busca por cargo/profissão, UF e órgão/instituição;
- combinação de filtros;
- paginação de resultados;
- apresentação detalhada quando houver um único resultado;
- endpoint de saúde: `GET /api/health`;
- respostas JSON e erros HTTP padronizados;
- validação de parâmetros, proteção contra SQL injection, rate limiting e timeout.

## Planejamento e equipe

O plano prevê duas sprints de 15 dias. As tarefas devem ser executadas e registradas com datas, commits e Pull Requests reais.

- [Roadmap](ROADMAP.md): visão do produto, sprints, especificações, documentação e critérios de aceite.
- [Tasks](TASK.md): divisão rotativa para três desenvolvedores, tasks `SB-01` a `SB-21`, branches e revisão obrigatória.
- [Guia de contribuição](CONTRIBUTING.md): fluxo de Issues, branches, Pull Requests e revisão.
- [Documentação](docs/README.md): índice dos documentos técnicos e evidências do projeto.
- [Requisitos completos](REQUERIMENTS.md): requisitos funcionais e não funcionais da disciplina.

## Fluxo de desenvolvimento

Cada sprint terá uma branch de integração distinta:

```text
main
  ├── sprint/01-fundacao-api
  └── sprint/02-experiencia-entrega
```

Cada task será desenvolvida em uma branch criada a partir da branch da sprint, como `feat/SB-07-api-filtros`. Todo Pull Request deverá:

1. estar vinculado a uma Issue `SB-XX`;
2. apontar para a branch da sprint correspondente;
3. ter pelo menos uma aprovação de revisor diferente do autor;
4. ter testes relevantes aprovados;
5. atualizar a documentação quando necessário.

Padrão de commit:

```text
tipo(escopo): resumo objetivo [SB-XX]
```

Exemplo: `feat(api): add validated UF filter [SB-07]`.

## Estrutura prevista

```text
servidorbr/
├── backend/              # Flask, Gunicorn, testes e Dockerfile
├── frontend/             # React/Vite, Nginx e Dockerfile
├── db/                   # scripts SQL, ETL e arquivos de dados locais
├── docs/                 # arquitetura, API, ETL, segurança e relatório
├── ROADMAP.md            # planejamento das sprints
├── TASK.md               # tarefas e responsáveis
├── REQUERIMENTS.md       # requisitos do trabalho
├── docker-compose.yml    # criado na Sprint 1
└── README.md
```

## Como executar (quando a Sprint 1 estiver concluída)

### Pré-requisitos

- Docker Desktop com Docker Compose;
- Git;
- acesso aos CSVs públicos usados pelo ETL, quando necessário.

### Inicialização

```bash
git clone <URL_DO_REPOSITORIO>
cd servidorbr
cp .env.example .env
docker compose up --build
```

URLs previstas:

| Serviço | Endereço |
| --- | --- |
| Frontend | `http://localhost:3000` |
| API | `http://localhost:8000/api/health` |

> As portas definitivas serão confirmadas na task SB-10. Não versione o arquivo `.env`, senhas ou dados pessoais.

## Fontes de dados

- [Gestão de Pessoas do Executivo Federal - Aposentados](https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados)
- [Gestão de Pessoas do Executivo Federal - Carreiras/Cargos](https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---carreiras--cargos)

Os arquivos originais não serão enviados ao Git. O processo de análise, tratamento e importação será documentado em `docs/dados-e-etl.md` durante as tasks SB-02 e SB-05.

## Licença

Projeto acadêmico desenvolvido para a disciplina de Desenvolvimento de Sistemas.

# ServidorBR

Aplicação full stack para consulta de dados públicos de servidores aposentados do Poder Executivo Federal, com PostgreSQL, API Flask/Gunicorn e interface web HTML/CSS/JavaScript servida por Nginx.

O MVP local está implementado em 20/10/2026. A base inicia vazia; é necessário obter um CSV oficial e importá-lo. A fonte de aposentados não fornece UF no dicionário consultado, então esse filtro é explicitamente indisponível. O enunciado também exige uma equipe real de pelo menos três integrantes; commits de uma só pessoa não atendem esse item.


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
| Frontend | HTML, CSS, JavaScript, Nginx |
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

## Como executar

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
| Frontend e proxy da API | `http://localhost:3000` |
| Saúde da API | `http://localhost:3000/api/health` |

As credenciais de `.env.example` são apenas para desenvolvimento local. Troque-as antes de qualquer ambiente compartilhado. Não versione `.env` nem arquivos CSV.

### Importar uma base oficial

Coloque o CSV obtido de fonte oficial fora do Git e execute após iniciar os containers:

```bash
docker compose cp caminho/aposentados.csv backend:/tmp/aposentados.csv
docker compose exec backend python etl.py /tmp/aposentados.csv
```

O ETL lê colunas `Nome`, `Cargo` e `Nome do órgão`, ignora registros sem nome e não persiste CPF ou matrícula. A importação usa uma chave de conteúdo para ignorar duplicatas. Consulte [dados e ETL](docs/dados-e-etl.md).

### API

```text
GET /api/servidores?nome=JOAO%20DA%20SILVA
GET /api/servidores?cargo=PROFESSOR&orgao=UNIVERSIDADE&page=1&per_page=25
GET /api/servidores?similar=JOAO%25SILVA&limit=100
```

Nome é exato após normalização; cargo e órgão aceitam trecho. O filtro `uf` retorna `422 UF_UNAVAILABLE`, pois não está disponível na fonte escolhida. Veja o contrato completo em [docs/api.md](docs/api.md).

## Fontes de dados

- [Gestão de Pessoas do Executivo Federal - Aposentados](https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados)
- [Gestão de Pessoas do Executivo Federal - Carreiras/Cargos](https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---carreiras--cargos)

Os arquivos originais não serão enviados ao Git. O processo de análise, tratamento e importação será documentado em `docs/dados-e-etl.md` durante as tasks SB-02 e SB-05.

## Licença

Projeto acadêmico desenvolvido para a disciplina de Desenvolvimento de Sistemas.

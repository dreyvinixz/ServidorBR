# Testes e carga - ServidorBR

## Testes automatizados existentes

Com Python 3.12 e dependências instaladas:

```powershell
python -m pip install -r backend/requirements.txt
python -m unittest discover -s backend -p 'test_*.py'
```

Dezesseis casos passaram localmente na branch de fechamento. Além dos testes de API para normalização, parâmetros desconhecidos, UF, paginação, SQL injection, busca por similaridade e opções distintas do endpoint `/api/opcoes`, a suíte cobre contagens abaixo/acima do limite, linhas idênticas preservadas, reimportação idempotente, delimitadores `;`, `,` e tabulação, nome vazio rejeitado, formato oficial sem cabeçalho em CP1252, campo grande em coluna não pesquisada e exclusão de CPF/matrícula dos dados persistidos.

## Validação de configuração

`docker compose config -q` passou localmente em 20/10/2026. Os containers `db`, `backend` e `frontend` iniciaram e ficaram saudáveis; a página retornou HTTP 200 e `GET /api/health` pelo Nginx retornou `{"database":"ok","status":"ok"}`. Com as duas publicações importadas, a busca por `AGENTE ADMINISTRATIVO` retornou HTTP 200 com 35 correspondências; a consulta por similaridade retornou HTTP 200 com limite de 100 resultados.

## Medição local de consultas

Com 414.801 registros importados das duas publicações oficiais de 08/2025, o script `backend/benchmark_api.py --runs 20` executou 20 requisições sequenciais por cenário via Nginx em `http://localhost:3000` (sem concorrência). O cliente mede o tempo HTTP ponta a ponta no host Windows; cada busca retorna no máximo 1 registro. P99 com 20 amostras é apenas o maior valor observado e não estima cauda de produção. O cenário de similaridade respeita o limite da API e informa no máximo 100 resultados.

Medição em 20/10/2026:

| Cenário | Linhas correspondentes | Média | P50 | P95 | P99/maior |
|---|---:|---:|---:|---:|---:|
| Nome exato sem resultado | 0 | 214,291 ms | 27,976 ms | 294,127 ms | 2.864,741 ms |
| Cargo parcial | 35 | 21,295 ms | 15,715 ms | 32,950 ms | 81,264 ms |
| Órgão parcial | 188 | 53,991 ms | 17,573 ms | 117,539 ms | 508,722 ms |
| Similaridade de nome | 100 (limite) | 470,935 ms | 464,402 ms | 535,489 ms | 550,370 ms |

O cenário de similaridade revelou um erro Psycopg no operador `%` do `pg_trgm`, que retornava 503. O operador foi escapado como `%%` na consulta parametrizada e passou a ser coberto por teste de regressão; após a correção, as 20 amostras responderam com HTTP 200.

### Reavaliação após COUNT limitado

Na base local de 414.801 registros, o benchmark sequencial `backend/benchmark_api.py --runs 20` foi executado antes e em duas rodadas depois de limitar o `COUNT` da busca `similar`. Média/P50/P95 foram 467,657/458,078/508,740 ms antes; 360,438/337,995/463,395 ms na primeira rodada posterior; e 377,347/305,275/413,060 ms na segunda. O P99/maior foi 525,717 ms antes e 532,831/1.611,785 ms depois; com 20 amostras, P99 é o máximo observado. Os planos e a limitação da amostra estão detalhados em [`analise-busca-similaridade.md`](analise-busca-similaridade.md).

Esses números são a linha de base anterior à otimização, na fixture local completa; similaridade foi a consulta mais lenta, com P50 de 464 ms e P95 de 535 ms. Um teste observou um pico isolado de 2,865 s na busca exata sem resultado. Os valores não representam uma garantia de produção.

A análise inicial de `EXPLAIN (ANALYZE, BUFFERS)` para essa busca está em [`analise-busca-similaridade.md`](analise-busca-similaridade.md), junto à medição da consulta após limitar o `COUNT`.

## Carga concorrente

## Aplicativo desktop adicional

Em 20/10/2026, `desktop/npm ci`, `npm run check`, `npm audit` e `npm run package:win` foram executados em Windows. A auditoria reportou zero vulnerabilidades. O empacotamento gerou `desktop/release/ServidorBR-win32-x64/ServidorBR.exe`; a execução abriu a janela Electron com o título `ServidorBR — Consulta pública`. O app usa a API local do Compose, cujo healthcheck retornou HTTP 200. A inspeção visual do conteúdo da janela não foi possível porque o adaptador de navegador/desktop não estava disponível. O workflow CI Windows foi configurado para repetir o pacote e publicar a pasta como artefato.

O script `backend/benchmark_concurrent.py` executa buscas por similaridade em paralelo e coleta `docker stats` do backend, banco e frontend durante cada nível. Para reproduzir na stack local:

```powershell
python backend/benchmark_concurrent.py --levels 1,2,4,8 --requests 25 --stats-interval 0.5 --output docs/benchmark-concorrente-2026-10-20.json
```

Foi usado o cenário `similar=MARIA&limit=100&per_page=1`, com uma chamada de aquecimento e 25 requisições em cada nível (101 chamadas no total). A API expôs até 100 resultados por chamada. O volume tinha 414.801 registros e era uma fixture exploratória mista: 413.990 linhas do arquivo `_FULL` e 811 da publicação mensal. A regra canônica documentada posteriormente seleciona somente `_FULL`; portanto, este resultado preserva a composição usada na medição anterior, não uma reconstrução canônica.

Medição local em 20/10/2026:

| Concorrência | RPS | Média | P50 | P95 | P99/maior | HTTP 200 | Erros | CPU média/pico do banco | RAM máxima do banco |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,747 | 571,908 ms | 562,910 ms | 622,533 ms | 746,564 ms | 25/25 | 0 | 98,69% / 102,57% | 338,30 MiB |
| 2 | 2,918 | 664,687 ms | 644,369 ms | 823,892 ms | 836,547 ms | 25/25 | 0 | 196,58% / 200,13% | 341,90 MiB |
| 4 | 4,464 | 786,386 ms | 752,932 ms | 982,653 ms | 1.022,327 ms | 25/25 | 0 | 307,47% / 394,17% | 347,10 MiB |
| 8 | 4,131 | 1.243,185 ms | 1.126,815 ms | 1.946,416 ms | 2.126,200 ms | 25/25 | 0 | 377,03% / 610,37% | 354,80 MiB |

Todos os requests retornaram HTTP 200. Nesta rodada, a vazão máxima ocorreu em concorrência 4; elevar para 8 reduziu a vazão e elevou o P95 para 1,95 s enquanto o pico de CPU observado no banco chegou a 610%. Isso aponta saturação crescente do banco para esta consulta e máquina, mas uma rodada de 25 amostras por nível não constitui capacidade de produção. O P99 com 25 amostras é igual ao maior valor observado. `docker stats` foi amostrado durante as rodadas; as contagens de amostras e o [relatório JSON sem dados pessoais](benchmark-concorrente-2026-10-20.json) guardam os valores completos.

Após o `COUNT` limitado, a carga concorrente foi repetida nas mesmas condições e com 25 requisições por nível:

| Concorrência | RPS antes → depois | P50 antes → depois | P95 antes → depois | Erros depois |
|---:|---:|---:|---:|---:|
| 1 | 1,747 → 3,038 | 562,910 → 315,633 ms | 622,533 → 416,612 ms | 0/25 |
| 2 | 2,918 → 4,413 | 644,369 → 417,600 ms | 823,892 → 556,910 ms | 0/25 |
| 4 | 4,464 → 6,090 | 752,932 → 488,089 ms | 982,653 → 531,444 ms | 0/25 |
| 8 | 4,131 → 6,160 | 1.126,815 → 756,404 ms | 1.946,416 → 1.329,003 ms | 0/25 |

Após a mudança, a CPU do banco foi observada em média/pico de 97,34%/100,68%, 178,12%/195,05%, 207,19%/390,14% e 342,40%/684,81% para concorrência 1, 2, 4 e 8; a memória máxima ficou entre 337,90 e 354,60 MiB. A coleta teve de 2 a 4 amostras por nível, conforme duração, então os picos são observados e podem perder variações curtas. A vazão ficou praticamente estável entre 4 e 8 concorrentes, enquanto o P95 subiu de 531 ms para 1,329 s. Todas as 100 requisições tiveram sucesso. O artefato integral depois da alteração está em [`benchmark-concorrente-depois-count-limitado-2026-10-20.json`](benchmark-concorrente-depois-count-limitado-2026-10-20.json); o antes está no JSON acima.

Rate limit em memória, limite de consulta de 8 s e timeout Gunicorn de 15 s são configurações iniciais, não limites validados por benchmark.

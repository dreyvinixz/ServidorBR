# Segurança - ServidorBR

## Controles no código

| Risco | Controle | Limitação |
|---|---|---|
| SQL injection | Valores enviados como parâmetros Psycopg; fragmentos SQL são constantes do backend | Revisar qualquer consulta nova |
| Strings e filtros inválidos | Lista de parâmetros permitidos; limites de tamanho; validação de paginação/UF | Cargo e órgão são campos livres, sem catálogo de valores |
| Sobrecarga | Flask-Limiter: 120 solicitações/min por IP; Gunicorn com 2 workers/4 threads | Contadores em memória e isolados por processo/instância |
| Busca longa | PostgreSQL `statement_timeout=8000ms`; Gunicorn `timeout=15s` | Limites iniciais sem medição de carga real |
| Erro interno | JSON genérico ao cliente; exceções registradas no log do servidor | Controlar acesso e retenção dos logs |
| Dados pessoais | ETL descarta CPF e matrícula; API retorna nome, cargo, órgão e UF nullable | Arquivo CSV original ainda fica sob responsabilidade do operador |
| Credenciais | `.env` ignorado e `.env.example` versionado | Senha padrão de Compose é apenas para desenvolvimento local |

## UF ausente

UF válida retorna `422 UF_UNAVAILABLE`. A fonte consultada não traz UF e nenhuma localização é inferida por nome do órgão.

## Para ambiente compartilhado

Trocar senhas padrão, usar armazenamento compartilhado para rate limit, ativar HTTPS e configurar proxy confiável antes de publicar o serviço. O rate limit atual não substitui controles de borda em produção.

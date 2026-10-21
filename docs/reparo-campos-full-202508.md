# Reparo dos campos de cargo e órgão no FULL 08/2025

Em 20/10/2026, os campos `cargo`, `cargo_norm`, `orgao` e `orgao_norm` foram recuperados na tabela `servidores` usando a publicação oficial `APOSENTADOS_082025_FULL.csv`. A correspondência foi feita exclusivamente pela chave composta `(source_file, source_hash)`. Nenhuma linha foi inserida ou excluída.

Antes do `UPDATE`, a transação criou `public.servidores_full_fields_backup_20261020` com `id`, a chave composta e os valores originais dos quatro campos para as 413.990 linhas FULL. A tabela é permanente e deve ser preservada enquanto a reversão for necessária.

## Resultado conferido

| Verificação | Resultado |
|---|---:|
| Total de `servidores` | 414.801 |
| Linhas FULL 08/2025 | 413.990 |
| FULL com cargo preenchido | 413.920 |
| FULL com órgão preenchido | 413.990 |
| Linhas da extração mensal | 811 |
| Backup | 413.990 |
| Chaves FULL sem correspondência | 0 |

Os 70 cargos sem valor continuam nulos porque a publicação oficial não fornece cargo nessas linhas. A assinatura dos quatro campos das 811 linhas mensais foi comparada antes e depois da atualização.

## Procedimento reproduzível

`backend/repair_full_fields.py` baixa a fonte oficial, confere contagens e hashes e, por padrão, executa apenas o preflight. `--apply` habilita uma transação que cria o backup antes da atualização, prepara os valores em tabela temporária, atualiza somente os quatro campos e aborta se qualquer contagem, chave ou assinatura mensal divergir.

```powershell
docker compose exec backend python repair_full_fields.py
docker compose exec backend python repair_full_fields.py --apply
```

O script recusa aplicar se o estado atual não corresponder ao esperado ou se a tabela de backup já existir. Para uma nova recuperação, revisar e adaptar explicitamente a constante do backup e as contagens antes de executar.

## Reversão

Executar no PostgreSQL restaura os quatro campos originais pelas chaves gravadas no backup. O bloco exige exatamente 413.990 atualizações; qualquer diferença cancela a transação.

```sql
BEGIN;
DO $$
DECLARE
    affected integer;
BEGIN
    UPDATE servidores AS target
    SET cargo = backup.cargo,
        cargo_norm = backup.cargo_norm,
        orgao = backup.orgao,
        orgao_norm = backup.orgao_norm
    FROM public.servidores_full_fields_backup_20261020 AS backup
    WHERE target.source_file = backup.source_file
      AND target.source_hash = backup.source_hash
      AND target.id = backup.id;

    GET DIAGNOSTICS affected = ROW_COUNT;
    IF affected <> 413990 THEN
        RAISE EXCEPTION 'Reversão esperava 413990 linhas, atualizou %', affected;
    END IF;
END $$;
COMMIT;
```

Depois da reversão, conferir o total de 414.801, comparar os quatro campos FULL com a tabela de backup e confirmar que as 811 linhas mensais permanecem inalteradas.

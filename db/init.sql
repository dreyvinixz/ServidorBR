CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS servidores (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    nome_norm TEXT NOT NULL,
    cargo TEXT,
    cargo_norm TEXT NOT NULL DEFAULT '',
    orgao TEXT,
    orgao_norm TEXT NOT NULL DEFAULT '',
    uf CHAR(2),
    source_hash CHAR(64) UNIQUE NOT NULL,
    source_file TEXT NOT NULL,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_servidores_nome_norm ON servidores (nome_norm);
CREATE INDEX IF NOT EXISTS ix_servidores_cargo_norm ON servidores (cargo_norm);
CREATE INDEX IF NOT EXISTS ix_servidores_orgao_norm ON servidores (orgao_norm);
CREATE INDEX IF NOT EXISTS ix_servidores_nome_trgm ON servidores USING GIN (nome_norm gin_trgm_ops);
CREATE INDEX IF NOT EXISTS ix_servidores_cargo_trgm ON servidores USING GIN (cargo_norm gin_trgm_ops);
CREATE INDEX IF NOT EXISTS ix_servidores_orgao_trgm ON servidores USING GIN (orgao_norm gin_trgm_ops);

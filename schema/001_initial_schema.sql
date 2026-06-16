PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS volumes (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    sequence_no INTEGER NOT NULL UNIQUE,
    target_terms INTEGER NOT NULL CHECK (target_terms >= 0),
    purpose TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('planned', 'active', 'complete', 'deprecated')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    volume_id INTEGER NOT NULL REFERENCES volumes(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    description TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (volume_id, slug)
);

CREATE TABLE IF NOT EXISTS volume_relations (
    id INTEGER PRIMARY KEY,
    source_volume_id INTEGER NOT NULL REFERENCES volumes(id) ON DELETE CASCADE,
    target_volume_id INTEGER NOT NULL REFERENCES volumes(id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    rationale TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (source_volume_id, target_volume_id, relation_type)
);

CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY,
    term_uid TEXT NOT NULL UNIQUE,
    zh_term TEXT NOT NULL,
    en_term TEXT,
    volume_id INTEGER NOT NULL REFERENCES volumes(id) ON DELETE RESTRICT,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    definition_short TEXT,
    definition_long TEXT,
    visual_effect TEXT,
    prompt_usage TEXT,
    positive_prompt TEXT,
    negative_prompt TEXT,
    use_cases TEXT,
    source_refs TEXT,
    notes TEXT,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'review', 'published', 'deprecated')),
    version TEXT NOT NULL DEFAULT 'V1.0',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS term_aliases (
    id INTEGER PRIMARY KEY,
    term_id INTEGER NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    alias TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT 'mixed',
    UNIQUE (term_id, alias)
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS term_tags (
    term_id INTEGER NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (term_id, tag_id)
);

CREATE TABLE IF NOT EXISTS term_relations (
    id INTEGER PRIMARY KEY,
    source_term_id INTEGER NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    target_term_id INTEGER REFERENCES terms(id) ON DELETE CASCADE,
    target_label TEXT,
    note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (target_term_id IS NOT NULL OR target_label IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS term_chunks (
    id INTEGER PRIMARY KEY,
    chunk_uid TEXT NOT NULL UNIQUE,
    term_id INTEGER NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
    chunk_type TEXT NOT NULL,
    content TEXT NOT NULL,
    token_hint INTEGER,
    embedding_model TEXT,
    embedding_ref TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS import_runs (
    id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL UNIQUE,
    source_path TEXT NOT NULL,
    rows_seen INTEGER NOT NULL DEFAULT 0,
    rows_imported INTEGER NOT NULL DEFAULT 0,
    warnings INTEGER NOT NULL DEFAULT 0,
    errors INTEGER NOT NULL DEFAULT 0,
    started_at TEXT NOT NULL,
    finished_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_categories_volume ON categories(volume_id);
CREATE INDEX IF NOT EXISTS idx_terms_volume ON terms(volume_id);
CREATE INDEX IF NOT EXISTS idx_terms_category ON terms(category_id);
CREATE INDEX IF NOT EXISTS idx_terms_zh ON terms(zh_term);
CREATE INDEX IF NOT EXISTS idx_terms_en ON terms(en_term);
CREATE INDEX IF NOT EXISTS idx_term_aliases_alias ON term_aliases(alias);
CREATE INDEX IF NOT EXISTS idx_term_relations_source ON term_relations(source_term_id);
CREATE INDEX IF NOT EXISTS idx_term_chunks_term ON term_chunks(term_id);


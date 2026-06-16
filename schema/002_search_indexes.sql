CREATE VIRTUAL TABLE IF NOT EXISTS terms_fts USING fts5(
    term_uid UNINDEXED,
    zh_term,
    en_term,
    aliases,
    body,
    tokenize = 'unicode61'
);


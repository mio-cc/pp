-- 003: 面向十万级数据的性能扩展
-- 1) 补充常用过滤/排序字段的索引
-- 2) 增加 trigram 分词的 FTS 表，让中文子串检索也能走索引（≥3字）

-- 复合索引：前端最常用「按卷 + 按分类」过滤
CREATE INDEX IF NOT EXISTS idx_terms_volume_category ON terms(volume_id, category_id);
-- 状态过滤（draft/review/published/deprecated）
CREATE INDEX IF NOT EXISTS idx_terms_status ON terms(status);
-- 卷内按 term_uid 排序的覆盖场景
CREATE INDEX IF NOT EXISTS idx_terms_volume_uid ON terms(volume_id, term_uid);
-- 标签反查
CREATE INDEX IF NOT EXISTS idx_term_tags_tag ON term_tags(tag_id);

-- trigram FTS：专为中文子串检索。unicode61 对中文几乎不分词，
-- trigram 把文本切成 3 字窗口建索引，MATCH 一个 ≥3 字的子串即可命中，
-- 十万级也能走索引，避免 LIKE '%词%' 的全表扫描。
CREATE VIRTUAL TABLE IF NOT EXISTS terms_fts_tri USING fts5(
    term_uid UNINDEXED,
    zh_term,
    en_term,
    aliases,
    body,
    tokenize = 'trigram'
);

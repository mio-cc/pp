-- 004: 提示词中英双语
-- positive_prompt / negative_prompt 保持英文(给 AI 绘图工具直接用)
-- 新增 *_cn 中文对应版本,中英并存且语义对应
ALTER TABLE terms ADD COLUMN positive_prompt_cn TEXT;
ALTER TABLE terms ADD COLUMN negative_prompt_cn TEXT;

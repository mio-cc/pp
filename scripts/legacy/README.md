# legacy 脚本（已归档，勿再使用）

这些是 v1（21 列、含 positive_prompt/definition_short）时期的一次性卷生成器与数据修复脚本，
**已被统一的注入接口取代**。它们仍按旧 16→21 列结构产出，与当前 16 列契约不符，仅作历史留存。

新增/补全术语请改用：
- `python scripts/ingest.py check|add-terms <terms.json>`（见 docs/ai-contributor-guide.md、docs/templates/）
- 新增卷：`python scripts/ingest.py add-volume <volume.json>`
- 重建主库：`python scripts/rebuild.py`（或 ./manage.sh build）

不要再运行本目录脚本写 CSV，否则会引入已废弃的列。

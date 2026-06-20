# 代码审计报告（2026-06-18）

范围：api/app.py、scripts/{build_kb,rebuild,ingest,validate_kb,search_terms,run_api}.py、frontend/src、schema、manage.sh。
方法：语法检查 + 风险 grep + 端到端测试（validate/13接口/ingest三场景/边界探测）+ 人工审 + 独立子代理复审。

## 结论：无高危漏洞或致命 bug

**安全面（API 只读知识库）**
- ✅ 无 SQL 注入：所有用户输入(volume/category/category_prefix/status/tag/tags/q/sort)均走 `?` 参数绑定；`ORDER BY` 取自白名单 `VALID_SORTS`；DB 以 `mode=ro` 只读打开（纵深防御）。
- ✅ 无 FTS 注入：`fts_match_uids` 把查询转义(`"`→`""`)并作引号短语经 `?` 传入。
- ✅ 无 XSS：前端无 `v-html`/`innerHTML`，数据经 Vue `{{ }}` 自动转义。
- ✅ 参数边界齐全：page≥1、page_size≤200、limit≤100、count≤20，越界返回 422。
- ✅ 路由顺序正确：/api/terms/{batch,random,compare} 均注册在 `/{term_uid}` 之前，无通配遮蔽。
- 注：CORS `allow_origins=["*"]`——只读无鉴权 API 可接受；若将来加鉴权/写操作需收紧（低）。

**数据管线**
- ✅ ingest 校验有效：拒绝 重复 term_uid/同卷 zh_term、顶层分类越界、占位/复读定义、更新不存在的 uid。
- ✅ CSV 由 csv.DictWriter 写出，自动转义。
- ✅ 分类树为纯树（0 个"既挂术语又有子类"的混层节点），故前端"分支只显子类"修复不会隐藏任何术语。

## 已修复的问题
| 文件 | 问题 | severity | 修复 |
|---|---|---|---|
| api/app.py | 版本号不一致(app/health=2.0, root=2.1) | 低 | 统一为 2.1 |
| scripts/ingest.py | `update-terms` 改 category 不校验顶层∈config（校验绕过） | 中 | 改 category/zh_term 时补 顶层∈config + 同卷唯一 校验 |
| scripts/ingest.py | 写 CSV 后 rebuild 失败会留中间态（无回滚） | 中 | 新增 `write_and_build`：备份→写→重建+校验，失败回滚 CSV 与主库 |
| scripts/ingest.py | term_uid 自增无 9999 上限保护 | 低 | 超 9999 报错而非产出 5 位非法 uid |
| scripts/ingest.py | category 含空段后未 `continue` | 低 | 加 continue |

## 复核为误报（子代理报高危但实际无误）
- related 子查询"参数数量不匹配"：实为 4 `?` 对 4 参数，实测 200，正常。
- root 端点清单"缺 categories/tree"：实际已包含。
- category_prefix"与 category 不一致"：两者 AND 叠加，工作正常，仅设计风格差异。

## 残留（低优先，未改）
- combine 端点只收对象、batch 兼收裸数组——API 入参宽容度不一致（低）。
- `q` 的 LIKE 兜底中 `%`/`_` 按通配符解释（搜索语义，非安全问题）。
- legacy 脚本仍按 21 列写法——已归档 scripts/legacy/ 并标注勿运行。

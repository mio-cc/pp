# 填充模版与接口使用说明（给 AI 模型）

本目录的模版配合 `scripts/ingest.py` 接口使用。**不要手改 `data/raw/terms_seed.csv`**，
按下面流程产出 JSON 提交即可，工具会逐条校验、自动转义、入库、重建、再校验。

## 文件
- `term.template.json`：术语填充模版（空白骨架 + 一条填好的范例）。机器规范见 `../../schema/term.schema.json`。
- `volume.template.json`：新增卷的填充模版。机器规范见 `../../schema/volume.schema.json`。
- 完整逐字段说明、正反例、分类规则、三种场景：见 `../ai-contributor-guide.md`（**先读它**）。

## 三步流程（务必先 check 再 add）
```bash
python scripts/ingest.py check      你的术语.json    # ① 只校验，不写库；看到「✓ 校验通过」再下一步
python scripts/ingest.py add-terms  你的术语.json    # ② 写入 CSV → 重建主库 → 再校验
python scripts/ingest.py add-volume 新卷.json        # 新增整卷时先做这步，再 add-terms
```

## 写 JSON 时最容易错、务必注意
1. **顶层是数组**：`[ {第一条}, {第二条} ]`，即使只有一条也要放进数组。
2. **多值用数组、不要用分号**：`"tags": ["焦距","定焦"]`（对）；`"tags": "焦距;定焦"`（错）。
   涉及字段：aliases、use_cases、related_terms、confused_with、tags。
3. **term_uid 留空**：写 `"term_uid": ""` 或不写该键，工具自动按卷分配，别自己编号导致冲突。
4. **名字即提示词**：没有 positive_prompt 字段。`zh_term`=中文提示词、`en_term`=英文提示词，要写得原子、具体、可直接出图。
5. **category 是 ` / ` 路径**：首段必须是该卷在 `config/volumes.json` 的顶层分类；末段所在层下面挂的就是本术语。
6. **definition_long 要真**：写清含义/原理/视觉/用法（建议 100–200 字），不能复读名字，不能写「待补充」。
7. **必填不能空**：zh_term、en_term、volume_code、category、definition_long、visual_effect、prompt_usage、use_cases、tags、status、version。

## 一条最小可用范例
```json
[
  {
    "term_uid": "",
    "zh_term": "暖色温3200K", "en_term": "Warm 3200K",
    "volume_code": "V06", "category": "色彩科学 / 色温",
    "definition_long": "3200K 属低色温暖光，画面偏橙黄，常见于钨丝灯、烛光、黄昏，营造温暖怀旧或亲密氛围。",
    "visual_effect": "整体偏暖橙、温馨柔和。",
    "prompt_usage": "营造暖调室内或黄昏氛围时加入。",
    "use_cases": ["室内人像", "氛围照明"],
    "related_terms": ["中性色温5000K"], "confused_with": ["冷蓝色调6500K"],
    "tags": ["色彩", "色温", "暖"], "status": "published", "version": "V1.0"
  }
]
```
提交：`python scripts/ingest.py check 上面这个文件.json`，看到「✓ 校验通过」后改用 `add-terms`。

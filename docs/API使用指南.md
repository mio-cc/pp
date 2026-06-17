# API 使用指南

## 基础信息

- **基础URL**：`http://localhost:8000`
- **协议**：只读 GET 请求（CORS 已开启）
- **文档**：`http://localhost:8000/docs`（Swagger UI）
- **数据格式**：JSON

## 启动服务

```bash
# 安装依赖
pip install -r api/requirements.txt

# 启动服务（开发模式）
python -m uvicorn api.app:app --reload --port 8000

# 或使用项目脚本
./manage.sh start
```

## API 端点

### 1. 健康检查

```http
GET /api/health
```

**返回示例**：
```json
{
  "status": "ok",
  "terms": 1611,
  "version": "2.0"
}
```

---

### 2. 元数据总览（初始化必调）

```http
GET /api/meta
```

**说明**：获取所有卷册、分类、标签、统计信息，用于前端初始化下拉框。

**返回示例**：
```json
{
  "project": "AI视觉设计与提示词工程百科",
  "version": "V1.0",
  "total_terms": 1611,
  "target_total": 10000,
  "completion_percent": 16.11,
  "status_counts": {
    "published": 1611
  },
  "volumes": [
    {
      "code": "V01",
      "title": "摄影体系",
      "sequence": 1,
      "target_terms": 500,
      "current_terms": 191,
      "completion_percent": 38.2,
      "purpose": "建立摄影语言、器材、曝光、镜头和拍摄类型的基础词汇。",
      "categories": [
        {"name": "摄影基础", "term_count": 15},
        {"name": "曝光控制", "term_count": 42}
      ]
    }
  ],
  "tags": [
    {"name": "摄影", "term_count": 188},
    {"name": "色彩", "term_count": 210}
  ]
}
```

---

### 3. 术语列表（筛选 + 分页）

```http
GET /api/terms?volume=V06&category=色彩体系&tag=中国色&status=published&sort=volume&page=1&page_size=20
```

**查询参数**：
| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `q` | string | 关键词（中英文名/别名/定义，≥3字走 trigram FTS） | `暖色温` |
| `volume` | string | 卷册代码 | `V06` |
| `category` | string | 分类名（精确匹配） | `色彩体系` |
| `tag` | string | 标签名 | `中国色` |
| `status` | string | 状态：draft/review/published/deprecated | `published` |
| `sort` | string | 排序：uid/zh/volume/status | `volume` |
| `page` | int | 页码（从1开始） | `1` |
| `page_size` | int | 每页条数（1-200） | `20` |

**返回示例**：
```json
{
  "page": 1,
  "page_size": 20,
  "total": 30,
  "total_pages": 2,
  "items": [
    {
      "term_uid": "V06_T0211",
      "zh_term": "朱殷",
      "en_term": "Zhuyin",
      "volume_code": "V06",
      "volume_title": "灯光与色彩科学",
      "category": "色彩体系 / 中国传统色",
      "definition_short": "如胭脂般浓艳的朱红色，古代贵族用色。",
      "positive_prompt": "zhuyin, rouge red, vivid red",
      "negative_prompt": "",
      "positive_prompt_cn": "朱殷, 鲜艳红",
      "negative_prompt_cn": "",
      "tags": ["色彩", "中国色", "红"],
      "status": "published"
    }
  ]
}
```

---

### 4. 术语详情

```http
GET /api/terms/V06_T0211
```

**返回示例**：
```json
{
  "term_uid": "V06_T0211",
  "zh_term": "朱殷",
  "en_term": "Zhuyin",
  "volume_code": "V06",
  "volume_title": "灯光与色彩科学",
  "category": "色彩体系 / 中国传统色",
  "definition_short": "如胭脂般浓艳的朱红色，古代贵族用色。",
  "definition_long": "朱殷，如胭脂般浓艳的朱红色，古代贵族用色。源自中国或日本传统色彩文化，具有独特的文化内涵与审美意境。",
  "visual_effect": "鲜艳娇媚、明亮红。",
  "prompt_usage": "用于传统美人、古装场景。",
  "positive_prompt": "zhuyin, rouge red, vivid red",
  "negative_prompt": "",
  "positive_prompt_cn": "朱殷, 鲜艳红",
  "negative_prompt_cn": "",
  "use_cases": ["古装", "人像"],
  "aliases": ["胭脂朱"],
  "related_terms": [],
  "confused_with": [],
  "tags": ["色彩", "中国色", "红"],
  "source_refs": "zhongguose.com;nipponcolors.com",
  "status": "published",
  "version": "V1.0"
}
```

---

### 5. 全文搜索

```http
GET /api/search?q=电影感&limit=20
```

**查询参数**：
| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `q` | string | 搜索关键词（必填） | - |
| `limit` | int | 返回条数（1-100） | 20 |

**搜索逻辑**：
- **≥3字**：trigram FTS 子串检索（已索引，快速）
- **<3字**：LIKE 全表扫描（兜底）

**返回示例**：
```json
{
  "query": "电影感",
  "count": 2,
  "engine": "trigram",
  "items": [
    {
      "term_uid": "V02_T0120",
      "zh_term": "电影感",
      "en_term": "Cinematic",
      "volume_code": "V02",
      "volume_title": "电影摄影体系",
      "category": "电影风格",
      "definition_short": "具有电影质感的画面氛围与叙事性。",
      "positive_prompt": "cinematic, movie quality",
      "positive_prompt_cn": "电影感, 电影质感",
      "tags": ["电影", "质感"],
      "status": "published"
    }
  ]
}
```

---

### 6. 卷册列表

```http
GET /api/volumes
```

**返回**：所有卷册的详细信息（同 `/api/meta` 中的 volumes 字段）。

---

### 7. 卷册分类

```http
GET /api/volumes/V06/categories
```

**返回示例**：
```json
{
  "volume_code": "V06",
  "items": [
    {"name": "光度与照度", "term_count": 5},
    {"name": "色彩科学", "term_count": 80},
    {"name": "色彩体系", "term_count": 155}
  ]
}
```

---

### 8. 标签列表

```http
GET /api/tags
```

**返回示例**：
```json
{
  "items": [
    {"name": "色彩", "term_count": 240},
    {"name": "摄影", "term_count": 191}
  ]
}
```

---

### 9. 统计信息

```http
GET /api/stats
```

**返回**：项目完成度统计（同 `/api/meta` 的统计部分）。

---

### 10. 提示词导出

```http
GET /api/export/prompts?volume=V08&tag=质量&format=json
```

**查询参数**：
| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `volume` | string | 卷册过滤 | - |
| `tag` | string | 标签过滤 | - |
| `format` | string | json/text | `json` |

**JSON 格式返回**：
```json
{
  "count": 5,
  "items": [
    {
      "term_uid": "V08_T0127",
      "zh_term": "杰作",
      "en_term": "Masterpiece",
      "volume_code": "V08",
      "positive_prompt": "masterpiece, best quality",
      "negative_prompt": ""
    }
  ]
}
```

**TEXT 格式返回**：
```text
# 杰作 / Masterpiece [V08_T0127]
+ masterpiece, best quality

# 8K分辨率 / 8K Resolution [V08_T0128]
+ 8K resolution, ultra detailed
```

---

## 常见用例

### 1. 初始化前端（获取所有元数据）
```javascript
fetch('http://localhost:8000/api/meta')
  .then(res => res.json())
  .then(data => {
    console.log('卷册：', data.volumes);
    console.log('标签：', data.tags);
  });
```

### 2. 按卷筛选术语
```javascript
fetch('http://localhost:8000/api/terms?volume=V06&page_size=50')
  .then(res => res.json())
  .then(data => {
    console.log('V06术语：', data.items);
  });
```

### 3. 搜索关键词
```javascript
fetch('http://localhost:8000/api/search?q=赛博朋克')
  .then(res => res.json())
  .then(data => {
    console.log('搜索结果：', data.items);
  });
```

### 4. 获取术语详情
```javascript
fetch('http://localhost:8000/api/terms/V15_T0001')
  .then(res => res.json())
  .then(data => {
    console.log('术语详情：', data);
  });
```

### 5. 导出提示词（纯文本）
```javascript
fetch('http://localhost:8000/api/export/prompts?volume=V08&format=text')
  .then(res => res.text())
  .then(text => {
    console.log('提示词清单：\n', text);
  });
```

---

## 技术细节

### 中文搜索优化
- **trigram FTS5**：对中文进行3字符trigram索引（如"赛博朋克" → "赛博博" + "博朋朋" + "朋克克"）
- **≥3字查询**：走索引，速度快
- **<3字查询**：LIKE 全表扫描（兜底，适用于短词）

### 分页限制
- 最大 `page_size`：200
- 推荐默认：20

### 只读模式
- 数据库以 `mode=ro` 打开，物理上无法写入
- 所有写操作走 `CSV → build_kb.py → SQLite` 流程

### CORS
- 允许所有来源（`allow_origins=["*"]`）
- 仅允许 GET 方法

---

## 前端集成示例（Vue 3）

```vue
<script setup>
import { ref, onMounted } from 'vue'

const volumes = ref([])
const terms = ref([])
const selectedVolume = ref('')

onMounted(async () => {
  // 初始化：获取元数据
  const meta = await fetch('http://localhost:8000/api/meta').then(r => r.json())
  volumes.value = meta.volumes
})

const loadTerms = async () => {
  const url = `http://localhost:8000/api/terms?volume=${selectedVolume.value}&page_size=100`
  const data = await fetch(url).then(r => r.json())
  terms.value = data.items
}
</script>

<template>
  <div>
    <select v-model="selectedVolume" @change="loadTerms">
      <option value="">选择卷册</option>
      <option v-for="vol in volumes" :key="vol.code" :value="vol.code">
        {{ vol.title }} ({{ vol.current_terms }}/{{ vol.target_terms }})
      </option>
    </select>

    <ul>
      <li v-for="term in terms" :key="term.term_uid">
        {{ term.zh_term }} - {{ term.definition_short }}
      </li>
    </ul>
  </div>
</template>
```

---

## 错误响应

### 404 Not Found
```json
{
  "detail": "未找到术语 V99_T9999"
}
```

### 503 Service Unavailable
```json
{
  "detail": "数据库不存在，请先运行 python scripts/build_kb.py"
}
```

---

---

## 新增功能（v2.1）

### 11. 分类路径层级筛选
```http
GET /api/terms?category_prefix=代表性风格/
```

**说明**：筛选分类路径以指定前缀开头的所有术语，用于树形菜单筛选。

**参数**：
- `category_prefix`: 分类路径前缀，如「代表性风格/」或「色彩体系/中国传统色」

---

### 12. 批量获取术语详情
```http
POST /api/terms/batch
Content-Type: application/json

["V06_T0211", "V02_T0120", "V08_T0127"]
```

**说明**：一次性获取多个术语的完整详情，用于篮子功能等场景。

**限制**：最多50条。

---

### 13. 随机术语探索
```http
GET /api/terms/random?count=5&volume=V06
```

**参数**：
- `count`: 返回数量（1-20）
- `volume`: 限定卷册（可选）
- `category`: 限定分类（可选）
- `tag`: 限定标签（可选）

---

### 14. 提示词合并组合
```http
POST /api/prompts/combine
Content-Type: application/json

{
  "term_uids": ["V06_T0211", "V02_T0120", "V08_T0127"],
  "language": "both",
  "format": "comma"
}
```

**参数**：
- `term_uids`: 术语UID列表（最多30条）
- `language`: 语言选项：`en` / `cn` / `both`
- `format`: 格式选项：`comma`（逗号分隔）/ `newline`（换行）/ `weighted`（带权重）

**返回示例**：
```json
{
  "combined": "zhuyin, cinematic, masterpiece, best quality",
  "combined_en": "zhuyin, cinematic, masterpiece, best quality",
  "combined_cn": "朱殷, 电影感, 杰作",
  "language": "both",
  "format": "comma",
  "count": 3,
  "terms": [...]
}
```

---

### 15. 相关术语推荐
```http
GET /api/terms/{term_uid}/related?limit=5
```

**说明**：基于同分类、同标签智能推荐相关术语。

---

### 16. 术语对比
```http
GET /api/terms/compare?a=V06_T0211&b=V06_T0145
```

**说明**：对比两个术语的异同。

---

### 17. 分类树状结构
```http
GET /api/volumes/{code}/categories/tree
```

**说明**：获取分类的树状结构，用于前端树形菜单渲染。

**返回示例**：
```json
{
  "volume_code": "V03",
  "tree": {
    "代表性风格": {
      "_count": 20,
      "_children": {
        "动画导演": {
          "_count": 2,
          "_children": {}
        }
      }
    }
  }
}
```

---

### 18. 多标签筛选（AND/OR逻辑）
```http
GET /api/terms?tags=色彩,中国色&tag_logic=AND
```

**说明**：
- 单标签筛选：`tag=色彩`
- 多标签筛选：`tags=色彩,中国色,传统`
- 逻辑控制：`tag_logic=AND`（默认）或 `tag_logic=OR`

---

### 19. 高级搜索（指定字段）
```http
GET /api/search/advanced?zh_term=朱殷&positive_prompt=neon
```

**参数**：
- `zh_term`: 中文名模糊匹配
- `en_term`: 英文名模糊匹配
- `definition_short`: 简短定义模糊匹配
- `positive_prompt`: 英文提示词模糊匹配
- `category`: 分类模糊匹配
- `volume`: 卷册精确匹配
- `limit`: 返回数量限制

---

### 20. 版本说明

v2.1 新增功能：
- ✅ 分类路径层级筛选
- ✅ 批量获取术语详情
- ✅ 随机术语探索
- ✅ 提示词合并组合
- ✅ 相关术语推荐
- ✅ 术语对比
- ✅ 分类树状结构
- ✅ 多标签筛选（AND/OR逻辑）
- ✅ 高级搜索（指定字段）

---

## 性能建议

1. **首次加载**：调用 `/api/meta` 获取全量元数据缓存在前端
2. **分页加载**：按需加载术语，`page_size=20`
3. **搜索防抖**：用户输入搜索关键词时加300ms防抖
4. **术语详情**：点击时才调用 `/api/terms/{uid}`，不预加载
5. **提示词导出**：大批量导出用 `format=text`，减少JSON解析开销
6. **批量获取**：多术语详情时用 `/api/terms/batch`，减少请求次数
7. **树状菜单**：用 `/api/volumes/{code}/categories/tree` 获取分类树，客户端递归渲染
8. **标签筛选**：AND逻辑适合精确筛选，OR逻辑适合宽泛搜索

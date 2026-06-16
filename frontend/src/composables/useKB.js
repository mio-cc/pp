import { reactive } from 'vue'

/**
 * 懒加载数据层 —— 面向十万级数据设计。
 * api 模式连 FastAPI 按需分页/搜索；offline 模式读静态 JSON（index 秒开 + 分卷懒加载）。
 * page_size 一律 ≤200（与 API 上限一致，既符合校验也防超大响应）。
 */
const state = reactive({
  mode: '',
  ready: false,
  error: null,
  index: null,
  _base: ''
})

const volumeCache = new Map()
const catCache = new Map()
let allTerms = null

async function fetchJSON(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

async function tryStatic(paths) {
  for (const p of paths) {
    try {
      return await fetchJSON(p)
    } catch (e) {
      /* next */
    }
  }
  return null
}

const STATIC_BASES = ['./data/exports/web', '../data/exports/web', '/data/exports/web', 'data/exports/web']

async function init() {
  try {
    const meta = await fetchJSON(location.origin + '/api/meta')
    state.index = meta
    state.mode = 'api'
    state.ready = true
    return state
  } catch (e) {
    /* 转离线 */
  }
  for (const base of STATIC_BASES) {
    const idx = await tryStatic([`${base}/index.json`, `${base}/meta.json`])
    if (idx) {
      state.index = idx
      state.mode = 'offline'
      state._base = base
      state.ready = true
      return state
    }
  }
  state.error =
    '无法加载数据。请先构建知识库并启动服务：\n' +
    '1. ./manage.sh build  构建知识库\n' +
    '2. ./manage.sh start  启动 API 服务\n' +
    '3. 访问 http://服务器IP:8000/app/'
  return state
}

// 按分页循环取完某个筛选条件下的全部术语；page_size 固定 200
async function fetchAllPages(baseUrl) {
  const sep = baseUrl.includes('?') ? '&' : '?'
  let page = 1
  let out = []
  for (;;) {
    const data = await fetchJSON(`${baseUrl}${sep}page=${page}&page_size=200`)
    out = out.concat(data.items)
    if (page >= (data.total_pages || 1)) break
    page += 1
  }
  return out
}

async function loadVolumeTerms(volumeCode) {
  if (volumeCache.has(volumeCode)) return volumeCache.get(volumeCode)
  let terms = []
  if (state.mode === 'api') {
    terms = await fetchAllPages(`${location.origin}/api/terms?volume=${encodeURIComponent(volumeCode)}`)
  } else {
    const data = await tryStatic([`${state._base}/volumes/${volumeCode}.json`])
    terms = data ? data.items : []
  }
  volumeCache.set(volumeCode, terms)
  return terms
}

async function loadCategoryTerms(volumeCode, categoryName) {
  const key = `${volumeCode}::${categoryName}`
  if (catCache.has(key)) return catCache.get(key)
  let filtered
  if (state.mode === 'api') {
    // API 模式：直接按卷+分类查，只拉该分类术语（十万级也不会拖全卷）
    filtered = await fetchAllPages(
      `${location.origin}/api/terms?volume=${encodeURIComponent(volumeCode)}&category=${encodeURIComponent(categoryName)}`
    )
  } else {
    const volTerms = await loadVolumeTerms(volumeCode)
    filtered = volTerms.filter((t) => (t.category || '未分类') === categoryName)
  }
  catCache.set(key, filtered)
  return filtered
}

async function ensureAllTerms() {
  if (allTerms) return allTerms
  if (state.mode === 'api') {
    allTerms = await fetchAllPages(location.origin + '/api/terms')
  } else {
    const all = []
    for (const v of state.index.volumes) {
      all.push(...(await loadVolumeTerms(v.code)))
    }
    allTerms = all
  }
  return allTerms
}

async function search(q, limit = 50) {
  q = (q || '').trim()
  if (!q) return []
  if (state.mode === 'api') {
    const data = await fetchJSON(`${location.origin}/api/search?q=${encodeURIComponent(q)}&limit=${limit}`)
    return data.items
  }
  const all = await ensureAllTerms()
  const ql = q.toLowerCase()
  const hits = []
  for (const t of all) {
    if (
      t.zh_term.toLowerCase().includes(ql) ||
      (t.en_term || '').toLowerCase().includes(ql) ||
      (t.definition_short || '').toLowerCase().includes(ql) ||
      (t.positive_prompt || '').toLowerCase().includes(ql)
    ) {
      hits.push(t)
      if (hits.length >= limit) break
    }
  }
  return hits
}

export function useKB() {
  return { state, init, loadVolumeTerms, loadCategoryTerms, search }
}

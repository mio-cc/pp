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

async function fetchJSONWithInit(url, init) {
  const res = await fetch(url, init)
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

async function loadCategoryBranchTerms(volumeCode, categoryPath) {
  const key = `${volumeCode}::branch::${categoryPath}`
  if (catCache.has(key)) return catCache.get(key)
  let filtered
  if (state.mode === 'api') {
    filtered = await fetchAllPages(
      `${location.origin}/api/terms?volume=${encodeURIComponent(volumeCode)}&category_prefix=${encodeURIComponent(categoryPath)}`
    )
  } else {
    const volTerms = await loadVolumeTerms(volumeCode)
    filtered = volTerms.filter((t) => {
      const cat = t.category || '未分类'
      return cat === categoryPath || cat.startsWith(`${categoryPath} / `)
    })
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

async function termDetail(termUid) {
  if (state.mode === 'api') {
    return fetchJSON(`${location.origin}/api/terms/${encodeURIComponent(termUid)}`)
  }
  const all = await ensureAllTerms()
  return all.find((t) => t.term_uid === termUid) || null
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
      (t.definition_long || '').toLowerCase().includes(ql)
    ) {
      hits.push(t)
      if (hits.length >= limit) break
    }
  }
  return hits
}

async function batchTerms(termUids) {
  const cleaned = (termUids || []).map((uid) => uid && uid.trim()).filter(Boolean)
  if (!cleaned.length) return { count: 0, requested_count: 0, missing_term_uids: [], items: [] }

  if (state.mode === 'api') {
    return fetchJSONWithInit(`${location.origin}/api/terms/batch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ term_uids: cleaned })
    })
  }

  const all = await ensureAllTerms()
  const byUid = new Map(all.map((t) => [t.term_uid, t]))
  const items = cleaned.map((uid) => byUid.get(uid)).filter(Boolean)
  const missing = cleaned.filter((uid) => !byUid.has(uid))
  return { count: items.length, requested_count: cleaned.length, missing_term_uids: missing, items }
}

async function combinePrompts(termUids, options = {}) {
  const cleaned = (termUids || []).map((uid) => uid && uid.trim()).filter(Boolean)
  const language = options.language || 'en'
  const format = options.format || 'comma'

  if (!cleaned.length) {
    return {
      combined: '',
      combined_en: '',
      combined_cn: '',
      language,
      format,
      count: 0,
      requested_count: 0,
      missing_term_uids: [],
      terms: []
    }
  }

  if (state.mode === 'api') {
    return fetchJSONWithInit(`${location.origin}/api/prompts/combine`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ term_uids: cleaned, language, format })
    })
  }

  const detail = await batchTerms(cleaned)
  let promptsEn = detail.items.map((t) => t.en_term || t.zh_term || '').filter(Boolean)
  let promptsCn = detail.items.map((t) => t.zh_term || '').filter(Boolean)

  let sep = ', '
  if (format === 'newline') sep = '\n'
  if (format === 'weighted') {
    promptsEn = promptsEn.map((p) => `(${p}:1.1)`)
    promptsCn = promptsCn.map((p) => `(${p}:1.1)`)
  }

  const combinedEn = promptsEn.join(sep)
  const combinedCn = promptsCn.join(sep)
  const combined =
    language === 'en'
      ? combinedEn
      : language === 'cn'
        ? combinedCn
        : (combinedEn && combinedCn ? `${combinedEn}\n${combinedCn}` : combinedEn || combinedCn)

  return {
    combined,
    combined_en: combinedEn,
    combined_cn: combinedCn,
    language,
    format,
    count: detail.items.length,
    requested_count: cleaned.length,
    missing_term_uids: detail.missing_term_uids || [],
    terms: detail.items.map((t) => ({
      term_uid: t.term_uid,
      zh_term: t.zh_term,
      prompt_en: t.en_term || t.zh_term || '',
      prompt_cn: t.zh_term || ''
    }))
  }
}

async function randomTerms(options = {}) {
  const qs = new URLSearchParams()
  if (options.count) qs.set('count', String(options.count))
  if (options.volume) qs.set('volume', options.volume)
  if (options.category) qs.set('category', options.category)
  if (options.category_prefix) qs.set('category_prefix', options.category_prefix)
  if (options.tag) qs.set('tag', options.tag)

  if (state.mode === 'api') {
    return fetchJSON(`${location.origin}/api/terms/random?${qs.toString()}`)
  }

  let source = await ensureAllTerms()
  if (options.volume) source = source.filter((t) => t.volume_code === options.volume)
  if (options.category) source = source.filter((t) => (t.category || '') === options.category)
  if (options.category_prefix) {
    source = source.filter((t) => {
      const cat = t.category || ''
      return cat === options.category_prefix || cat.startsWith(`${options.category_prefix} / `)
    })
  }
  if (options.tag) {
    source = source.filter((t) => (t.tags || []).includes(options.tag))
  }

  const shuffled = [...source]
  for (let i = shuffled.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  const count = Number(options.count || 5)
  return {
    count: Math.min(count, shuffled.length),
    available: shuffled.length,
    items: shuffled.slice(0, count)
  }
}

export function useKB() {
  return {
    state,
    init,
    loadVolumeTerms,
    loadCategoryTerms,
    loadCategoryBranchTerms,
    search,
    batchTerms,
    combinePrompts,
    randomTerms,
    termDetail
  }
}

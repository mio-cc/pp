<template>
  <div class="app" :class="{ 'side-hidden': sideCollapsed }">
    <header class="topbar">
      <button class="toggle" title="折叠/展开侧栏 (Ctrl+\)" @click="sideCollapsed = !sideCollapsed">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="9" y1="4" x2="9" y2="20"/></svg>
      </button>
      <span class="brand"><span class="mk"><i></i></span><span>视觉术语<span class="dot">·</span><span class="sub">提示词构建器</span></span></span>
      <span v-if="kb.state.mode" class="modetag">{{ kb.state.mode === 'api' ? 'API 模式' : '离线模式' }}</span>
        <div class="search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
          <input ref="searchInput" v-model="q" placeholder="搜索术语…（Ctrl+K）" @input="onSearch" />
        </div>
        <button class="tool" title="随机术语" @click="loadRandom"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h4l3 10h4l3-10h2"/><path d="M16 7h4l-3 10"/></svg></button>
      </header>

    <div class="body">
      <aside class="side">
        <div class="side-hd"><span>体系 / 分类</span><span class="cnt">{{ totalTerms }} 词</span></div>
        <div class="tree">
          <div v-for="r in flatRows" :key="r.key" class="trow" :class="[r.depth === 0 ? 'lv1' : 'sub', { on: r.key === activeKey, open: r.open }]" @click="onRowClick(r)">
            <span v-for="i in r.depth" :key="i" class="guide-cell"></span>
            <span class="tw" :style="{ visibility: r.hasKids ? 'visible' : 'hidden' }" @click.stop="onCaret(r)">▶</span>
            <span v-if="r.depth === 0" class="ico">◆</span>
            <span class="tn">{{ r.title }}</span>
            <span v-if="loadingVol.has(r.code) && r.type==='vol'" class="tc">…</span>
            <span v-else class="tc">{{ r.count }}</span>
          </div>
        </div>
      </aside>

      <main class="main">
        <div v-if="!kb.state.ready && !kb.state.error" class="center-state"><div class="spinner"></div><div>加载知识库…</div></div>
        <div v-else-if="kb.state.error" class="center-state err"><div class="big">!</div><pre>{{ kb.state.error }}</pre></div>

        <template v-else>
          <div class="crumb">
            <template v-for="(s, i) in view.crumb" :key="i">
              <span class="seg" :class="{ cur: !s.fn }" @click="s.fn && s.fn()">{{ s.label }}</span>
              <span v-if="i < view.crumb.length - 1" class="arr">›</span>
            </template>
            <span class="hint">{{ view.hint }}</span>
          </div>

          <div v-if="view.type === 'welcome'" class="welcome">
            <div class="welcome-card">
              <div class="big">⌘</div><h3>选择一个体系开始构建提示词</h3>
              <p>共 {{ vols.length }} 卷 · {{ totalTerms }} 个术语 · 分类任意深度</p>
              <div class="vq-grid">
                <button v-for="v in vols" :key="v.code" class="vq" @click="navigate(v.code, null)">{{ v.title }}<span>{{ v.current_terms }}</span></button>
              </div>
            </div>
          </div>

          <template v-else>
            <div v-if="view.cards.length" class="secgrp">
              <div class="gh"><span class="gt">{{ view.title }}</span><span class="gline"></span><span class="gn">{{ view.cards.length }} {{ view.type==='volume' ? '分类' : '子类' }}</span></div>
              <div class="vq-grid">
                <button v-for="c in view.cards" :key="c.path" class="vq" @click="navigate(view.code, c.path)">
                  {{ c.name }}<span v-if="c.childCount" style="color:var(--accent)">›{{ c.childCount }}</span><span>{{ c.count }}</span>
                </button>
              </div>
            </div>
            <div v-if="view.terms.length" class="secgrp">
              <div class="gh"><span class="gt">{{ view.type==='search' ? '命中结果' : view.title + ' · 术语' }}</span><span class="gline"></span><span class="gn">{{ view.terms.length }}</span></div>
              <div class="chips">
                <div v-for="t in view.terms" :key="t.term_uid" class="cchip" :class="{ sel: inCart(t.term_uid) }" @click="openDetail(t)">
                  <div class="cn">{{ t.zh_term }}</div>
                  <div class="ce">{{ t.en_term || t.zh_term || '—' }}</div>
                  <span class="add" @click.stop="toggleCart(t)">{{ inCart(t.term_uid) ? '✓' : '+' }}</span>
                </div>
              </div>
            </div>
            <div v-if="!view.cards.length && !view.terms.length" class="center-state"><div class="big">∅</div><div>该分类暂无术语</div></div>
          </template>
        </template>
      </main>
    </div>

    <!-- 详情 -->
    <div class="detail" :class="{ open: !!detailTerm }">
      <template v-if="detailTerm">
        <button class="x" @click="detailTerm = null">✕</button>
        <div class="lin">
          <div><b>{{ detailTerm.volume_title }}</b><span class="tag">体系 {{ detailTerm.volume_code }}</span></div>
          <div v-for="(seg, i) in (detailTerm.category || '').split(' / ')" :key="i" :style="{ marginLeft: (i*10)+'px' }">└ <b>{{ seg }}</b></div>
          <div :style="{ marginLeft: ((detailTerm.category||'').split(' / ').length*10)+'px' }">└ <b>{{ detailTerm.zh_term }}</b><span class="tag">术语</span></div>
        </div>
        <h2>{{ detailTerm.zh_term }}<button class="cpname" @click="copyText(detailTerm.zh_term, $event)" title="复制中文提示词">复制</button></h2>
        <div class="den">{{ detailTerm.en_term || detailTerm.term_uid }}<button v-if="detailTerm.en_term" class="cpname" @click="copyText(detailTerm.en_term, $event)" title="复制英文提示词">复制</button></div>
        <div class="namehint">中文名即中文提示词 · 英文名即英文提示词</div>
        <div v-if="detailTerm.definition_long" class="sec"><div class="slabel">详细解释</div><div class="stext">{{ detailTerm.definition_long }}</div></div>
        <div v-if="detailTerm.visual_effect" class="sec"><div class="slabel">视觉表现</div><div class="stext">{{ detailTerm.visual_effect }}</div></div>
        <div v-if="detailTerm.prompt_usage" class="sec"><div class="slabel">提示词用法</div><div class="stext">{{ detailTerm.prompt_usage }}</div></div>
        <div v-if="detailTerm.use_cases && detailTerm.use_cases.length" class="sec"><div class="slabel">适用场景</div><div class="chips"><span v-for="u in detailTerm.use_cases" :key="u" class="chip">{{ u }}</span></div></div>
        <div v-if="detailTerm.tags && detailTerm.tags.length" class="sec"><div class="slabel">标签</div><div class="chips"><span v-for="tg in detailTerm.tags" :key="tg" class="chip ctag">{{ tg }}</span></div></div>
        <button class="dbtn" :class="{ added: inCart(detailTerm.term_uid) }" @click="toggleCart(detailTerm)">{{ inCart(detailTerm.term_uid) ? '✓ 已在提示词篮' : '＋ 加入提示词篮' }}</button>
      </template>
    </div>

    <!-- 中英控件：浮于提示词篮外左上角 -->
    <div class="langfloat" :style="{ bottom: langBottom + 'px' }">
      <div class="seg-ctl">
        <button :class="{ on: copyLang==='en' }" @click="setLang('en')">EN</button>
        <button :class="{ on: copyLang==='cn' }" @click="setLang('cn')">中</button>
        <button :class="{ on: copyLang==='both' }" @click="setLang('both')">中英</button>
      </div>
    </div>

    <!-- 提示词篮 -->
      <div class="dock" ref="dockRef">
        <div class="dock-top">
          <span class="dlbl"><span class="icn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/></svg></span>提示词篮<span class="num">{{ cart.length }}</span></span>
        <span class="divd"></span>
        <div class="frags" :class="{ expanded: basketExpanded }">
          <span v-if="!cart.length" class="ph">点术语卡右上角 + 添加</span>
          <span v-for="(c, i) in cart" :key="c.term_uid" class="frag" :class="{ conflict: conflictUids.has(c.term_uid) }" :title="c.category">
            <span v-if="conflictUids.has(c.term_uid)" class="fdot"></span>{{ c.zh_term }}<x @click="cart.splice(i,1)">✕</x>
          </span>
        </div>
        <div class="acts">
          <button class="ic" title="批量获取术语" @click="loadBatch"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h10"/></svg></button>
          <button class="ic" title="提示词合并" @click="mergeBasket"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h10"/></svg></button>
          <button class="ic" :class="{ on: basketExpanded }" title="展开/收起提示词篮" @click="basketExpanded = !basketExpanded"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 14l5-5 5 5"/></svg></button>
          <button class="ic" :class="{ on: showPrev }" title="预览将复制的提示词" @click="showPrev = !showPrev"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg></button>
          <button class="copy" :class="{ done: copied }" @click="copyAll"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>{{ copied ? '✓ 已复制' : '复制' }}</button>
        </div>
      </div>
      <div class="dock-prev" :class="{ show: showPrev }">
        <template v-if="cart.length"><span v-if="conflictUids.size" class="warn">⚠ 同分支冲突 {{ conflictUids.size }} 项(已标红，仍可复制)</span><br v-if="conflictUids.size"><b>将复制：</b>{{ promptText }}</template>
        <span v-else class="pl">空。复制内容随语言开关变化(EN/中/中英)，不影响可复制</span>
      </div>
    </div>

    <div v-if="randomPanel.length" class="random-panel">
      <div class="gh"><span class="gt">随机术语</span><span class="gline"></span><button class="mini" @click="randomPanel = []">关闭</button></div>
      <div class="chips">
        <div v-for="t in randomPanel" :key="t.term_uid" class="cchip" :class="{ sel: inCart(t.term_uid) }" @click="openDetail(t)">
          <div class="cn">{{ t.zh_term }}</div>
          <div class="ce">{{ t.en_term || t.zh_term || '—' }}</div>
          <span class="add" @click.stop="toggleCart(t)">{{ inCart(t.term_uid) ? '✓' : '+' }}</span>
        </div>
      </div>
    </div>

    <div class="toast" :class="{ show: !!toastMsg }">{{ toastMsg }}</div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useKB } from './composables/useKB'

const kb = useKB()
const SEP = ' / '
const sideCollapsed = ref(false)
const q = ref('')
const searchInput = ref(null)
const expanded = reactive(new Set())
const volTrees = reactive({})
const loadingVol = reactive(new Set())
const activeKey = ref('')
const cart = reactive([])
const copyLang = ref('en')
const detailTerm = ref(null)
const showPrev = ref(false)
const basketExpanded = ref(false)
const copied = ref(false)
const toastMsg = ref('')
const dockRef = ref(null)
const langBottom = ref(70)
const randomPanel = ref([])
let toastT = null
let _ro = null
const view = reactive({ type: 'welcome', crumb: [{ label: '全部体系' }], title: '', hint: '', cards: [], terms: [], code: '' })

onMounted(() => {
  kb.init()
  window.addEventListener('keydown', onKey)
  measureDock()
  if (window.ResizeObserver && dockRef.value) { _ro = new ResizeObserver(() => measureDock()); _ro.observe(dockRef.value) }
})
onUnmounted(() => { window.removeEventListener('keydown', onKey); if (_ro) _ro.disconnect() })

const vols = computed(() => (kb.state.index ? kb.state.index.volumes : []))
const totalTerms = computed(() => (kb.state.index ? kb.state.index.total_terms : 0))

function toast(m) { toastMsg.value = m; clearTimeout(toastT); toastT = setTimeout(() => (toastMsg.value = ''), 1600) }
function onKey(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); searchInput.value && searchInput.value.focus() }
  if ((e.metaKey || e.ctrlKey) && e.key === '\\') { e.preventDefault(); sideCollapsed.value = !sideCollapsed.value }
  if (e.key === 'Escape') detailTerm.value = null
}

function buildTree(terms) {
  const root = { name: '', path: '', children: new Map(), terms: [], count: 0 }
  for (const t of terms) {
    const segs = (t.category || '未分类').split(SEP).map((s) => s.trim()).filter(Boolean)
    let node = root, parts = []
    for (const seg of segs) {
      parts.push(seg)
      if (!node.children.has(seg)) node.children.set(seg, { name: seg, path: parts.join(SEP), children: new Map(), terms: [], count: 0 })
      node = node.children.get(seg)
    }
    node.terms.push(t)
  }
  ;(function cnt(n) { let c = n.terms.length; n.children.forEach((ch) => (c += cnt(ch))); n.count = c; return c })(root)
  return root
}
function categoryPathForRow(r) {
  if (r.type === 'vol') return ''
  return r.path || ''
}
function findNode(code, path) { let n = volTrees[code]; if (!n) return null; for (const s of path.split(SEP)) { if (!n.children.has(s)) return null; n = n.children.get(s) } return n }
async function ensureVol(code) {
  if (volTrees[code]) return volTrees[code]
  loadingVol.add(code)
  try { const terms = await kb.loadVolumeTerms(code); volTrees[code] = buildTree(terms) } finally { loadingVol.delete(code) }
  return volTrees[code]
}

const flatRows = computed(() => {
  const rows = []
  for (const v of vols.value) {
    const vkey = 'V|' + v.code
    const open = expanded.has(vkey)
    rows.push({ type: 'vol', key: vkey, code: v.code, title: v.title, count: v.current_terms, depth: 0, hasKids: true, open })
    if (open && volTrees[v.code]) walk(volTrees[v.code].children, 1, v.code, rows)
  }
  return rows
})
function walk(children, depth, code, rows) {
  for (const node of children.values()) {
    const key = 'N|' + code + '|' + node.path
    const hasKids = node.children.size > 0
    const open = expanded.has(key)
    rows.push({ type: 'node', key, code, path: node.path, title: node.name, count: node.count, depth, hasKids, open })
    if (open && hasKids) walk(node.children, depth + 1, code, rows)
  }
}

function setVolExclusive(code) {
  for (const k of [...expanded]) { if (k === 'V|' + code) continue; if (k.startsWith('N|' + code + '|')) continue; expanded.delete(k) }
  expanded.add('V|' + code)
}
function onCaret(r) {
  if (!r.hasKids) return
  if (r.type === 'vol') { onRowClick(r); return }
  if (expanded.has(r.key)) { for (const k of [...expanded]) if (k === r.key || k.startsWith(r.key + SEP)) expanded.delete(k) }
  else expanded.add(r.key)
}
async function onRowClick(r) {
  if (r.type === 'vol') {
    await ensureVol(r.code)
    const was = expanded.has(r.key)
    setVolExclusive(r.code)
    if (was) { for (const k of [...expanded]) if (k === r.key || k.startsWith('N|' + r.code + '|')) expanded.delete(k) }
    activeKey.value = r.key
    await showVolume(r.code)
  } else {
    if (r.hasKids && !expanded.has(r.key)) expanded.add(r.key)
    activeKey.value = r.key
    await showNode(r.code, r.path)
  }
}

function goWelcome() { activeKey.value = ''; Object.assign(view, { type: 'welcome', crumb: [{ label: '全部体系' }], title: '', hint: '', cards: [], terms: [], code: '' }) }
async function showVolume(code) {
  const v = vols.value.find((x) => x.code === code); const root = volTrees[code]
  const cards = root ? [...root.children.values()].map((n) => ({ name: n.name, path: n.path, childCount: n.children.size, count: n.count })) : []
  Object.assign(view, { type: 'volume', title: v.title, code, crumb: [{ label: '全部体系', fn: goWelcome }, { label: v.title }], cards, terms: [], hint: cards.length + ' 个分类' })
}
async function showNode(code, path) {
  const v = vols.value.find((x) => x.code === code); const node = findNode(code, path); if (!node) return
  const segs = path.split(SEP)
  const crumb = [{ label: '全部体系', fn: goWelcome }, { label: v.title, fn: () => navigate(code, null) }]
  let acc = []
  segs.forEach((s, i) => { acc.push(s); const p = acc.join(SEP); crumb.push(i === segs.length - 1 ? { label: s } : { label: s, fn: () => navigate(code, p) }) })
  const kids = [...node.children.values()].map((n) => ({ name: n.name, path: n.path, childCount: n.children.size, count: n.count }))
  const terms = await kb.loadCategoryBranchTerms(code, path)
  Object.assign(view, { type: 'node', title: node.name, code, crumb, cards: kids, terms, hint: node.count + ' 个术语' })
}
async function navigate(code, path) {
  await ensureVol(code)
  setVolExclusive(code)
  if (path) { const segs = path.split(SEP); let acc = []; for (const s of segs) { acc.push(s); expanded.add('N|' + code + '|' + acc.join(SEP)) } activeKey.value = 'N|' + code + '|' + path; await showNode(code, path) }
  else { activeKey.value = 'V|' + code; await showVolume(code) }
}

function currentCategoryPath() {
  if (!activeKey.value.startsWith('N|')) return ''
  return activeKey.value.split('|').slice(2).join('|').replace(/\|/g, SEP)
}

let st = null
function onSearch() {
  clearTimeout(st); const s = q.value.trim()
  if (!s) { goWelcome(); return }
  st = setTimeout(async () => {
    const hits = await kb.search(s, 80)
    activeKey.value = ''
    Object.assign(view, { type: 'search', crumb: [{ label: '全部体系', fn: goWelcome }, { label: '搜索 “' + s + '”' }], title: '', cards: [], terms: hits, hint: hits.length + ' 条结果' })
  }, 200)
}

async function loadBatch() {
  const data = await kb.batchTerms(cart.map((c) => c.term_uid))
  toast(data.count ? `批量获取 ${data.count} 条` : '没有可批量获取的术语')
  if (data.items.length) {
    Object.assign(view, {
      type: 'search',
      crumb: [{ label: '全部体系', fn: goWelcome }, { label: '提示词篮 · 批量获取' }],
      title: '',
      cards: [],
      terms: data.items,
      hint: data.missing_term_uids.length ? `缺失 ${data.missing_term_uids.length} 条` : '批量获取完成'
    })
    q.value = ''
    randomPanel.value = []
  }
}

async function mergeBasket() {
  const data = await kb.combinePrompts(cart.map((c) => c.term_uid), { language: copyLang.value, format: 'comma' })
  if (!data.combined) {
    toast('提示词篮是空的')
    return
  }
  await navigator.clipboard?.writeText(data.combined)
  copied.value = true
  setTimeout(() => (copied.value = false), 1200)
  showPrev.value = true
  toast(`已合并 ${data.count} 条`)
}

async function loadRandom() {
  const activeVol = view.code || ''
  const activeCat = currentCategoryPath()
  const data = await kb.randomTerms({
    count: 8,
    volume: activeVol || undefined,
    category: activeCat || undefined,
    category_prefix: activeCat || undefined
  })
  randomPanel.value = data.items || []
  Object.assign(view, {
    type: 'search',
    crumb: [{ label: '全部体系', fn: goWelcome }, { label: '随机术语' }],
    title: '',
    cards: [],
    terms: data.items || [],
    hint: `${data.count || 0}/${data.available || 0}`
  })
}

async function openDetail(t) {
  detailTerm.value = t
  if (t && t.term_uid && t.definition_long === undefined && kb.state.mode === 'api') {
    try { const full = await kb.termDetail(t.term_uid); if (full) detailTerm.value = full } catch (e) { /* 保底用列表项 */ }
  }
}
function copyText(text, e) { navigator.clipboard && navigator.clipboard.writeText(text); const b = e.target; const o = b.textContent; b.textContent = '已复制'; setTimeout(() => (b.textContent = o), 900) }

function inCart(uid) { return cart.some((c) => c.term_uid === uid) }
function toggleCart(t) { const i = cart.findIndex((c) => c.term_uid === t.term_uid); if (i >= 0) { cart.splice(i, 1); toast('− ' + t.zh_term) } else { cart.push(t); toast('+ ' + t.zh_term) } }
const conflictUids = computed(() => { const byp = {}; cart.forEach((c) => { (byp[c.category] = byp[c.category] || []).push(c.term_uid) }); const s = new Set(); Object.values(byp).forEach((a) => { if (a.length > 1) a.forEach((u) => s.add(u)) }); return s })
function termText(t, lang) { const en = t.en_term || t.zh_term; const cn = t.zh_term; return lang === 'cn' ? cn : lang === 'both' ? en + '（' + cn + '）' : en }
const promptText = computed(() => cart.map((c) => termText(c, copyLang.value)).filter(Boolean).join(', '))
function setLang(l) { copyLang.value = l; showPrev.value = true; toast('复制语言：' + ({ en: '英文', cn: '中文', both: '中英' }[l]) + (cart.length ? '' : '（篮中加词后生效）')) }
function copyAll() { if (!cart.length) { toast('提示词篮是空的'); return } navigator.clipboard && navigator.clipboard.writeText(promptText.value); showPrev.value = true; copied.value = true; setTimeout(() => (copied.value = false), 1200); toast('已复制 ' + cart.length + ' 项(' + ({ en: '英文', cn: '中文', both: '中英' }[copyLang.value]) + ')') }

function measureDock() { const d = dockRef.value; if (d) langBottom.value = d.getBoundingClientRect().height + 16 + 1 }
window.addEventListener('resize', measureDock)
</script>

<style scoped>
.app { height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
.topbar { height: 48px; flex: 0 0 48px; display: flex; align-items: center; gap: 12px; padding: 0 14px; background: var(--panel); backdrop-filter: saturate(180%) blur(20px); border-bottom: 1px solid var(--line); position: relative; z-index: 30; }
.toggle { width: 30px; height: 30px; border-radius: 8px; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; justify-content: center; color: var(--ink2); transition: .2s; }
.toggle:hover { background: var(--hov); transform: scale(1.05); }
.toggle svg { width: 17px; height: 17px; transition: transform .3s; }
.app.side-hidden .toggle svg { transform: scaleX(-1); }
.brand { font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px; }
.brand .mk { width: 18px; height: 18px; border-radius: 50%; border: 1.5px solid var(--ink); position: relative; transition: transform .5s cubic-bezier(.34,1.56,.64,1); }
.brand .mk i { position: absolute; inset: 5px; border-radius: 50%; background: var(--ink); }
.brand:hover .mk { transform: rotate(90deg); }
.brand .dot { color: var(--mut); margin: 0 6px; } .brand .sub { color: var(--mut); font-weight: 400; font-size: 12px; }
.modetag { font-size: 10.5px; color: #fff; background: var(--accent); border-radius: 6px; padding: 2px 8px; font-weight: 500; }
.search { margin-left: auto; position: relative; width: 280px; max-width: 40vw; }
.search input { width: 100%; height: 32px; border: 1px solid var(--line); border-radius: 8px; background: rgba(255,255,255,.6); padding: 0 12px 0 32px; font-size: 12.5px; font-family: var(--font); transition: .25s; color: var(--ink); }
.search input:focus { outline: none; border-color: var(--accent); background: #fff; box-shadow: 0 0 0 3px rgba(10,132,255,.12); }
.search svg { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); width: 14px; height: 14px; color: var(--mut); }
.tool { width: 30px; height: 30px; border-radius: 8px; border: 1px solid var(--line); background: #fff; color: var(--mut); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: .2s; }
.tool:hover { background: var(--hov); color: var(--ink2); }
.tool svg { width: 15px; height: 15px; }
.body { flex: 1; display: flex; min-height: 0; position: relative; }
.side { width: var(--side-w); flex: 0 0 var(--side-w); background: var(--panel); backdrop-filter: saturate(180%) blur(20px); border-right: 1px solid var(--line); display: flex; flex-direction: column; overflow: hidden; transition: width .32s cubic-bezier(.4,0,.2,1), flex-basis .32s, opacity .28s, border-color .28s; }
.app.side-hidden .side { width: 0; flex-basis: 0; opacity: 0; border-color: transparent; pointer-events: none; }
.side-hd { padding: 12px 14px 8px; font-size: 11px; font-weight: 600; letter-spacing: .05em; color: var(--mut); text-transform: uppercase; display: flex; justify-content: space-between; }
.side-hd .cnt { font-weight: 400; color: var(--faint); }
.tree { flex: 1; overflow-y: auto; padding: 2px 8px 90px; }
.trow { display: flex; align-items: stretch; gap: 6px; padding: 6px 8px; cursor: pointer; border-radius: 8px; margin: 1px 0; transition: background .15s, color .15s; min-height: 30px; }
.trow > * { align-self: center; }
.trow:hover { background: var(--hov); } .trow.on { background: var(--sel); color: #fff; }
.trow.on .tc { color: rgba(255,255,255,.55); }
.guide-cell { align-self: stretch; width: 14px; flex: 0 0 14px; border-left: 1px solid rgba(0,0,0,.09); }
.trow.on .guide-cell { border-color: rgba(255,255,255,.18); }
.tw { width: 13px; flex: 0 0 13px; text-align: center; color: var(--faint); font-size: 9px; transition: transform .25s; }
.trow.open > .tw { transform: rotate(90deg); }
.ico { width: 14px; flex: 0 0 14px; color: var(--mut); font-size: 11px; }
.tn { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.trow.lv1 .tn { font-weight: 550; } .trow.sub .tn { color: var(--ink2); font-size: 12.5px; }
.trow.on .tn, .trow.on .ico { color: #fff; }
.tc { font-size: 10.5px; color: var(--faint); }
.main { flex: 1; overflow-y: auto; padding: 18px 22px 130px; min-width: 0; }
.center-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 20px; gap: 14px; color: var(--mut); }
.center-state .big { font-size: 34px; opacity: .5; } .center-state.err .big { color: #e06c5e; }
.center-state pre { font-family: var(--font); font-size: 13px; line-height: 1.8; text-align: center; white-space: pre-wrap; }
.spinner { width: 26px; height: 26px; border: 2.5px solid var(--line); border-top-color: var(--accent); border-radius: 50%; animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.crumb { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-bottom: 18px; font-size: 12px; min-height: 22px; }
.crumb .seg { display: inline-flex; align-items: center; padding: 3px 10px; border-radius: 20px; background: rgba(255,255,255,.6); border: 1px solid var(--line); color: var(--ink2); cursor: pointer; transition: .18s; }
.crumb .seg:hover { background: #fff; color: var(--ink); transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,.06); }
.crumb .seg.cur { background: var(--sel); color: #fff; border-color: var(--sel); cursor: default; }
.crumb .seg.cur:hover { transform: none; box-shadow: none; }
.crumb .arr { color: var(--faint); } .crumb .hint { color: var(--mut); margin-left: 8px; }
.secgrp { margin-bottom: 22px; } .gh { display: flex; align-items: center; gap: 9px; margin-bottom: 11px; }
.gh .gt { font-size: 13px; font-weight: 600; } .gh .gline { flex: 1; height: 1px; background: linear-gradient(90deg, var(--line), transparent); }
.gh .gn { font-size: 11px; color: var(--faint); background: rgba(0,0,0,.04); padding: 1px 8px; border-radius: 10px; }
.vq-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }
.vq { background: var(--panel-solid); border: 1px solid var(--line); border-radius: 10px; padding: 11px 13px; cursor: pointer; font-size: 12.5px; font-weight: 500; color: var(--ink2); display: flex; justify-content: space-between; align-items: center; gap: 4px; transition: .18s; text-align: left; }
.vq span { font-size: 10.5px; color: var(--faint); background: rgba(0,0,0,.04); padding: 1px 7px; border-radius: 9px; }
.vq:hover { transform: translateY(-2px); box-shadow: var(--shadow); border-color: rgba(0,0,0,.14); color: var(--ink); }
.chips { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 8px; }
.cchip { background: var(--panel-solid); border: 1px solid var(--line); border-radius: 10px; padding: 9px 11px; cursor: pointer; position: relative; overflow: hidden; transition: .2s; }
.cchip:hover { transform: translateY(-2px); box-shadow: var(--shadow); border-color: rgba(0,0,0,.14); }
.cchip:active { transform: translateY(0) scale(.98); }
.cchip .cn { font-size: 12.5px; font-weight: 550; margin-bottom: 2px; }
.cchip .ce { font-size: 10.5px; color: var(--mut); font-family: var(--mono); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cchip.sel { background: var(--sel); border-color: var(--sel); } .cchip.sel .cn { color: #fff; } .cchip.sel .ce { color: rgba(255,255,255,.6); }
.cchip .add { position: absolute; top: 7px; right: 7px; width: 19px; height: 19px; border-radius: 50%; background: var(--sel); color: #fff; font-size: 13px; line-height: 19px; text-align: center; opacity: 0; transform: scale(.7); transition: .2s cubic-bezier(.34,1.56,.64,1); }
.cchip:hover .add { opacity: 1; transform: scale(1); } .cchip.sel .add { opacity: 1; background: #fff; color: var(--sel); }
.welcome { display: flex; justify-content: center; padding-top: 40px; } .welcome-card { text-align: center; max-width: 640px; }
.welcome-card .big { font-size: 40px; opacity: .4; margin-bottom: 10px; } .welcome-card h3 { font-size: 17px; margin-bottom: 6px; }
.welcome-card p { color: var(--mut); font-size: 13px; margin-bottom: 22px; }
.detail { position: fixed; right: 14px; top: 62px; bottom: 128px; width: 338px; background: var(--panel-solid); border: 1px solid var(--line); border-radius: 18px; box-shadow: var(--shadow-lg); padding: 20px; overflow: auto; transform: translateX(calc(100% + 24px)); opacity: 0; transition: transform .35s cubic-bezier(.32,.72,0,1), opacity .28s; z-index: 46; }
.detail.open { transform: none; opacity: 1; }
.detail .x { position: absolute; top: 14px; right: 14px; width: 26px; height: 26px; border-radius: 50%; border: none; background: rgba(0,0,0,.05); cursor: pointer; color: var(--ink2); font-size: 14px; transition: .2s; }
.detail .x:hover { background: rgba(0,0,0,.1); transform: rotate(90deg); }
.detail .lin { font-size: 11px; color: var(--mut); line-height: 1.8; background: var(--bg); border-radius: 12px; padding: 11px 13px; margin-bottom: 16px; }
.detail .lin b { color: var(--ink); } .detail .lin .tag { font-size: 9px; color: var(--mut); margin-left: 6px; border: 1px solid var(--line); border-radius: 4px; padding: 0 4px; }
.detail h2 { font-size: 21px; margin-bottom: 3px; } .detail .den { font-size: 12px; color: var(--mut); font-family: var(--mono); margin-bottom: 14px; }
.detail .dnote { font-size: 13px; color: var(--ink2); line-height: 1.6; margin-bottom: 16px; }
.detail .sec { margin-bottom: 14px; } .detail .stext { font-size: 13px; color: var(--ink2); line-height: 1.65; }
.detail .namehint { font-size: 10.5px; color: var(--faint); margin: -6px 0 14px; }
.detail .chips { display: flex; flex-wrap: wrap; gap: 6px; }
.detail .chip { font-size: 12px; color: var(--ink2); background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 3px 9px; }
.detail .chip.ctag { background: var(--hov); }
.cpname { margin-left: 8px; font-size: 10px; vertical-align: middle; background: var(--hov); border: 1px solid var(--line); color: var(--mut); border-radius: 6px; padding: 1px 7px; cursor: pointer; font-family: var(--font); }
.cpname:hover { background: var(--ink); color: #fff; }
.slabel { font-size: 11px; font-weight: 600; color: var(--mut); text-transform: uppercase; letter-spacing: .04em; margin: 0 0 6px; display: flex; align-items: center; gap: 6px; }
.slabel .lg { font-size: 9px; background: var(--accent); color: #fff; border-radius: 3px; padding: 0 4px; } .slabel .lg.cn { background: #7a52cc; }
.pb { background: #1d1d1f; color: #e8e8ea; border-radius: 12px; padding: 11px 13px; font-family: var(--mono); font-size: 12px; line-height: 1.5; word-break: break-word; margin-bottom: 8px; position: relative; } .pb.cn { background: #222033; color: #e7e3f5; }
.pb .cp { position: absolute; top: 7px; right: 7px; background: rgba(255,255,255,.12); border: none; color: #fff; border-radius: 6px; padding: 2px 8px; font-size: 10px; cursor: pointer; }
.pb .cp:hover { background: rgba(255,255,255,.22); }
.dbtn { width: 100%; background: var(--sel); color: #fff; border: none; border-radius: 12px; padding: 12px; font-size: 13px; font-weight: 550; cursor: pointer; transition: .2s; margin-top: 6px; }
.dbtn:hover { background: #000; transform: translateY(-1px); } .dbtn.added { background: #28a745; }
.dock { position: fixed; left: calc(var(--side-w) + 16px); right: 16px; bottom: 16px; background: rgba(250,250,252,.85); backdrop-filter: saturate(180%) blur(30px); border: 1px solid rgba(0,0,0,.07); border-radius: 18px; box-shadow: 0 1px 1px rgba(0,0,0,.04), 0 10px 34px rgba(0,0,0,.1), inset 0 1px 0 rgba(255,255,255,.7); padding: 9px 11px; z-index: 45; transition: left .32s cubic-bezier(.4,0,.2,1); }
.app.side-hidden .dock { left: 16px; }
.langfloat { position: fixed; left: calc(var(--side-w) + 17px); z-index: 47; transition: left .32s cubic-bezier(.4,0,.2,1); }
.app.side-hidden .langfloat { left: 17px; }
.seg-ctl { display: flex; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: rgba(255,255,255,.92); backdrop-filter: blur(10px); box-shadow: 0 2px 8px rgba(0,0,0,.1); }
.seg-ctl button { border: none; background: transparent; font-size: 11px; padding: 4px 10px; cursor: pointer; color: var(--mut); font-weight: 600; transition: .15s; }
.seg-ctl button.on { background: var(--ink); color: #fff; }
.dock-top { display: flex; align-items: center; gap: 10px; }
.dlbl { font-size: 12px; color: var(--ink); font-weight: 600; display: flex; align-items: center; gap: 7px; white-space: nowrap; }
.dlbl .icn { width: 26px; height: 26px; border-radius: 8px; background: #fff; border: 1px solid var(--line); display: inline-flex; align-items: center; justify-content: center; }
.dlbl .icn svg { width: 13px; height: 13px; color: var(--ink2); }
.dlbl .num { background: #ededf0; color: var(--ink2); font-size: 10.5px; min-width: 18px; height: 18px; border-radius: 9px; display: inline-flex; align-items: center; justify-content: center; padding: 0 5px; font-weight: 600; }
.divd { width: 1px; height: 22px; background: var(--line); }
.frags { flex: 1; display: flex; gap: 6px; overflow-x: auto; min-height: 34px; align-items: center; }
.frags::-webkit-scrollbar { display: none; }
.frags.expanded { flex-wrap: wrap; max-height: 160px; overflow-y: auto; align-items: flex-start; padding: 2px 0; }
.frags .ph { color: var(--mut); font-size: 12px; white-space: nowrap; padding-left: 2px; }
.frag { background: #fff; border: 1px solid var(--line); color: var(--ink2); border-radius: 8px; padding: 5px 6px 5px 8px; font-size: 12px; display: flex; gap: 6px; align-items: center; white-space: nowrap; box-shadow: 0 1px 1.5px rgba(0,0,0,.04); }
.frag.conflict { border-color: var(--danger); background: #fff1f0; color: var(--danger); }
.frag .fdot { width: 6px; height: 6px; border-radius: 50%; background: var(--danger); flex: 0 0 6px; }
.frag x { cursor: pointer; color: var(--faint); font-size: 12px; width: 15px; height: 15px; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: .15s; }
.frag.conflict x { color: var(--danger); } .frag x:hover { color: #fff; background: #1d1d1f; }
.acts { display: flex; gap: 6px; align-items: center; }
.ic { width: 31px; height: 31px; border-radius: 8px; border: 1px solid var(--line); background: #fff; color: var(--mut); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: .18s; }
.ic:hover { background: var(--hov); color: var(--ink2); } .ic.on { background: var(--ink); color: #fff; border-color: var(--ink); }
.ic svg { width: 15px; height: 15px; }
.copy { background: var(--ink); color: #fff; border: none; border-radius: 8px; padding: 0 14px; height: 31px; font-size: 12.5px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: .2s; box-shadow: 0 1px 3px rgba(0,0,0,.2); white-space: nowrap; }
.copy:hover { background: #000; transform: translateY(-1px); } .copy.done { background: #28c840; }
.dock-prev { margin-top: 9px; padding-top: 9px; border-top: 1px solid var(--line); font-family: var(--mono); font-size: 11.5px; color: var(--ink2); line-height: 1.55; word-break: break-word; max-height: 0; opacity: 0; overflow: hidden; transition: max-height .3s cubic-bezier(.4,0,.2,1), opacity .25s, margin-top .3s, padding-top .3s; }
.dock-prev.show { max-height: 96px; opacity: 1; overflow: auto; }
.dock-prev .pl { color: var(--faint); } .dock-prev b { color: var(--accent); font-weight: 600; } .dock-prev .warn { color: var(--danger); font-weight: 600; }
.toast { position: fixed; top: 60px; left: 50%; transform: translateX(-50%) translateY(-20px); background: var(--sel); color: #fff; padding: 8px 18px; border-radius: 10px; font-size: 12.5px; font-weight: 500; opacity: 0; pointer-events: none; z-index: 99; transition: .3s cubic-bezier(.34,1.56,.64,1); }
.toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
.random-panel { position: fixed; left: calc(var(--side-w) + 16px); right: 16px; top: 62px; background: rgba(250,250,252,.96); border: 1px solid var(--line); border-radius: 16px; box-shadow: var(--shadow-lg); padding: 14px; z-index: 44; max-height: 250px; overflow: auto; }
.app.side-hidden .random-panel { left: 16px; }
.mini { border: 1px solid var(--line); background: #fff; color: var(--ink2); border-radius: 8px; height: 26px; padding: 0 10px; cursor: pointer; }
.mini:hover { background: var(--hov); }
@media (max-width: 880px) { .search { width: 160px; } }
</style>

<template>
  <div class="app" :class="{ 'side-hidden': sideCollapsed, 'detail-open': !!detailTerm }">
    <header class="mtop">
      <button class="mbtn" aria-label="打开导航" @click="sideOpen = true"><Icon name="panelLeft" /></button>
      <input
        class="msearch"
        :value="q"
        type="search"
        placeholder="搜索术语…"
        autocomplete="off"
        @input="onSearch($event.target.value)"
      >
      <span class="mnum">{{ totalTerms.toLocaleString() }}</span>
    </header>
    <div class="frame">
      <div class="scrim-side" :class="{ show: sideOpen }" @click="sideOpen = false"></div>
      <div class="scrim-detail" :class="{ show: !!detailTerm }" @click="closeDetail"></div>
      <button v-if="sideCollapsed" class="unfold" title="展开侧栏 (Ctrl+\)" @click="sideCollapsed = false">
        <Icon name="panelLeft" />
      </button>
      <SideNav
        ref="sideNav"
        :rows="flatRows"
        :active-key="activeKey"
        :q="q"
        :mode="kb.state.mode"
        :total-terms="totalTerms"
        :target-total="targetTotal"
        :progress-pct="progressPct"
        :random-loading="randomLoading"
        :class="{ open: sideOpen }"
        @row-click="onRowClick"
        @caret="onCaret"
        @search="onSearch"
        @random="loadRandom"
        @go-root="showOverview"
        @toggle-side="sideCollapsed = !sideCollapsed"
      />

      <div class="workcol">
        <div class="workrow">
      <main class="main">
        <!-- 背景点缀：水墨竹枝（纯线条 SVG），极慢摇曳 -->
        <div class="wm" aria-hidden="true">
          <svg viewBox="0 0 220 420" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g class="bam bam-main">
              <g stroke="#1b1b1d" stroke-width="5" stroke-linecap="round">
                <path d="M152 412 L151 346" /><path d="M151 338 L150 268" />
                <path d="M150 260 L150 186" /><path d="M150 178 L151 102" />
                <path d="M151 94 L153 34" />
              </g>
              <g stroke="#1b1b1d" stroke-width="2" stroke-linecap="round">
                <path d="M146 342 h11" /><path d="M145 264 h11" />
                <path d="M145 182 h11" /><path d="M146 98 h11" />
              </g>
              <g class="leaf la" fill="#1b1b1d">
                <path d="M153 96 Q175 100 198 118 Q173 112 153 102 Z" />
                <path d="M153 96 Q170 108 182 132 Q164 116 151 102 Z" />
                <path d="M153 96 Q148 118 132 136 Q142 116 149 99 Z" />
              </g>
              <g class="leaf lb" fill="#1b1b1d">
                <path d="M150 184 Q128 190 108 208 Q130 200 150 190 Z" />
                <path d="M150 184 Q136 198 128 220 Q140 202 152 190 Z" />
              </g>
            </g>
            <g class="bam bam-second">
              <g stroke="#1b1b1d" stroke-width="3" stroke-linecap="round">
                <path d="M92 414 L96 342" /><path d="M97 334 L101 262" />
                <path d="M102 254 L106 190" />
              </g>
              <g stroke="#1b1b1d" stroke-width="1.8" stroke-linecap="round">
                <path d="M92 338 h9" /><path d="M97 258 h9" />
              </g>
              <g class="leaf lc" fill="#1b1b1d">
                <path d="M106 192 Q88 200 70 220 Q90 208 108 198 Z" />
                <path d="M106 192 Q112 212 106 236 Q104 214 102 197 Z" />
                <path d="M106 192 Q122 202 132 222 Q118 208 104 198 Z" />
              </g>
            </g>
          </svg>
        </div>
        <div class="inner">
          <div v-if="!kb.state.ready && !kb.state.error" class="center-state">
            <div class="spinner"></div>
            <div>加载知识库…</div>
          </div>
          <div v-else-if="kb.state.error" class="center-state err">
            <pre>{{ kb.state.error }}</pre>
          </div>
          <div v-else class="viewwrap" :key="view.type + '|' + view.code + '|' + view.path + '|' + view.title">
            <PageHead :crumb="view.crumb" :title="view.title" :desc="view.desc" :metas="view.metas" />
            <VolumeGrid v-if="view.type === 'overview'" :volumes="vols" @select="(code) => navigate(code, null)" />
            <BranchGrid v-else-if="view.cards.length" :cards="view.cards" @open="(c) => navigate(view.code, c.path)" />
            <TermTable
              v-else
              :terms="view.terms"
              :selected-uid="detailTerm ? detailTerm.term_uid : ''"
              :empty-text="view.type === 'search' || view.type === 'random' ? '没有匹配的术语' : ''"
              @select="openDetail"
              @toggle="toggleCart"
            />
          </div>
        </div>
      </main>

      <aside class="detailcol">
        <TermDetail :term="detailTerm" @toggle="toggleCart" @jump="jumpToZh" @close="closeDetail" />
      </aside>
        </div>

        <PromptBar />
      </div>
    </div>

    <div class="toast" :class="{ show: !!toastMsg }">{{ toastMsg }}</div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useKB } from './composables/useKB'
import { useCart } from './composables/useCart'
import Icon from './components/Icon.vue'
import SideNav from './components/SideNav.vue'
import PageHead from './components/PageHead.vue'
import VolumeGrid from './components/VolumeGrid.vue'
import BranchGrid from './components/BranchGrid.vue'
import TermTable from './components/TermTable.vue'
import TermDetail from './components/TermDetail.vue'
import PromptBar from './components/PromptBar.vue'

const kb = useKB()
const cart = useCart()
const SEP = ' / '

const sideNav = ref(null)
const sideCollapsed = ref(false)
const sideOpen = ref(false)   // 窄屏抽屉
const q = ref('')
const expanded = reactive(new Set())
const volTrees = reactive({})
const loadingVol = reactive(new Set())
const activeKey = ref('')
const detailTerm = ref(null)
const randomLoading = ref(false)
const toastMsg = ref('')
let toastTimer = null

const view = reactive({
  type: 'overview', crumb: [{ label: '全部体系' }], title: '', desc: '', metas: [],
  cards: [], terms: [], code: '', path: '',
})

onMounted(async () => {
  await kb.init()
  if (kb.state.ready) {
    if ((location.hash || '').length > 2) await applyHash()
    else showOverview()
  }
  window.addEventListener('keydown', onKey)
  window.addEventListener('popstate', applyHash)
  window.addEventListener('hashchange', applyHash)
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKey)
  window.removeEventListener('popstate', applyHash)
  window.removeEventListener('hashchange', applyHash)
})

const vols = computed(() => (kb.state.index ? kb.state.index.volumes : []))
const totalTerms = computed(() => (kb.state.index ? kb.state.index.total_terms || 0 : 0))
const targetTotal = computed(() => {
  if (!kb.state.index) return 0
  return kb.state.index.target_total || vols.value.reduce((s, v) => s + (v.target_terms || 0), 0)
})
const progressPct = computed(() =>
  targetTotal.value ? Math.max(1.5, totalTerms.value * 100 / targetTotal.value) : 0
)

function toast(m) {
  toastMsg.value = m
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMsg.value = ''), 1600)
}

/* ---------- hash 路由：#/V01/~<base64url路径>/@V01_T0001 ----------
   分类路径用 base64url 编码，地址栏纯 ASCII 无中文/百分号；
   旧格式（中文分段）仍可解析，历史分享链接不失效。 */
function b64urlEncode(s) {
  const bytes = new TextEncoder().encode(s)
  let bin = ''
  bytes.forEach((b) => (bin += String.fromCharCode(b)))
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
}
function b64urlDecode(s) {
  try {
    const b64 = s.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - (s.length % 4)) % 4)
    const bin = atob(b64)
    return new TextDecoder().decode(Uint8Array.from(bin, (c) => c.charCodeAt(0)))
  } catch (e) {
    return ''
  }
}
let applyingHash = false
function syncHash() {
  if (applyingHash) return
  let h = '#/'
  if (view.code && (view.type === 'volume' || view.type === 'node')) {
    h = '#/' + view.code
    if (view.path) h += '/~' + b64urlEncode(view.path)
    if (detailTerm.value && view.type === 'node' && !view.cards.length) h += '/@' + detailTerm.value.term_uid
  }
  if (location.hash !== h) {
    // 仅「关闭详情」（当前 hash 去掉 @uid 后与目标一致）用 replaceState，不再压历史条目
    const closingDetail = location.hash.replace(/\/@[^/]+$/, '') === h
    if (closingDetail) history.replaceState(null, '', h)
    else history.pushState(null, '', h)
  }
}
async function applyHash() {
  if (!kb.state.ready) return
  applyingHash = true
  try {
    const raw = (location.hash || '').replace(/^#\/?/, '')
    if (!raw) { showOverview(); return }
    const parts = raw.split('/').map((s) => decodeURIComponent(s)).filter(Boolean)
    const code = parts.shift()
    if (code === 'basket' && parts.length) {
      // 分享链接还原整篮：#/basket/uid1,uid2,…
      const uids = parts[0].split(',').map((s) => s.trim()).filter(Boolean)
      const data = await kb.batchTerms(uids)
      if (data.items && data.items.length) {
        cart.clear()
        data.items.forEach((t) => cart.toggle(t))
        toast('已从链接还原提示词篮 ' + data.items.length + ' 项')
      }
      showOverview()
      return
    }
    let uid = null
    if (parts.length && parts[parts.length - 1].startsWith('@')) uid = parts.pop().slice(1)
    let path = null
    if (parts.length === 1 && parts[0].startsWith('~')) path = b64urlDecode(parts[0].slice(1)) || null
    else path = parts.join(SEP) || null  // 旧格式：中文分段，向后兼容
    if (!vols.value.some((v) => v.code === code)) { showOverview(); return }
    if (view.code !== code || (view.path || null) !== path) await navigate(code, path)
    if (uid && (!detailTerm.value || detailTerm.value.term_uid !== uid)) {
      let t = view.terms.find((x) => x.term_uid === uid) || null
      if (!t && kb.state.mode === 'api') t = await kb.termDetail(uid).catch(() => null)
      if (t) await openDetail(t)
    } else if (!uid) {
      detailTerm.value = null  // 浏览器返回键去掉 @uid → 同步关闭详情层
    }
  } finally {
    applyingHash = false
  }
}
function onKey(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); sideNav.value && sideNav.value.focusSearch() }
  if ((e.metaKey || e.ctrlKey) && e.key === '\\') { e.preventDefault(); sideCollapsed.value = !sideCollapsed.value }
  if (e.key === 'Escape') {
    if (sideOpen.value) sideOpen.value = false
    else if (q.value) { cancelSearch(); showOverview() }
    else if (detailTerm.value) closeDetail()
  }
}

function closeDetail() {
  detailTerm.value = null
  syncHash()  // 回写 hash（去掉 @uid），避免刷新后详情复活
}

/* ---------- 分类树（客户端懒加载建树，与数据层解耦） ---------- */
function buildTree(terms) {
  const root = { name: '', path: '', children: new Map(), terms: [], count: 0 }
  for (const t of terms) {
    const segs = (t.category || '未分类').split(SEP).map((s) => s.trim()).filter(Boolean)
    let node = root
    const parts = []
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
function findNode(code, path) {
  let n = volTrees[code]
  if (!n) return null
  for (const s of path.split(SEP)) {
    if (!n.children.has(s)) return null
    n = n.children.get(s)
  }
  return n
}
async function ensureVol(code) {
  if (volTrees[code]) return volTrees[code]
  loadingVol.add(code)
  try {
    const terms = await kb.loadVolumeTerms(code)
    volTrees[code] = buildTree(terms)
  } finally {
    loadingVol.delete(code)
  }
  return volTrees[code]
}

const flatRows = computed(() => {
  const rows = []
  for (const v of vols.value) {
    const vkey = 'V|' + v.code
    const open = expanded.has(vkey)
    rows.push({
      type: 'vol', key: vkey, code: v.code, title: v.code + ' · ' + v.title,
      count: v.current_terms, depth: 0, hasKids: true, open,
      loading: loadingVol.has(v.code),
    })
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
  for (const k of [...expanded]) {
    if (k === 'V|' + code) continue
    if (k.startsWith('N|' + code + '|')) continue
    expanded.delete(k)
  }
  expanded.add('V|' + code)
}
function onCaret(r) {
  if (!r.hasKids) return
  if (r.type === 'vol') { onRowClick(r); return }
  if (expanded.has(r.key)) { for (const k of [...expanded]) if (k === r.key || k.startsWith(r.key + SEP)) expanded.delete(k) }
  else expanded.add(r.key)
}
async function onRowClick(r) {
  cancelSearch()
  if (r.type !== 'vol') sideOpen.value = false  // 窄屏点中分类后收起抽屉（点卷展开树时保留）
  if (r.type === 'vol') {
    await ensureVol(r.code)
    const was = expanded.has(r.key)
    setVolExclusive(r.code)
    if (was) { for (const k of [...expanded]) if (k === r.key || k.startsWith('N|' + r.code + '|')) expanded.delete(k) }
    activeKey.value = r.key
    showVolume(r.code)
  } else {
    if (r.hasKids && !expanded.has(r.key)) expanded.add(r.key)
    activeKey.value = r.key
    await showNode(r.code, r.path)
  }
}

/* ---------- 视图 ---------- */
function showOverview() {
  activeKey.value = ''
  cancelSearch()
  sideOpen.value = false
  Object.assign(view, {
    type: 'overview',
    crumb: [{ label: '全部体系' }],
    title: '全部体系',
    desc: '层级不限深度：体系 → 分支 → 术语。点击进入任意体系浏览分类树，术语名字即提示词。',
    metas: [
      { icon: 'layers', label: '体系', num: vols.value.length },
      { icon: 'tag', label: '已收录', num: totalTerms.value.toLocaleString() },
      { icon: 'folderTree', label: '目标', num: targetTotal.value.toLocaleString() },
    ],
    cards: [], terms: [], code: '', path: '',
  })
  detailTerm.value = null
  syncHash()
}
function showVolume(code) {
  const v = vols.value.find((x) => x.code === code)
  const root = volTrees[code]
  const cards = root
    ? [...root.children.values()].map((n) => ({ name: n.name, path: n.path, childCount: n.children.size, count: n.count }))
    : []
  Object.assign(view, {
    type: 'volume',
    crumb: [{ label: '全部体系', fn: showOverview }, { label: v.code + ' ' + v.title }],
    title: v.title,
    desc: v.purpose || '',
    metas: [
      { icon: 'folderTree', label: '分支', num: cards.length },
      { icon: 'tag', label: '术语', num: v.current_terms },
      { icon: 'layers', label: '目标', num: v.target_terms },
    ],
    cards, terms: [], code, path: '',
  })
  syncHash()
}
async function showNode(code, path) {
  const v = vols.value.find((x) => x.code === code)
  const node = findNode(code, path)
  if (!node) return
  const segs = path.split(SEP)
  const crumb = [{ label: '全部体系', fn: showOverview }, { label: v.code + ' ' + v.title, fn: () => navigate(code, null) }]
  const acc = []
  segs.forEach((s, i) => {
    acc.push(s)
    const p = acc.join(SEP)
    crumb.push(i === segs.length - 1 ? { label: s } : { label: s, fn: () => navigate(code, p) })
  })
  const kids = [...node.children.values()].map((n) => ({ name: n.name, path: n.path, childCount: n.children.size, count: n.count }))
  // 只取「直属本层」的术语；分支节点点进子类才看到术语
  const terms = kids.length ? [] : await kb.loadCategoryTerms(code, path)
  Object.assign(view, {
    type: 'node',
    crumb,
    title: node.name,
    desc: '',
    metas: kids.length
      ? [{ icon: 'folderTree', label: '分支', num: kids.length }, { icon: 'tag', label: '术语', num: node.count }]
      : [{ icon: 'tag', label: '术语', num: terms.length }, { icon: 'layers', label: '同叶互斥', num: '' }],
    cards: kids, terms, code, path,
  })
  syncHash()
}
async function navigate(code, path) {
  cancelSearch()
  await ensureVol(code)
  setVolExclusive(code)
  if (path) {
    const segs = path.split(SEP)
    const acc = []
    for (const s of segs) { acc.push(s); expanded.add('N|' + code + '|' + acc.join(SEP)) }
    activeKey.value = 'N|' + code + '|' + path
    await showNode(code, path)
  } else {
    activeKey.value = 'V|' + code
    showVolume(code)
  }
}

/* ---------- 搜索 / 随机 ---------- */
let searchTimer = null
let searchSeq = 0
function cancelSearch() {
  clearTimeout(searchTimer)
  searchSeq += 1  // 使在途搜索回调过期，防止幽灵搜索页覆盖当前视图
  q.value = ''
}
function onSearch(value) {
  q.value = value
  clearTimeout(searchTimer)
  const s = value.trim()
  if (!s) {
    const keepDrawer = sideOpen.value  // 抽屉内清空搜索词不应关掉抽屉
    showOverview()
    sideOpen.value = keepDrawer
    return
  }
  const seq = ++searchSeq
  searchTimer = setTimeout(async () => {
    const hits = await kb.search(s, 80)
    if (seq !== searchSeq || q.value.trim() !== s) return  // 已导航走 / 输入已变，丢弃过期结果
    activeKey.value = ''
    Object.assign(view, {
      type: 'search',
      crumb: [{ label: '全部体系', fn: showOverview }, { label: '搜索' }],
      title: '搜索 “' + s + '”',
      desc: '',
      metas: [{ icon: 'tag', label: '结果', num: hits.length }],
      cards: [], terms: hits, code: '', path: '',
    })
  }, 200)
}
async function loadRandom() {
  if (randomLoading.value) return
  randomLoading.value = true
  try {
    const data = await kb.randomTerms({
      count: 12,
      volume: view.code || undefined,
      category: view.path || undefined,
      category_prefix: view.path || undefined,
    })
    activeKey.value = ''
    Object.assign(view, {
      type: 'random',
      crumb: [{ label: '全部体系', fn: showOverview }, { label: '随机术语' }],
      title: '随机术语',
      desc: '',
      metas: [{ icon: 'shuffle', label: '抽取', num: (data.count || 0) + ' / ' + (data.available || 0) }],
      cards: [], terms: data.items || [], code: view.code, path: view.path,
    })
  } finally {
    randomLoading.value = false
  }
}

/* ---------- 详情 / 提示词栏 ---------- */
async function openDetail(t) {
  detailTerm.value = t
  if (t && t.term_uid && t.definition_long === undefined && kb.state.mode === 'api') {
    try {
      const full = await kb.termDetail(t.term_uid)
      if (full) detailTerm.value = full
    } catch (e) { /* 保底用列表项 */ }
  }
  syncHash()
}
function toggleCart(t) {
  const added = cart.toggle(t)
  toast((added ? '+ ' : '− ') + t.zh_term)
}
async function jumpToZh(zhName) {
  const hits = await kb.search(zhName, 10)
  const hit = hits.find((h) => h.zh_term === zhName) || hits[0]
  if (!hit) { toast('未找到「' + zhName + '」'); return }
  await navigate(hit.volume_code, hit.category || null)
  openDetail(hit)
}
</script>

<style scoped>
/* 100dvh：移动端浏览器工具栏展开/收起时取真实可视高度，旧浏览器回退 100vh */
.app { height: 100vh; height: 100dvh; display: flex; flex-direction: column; overflow: hidden; }
.frame { flex: 1; display: flex; min-height: 0; position: relative; }
.mtop { display: none; }
.scrim-side, .scrim-detail { display: none; }
.unfold { display: none; }
@media (min-width: 621px) {
  /* 折叠态的可见还原入口（触屏设备没有 Ctrl+\） */
  .unfold {
    display: flex; position: absolute; left: 10px; top: 14px; z-index: 10;
    width: 30px; height: 30px; align-items: center; justify-content: center;
    border: 1px solid var(--line-2); border-radius: var(--r-sm);
    background: var(--surface); color: var(--ink-2);
  }
  .unfold:hover { border-color: var(--ink); color: var(--ink); }
}
@media (min-width: 621px) {
  .app.side-hidden :deep(.side) { width: 0; flex-basis: 0; opacity: 0; pointer-events: none; }
}
/* 中屏 621–880：侧栏保持常驻但收窄，内容推排不遮盖 */
@media (min-width: 621px) and (max-width: 880px) {
  :deep(.side) { width: 240px; flex: 0 0 240px; }
}
/* 右侧工作列：中栏+右栏在上，提示词篮在下——篮子不横穿左侧栏 */
.workcol { flex: 1; min-width: 0; display: flex; flex-direction: column; min-height: 0; }
.workrow { flex: 1; display: flex; min-height: 0; }
.main { flex: 1; min-width: 0; overflow-y: auto; position: relative; }
.inner { max-width: 880px; padding: 26px 34px 48px; position: relative; z-index: 1; }
/* 留白处的水墨竹枝：整体 8% 墨色，竿与叶各自极慢摇曳（动中有静） */
.wm {
  position: absolute; top: 8px; right: 22px; z-index: 0;
  width: 210px; opacity: .08;
  pointer-events: none; user-select: none;
}
.wm svg { display: block; width: 100%; height: auto; }
.wm .bam { transform-box: fill-box; transform-origin: 50% 100%; }
.wm .bam-main { animation: bam-sway 9s ease-in-out infinite alternate; }
.wm .bam-second { animation: bam-sway 7s ease-in-out infinite alternate-reverse; }
.wm .leaf { transform-box: fill-box; transform-origin: 0% 0%; }
.wm .la { animation: leaf-sway 5.5s ease-in-out infinite alternate; }
.wm .lb { animation: leaf-sway 6.5s ease-in-out infinite alternate-reverse; }
.wm .lc { animation: leaf-sway 7.2s ease-in-out infinite alternate; }
@keyframes bam-sway { from { transform: rotate(-.7deg); } to { transform: rotate(.9deg); } }
@keyframes leaf-sway { from { transform: rotate(-2.2deg); } to { transform: rotate(2.6deg); } }
@media (max-width: 880px) { .wm { display: none; } }

/* 视图切换的轻微淡入上浮（静中有动；reduced-motion 下全局禁用） */
.viewwrap { animation: view-in .32s ease both; }
@keyframes view-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.detailcol { width: 336px; flex: 0 0 336px; overflow-y: auto; padding: 30px 26px 48px 6px; }
.center-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 90px 20px; gap: 14px; color: var(--ink-3);
}
.center-state pre { font-family: var(--font, var(--sans)); font-size: 13px; line-height: 1.8; text-align: center; white-space: pre-wrap; color: var(--danger); }
.spinner { width: 26px; height: 26px; border: 2.5px solid var(--line); border-top-color: var(--accent); border-radius: 50%; animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.toast {
  position: fixed; top: 18px; left: 50%; transform: translateX(-50%);
  background: var(--accent); color: #fff; padding: 8px 18px; border-radius: var(--r);
  font-size: 12.5px; font-weight: 500; opacity: 0; pointer-events: none; z-index: 99;
  transition: opacity .25s ease;
}
.toast.show { opacity: 1; }
/* ---------- 平板 ≤1100px：详情列改为右侧滑出层 ---------- */
@media (max-width: 1100px) {
  .detailcol {
    position: fixed; top: 0; right: 0; bottom: 0; z-index: 72;
    width: min(400px, 94vw); background: var(--surface);
    box-shadow: var(--sh-md); border-left: 1px solid var(--line);
    padding: 16px 18px 40px;
    transform: translateX(103%); transition: transform .28s ease;
  }
  .app.detail-open .detailcol { transform: none; }
  .scrim-detail {
    display: block; position: fixed; inset: 0; z-index: 71;
    background: rgba(20, 20, 22, .35);
    opacity: 0; pointer-events: none; transition: opacity .2s ease;
  }
  .scrim-detail.show { opacity: 1; pointer-events: auto; }
}

/* ---------- 中屏 ≤880px：仅收紧留白（侧栏仍常驻推排） ---------- */
@media (max-width: 880px) {
  .inner { padding: 18px 16px 40px; }
  .toast { top: 62px; max-width: 90vw; }
}

/* ---------- 手机 ≤620px：顶栏 + 侧栏抽屉（此宽度下两栏放不下才悬浮） ---------- */
@media (max-width: 620px) {
  .mtop {
    display: flex; align-items: center; gap: 10px;
    flex: 0 0 52px; height: 52px; padding: 0 12px;
    background: var(--surface); border-bottom: 1px solid var(--line);
  }
  .mbtn {
    width: 36px; height: 36px; flex: 0 0 36px;
    border: 1px solid var(--line-2); border-radius: var(--r-sm);
    display: flex; align-items: center; justify-content: center; color: var(--ink-2);
  }
  .msearch {
    flex: 1; min-width: 0; height: 34px; padding: 0 11px;
    border: 1px solid var(--line-2); border-radius: var(--r);
    background: var(--bg); color: var(--ink); font: 13px var(--sans);
  }
  .msearch:focus { outline: none; border-color: var(--accent); }
  .mnum { font-family: var(--mono); font-size: 11px; color: var(--ink-3); white-space: nowrap; }

  :deep(.side) {
    position: fixed; left: 0; top: 0; bottom: 0; z-index: 76;
    width: min(300px, 85vw); flex-basis: auto;
    transform: translateX(-103%); transition: transform .25s ease;
  }
  :deep(.side.open) { transform: none; box-shadow: var(--sh-md); }
  .scrim-side {
    display: block; position: fixed; inset: 0; z-index: 75;
    background: rgba(20, 20, 22, .48);  /* 手机抽屉遮罩加深，弱化背后残卡 */
    opacity: 0; pointer-events: none; transition: opacity .2s ease;
  }
  .scrim-side.show { opacity: 1; pointer-events: auto; }
  .detailcol { z-index: 78; }
  .scrim-detail { z-index: 77; }
}
</style>

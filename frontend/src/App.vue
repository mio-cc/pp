<template>
  <div class="app" :class="{ 'side-hidden': sideCollapsed }">
    <!-- 顶栏 -->
    <header class="topbar">
      <button class="toggle-side" title="折叠/展开侧栏 (Ctrl+\)" @click="sideCollapsed = !sideCollapsed">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <rect x="3" y="4" width="18" height="16" rx="2" />
          <line x1="9" y1="4" x2="9" y2="20" />
        </svg>
      </button>
      <span class="brand">视觉术语<span class="dot">·</span><span class="sub">提示词构建器</span></span>
      <a-tag v-if="kb.state.mode" size="small" :color="kb.state.mode === 'api' ? 'arcoblue' : 'gray'" class="mode-tag">
        {{ kb.state.mode === 'api' ? 'API 模式' : '离线模式' }}
      </a-tag>

      <div class="search-wrap">
        <a-input-search
          v-model="query"
          placeholder="搜索术语…（Ctrl+K）"
          allow-clear
          @input="onSearchInput"
          @clear="clearSearch"
        />
      </div>
    </header>

    <div class="body">
      <!-- 侧边栏：Vue 响应式控制，收缩 100% 可靠 -->
      <aside class="side">
        <div class="side-inner">
          <div class="side-hd">
            <span>体系 / 分类</span>
            <span class="cnt">{{ kb.state.index ? kb.state.index.total_terms : 0 }} 词</span>
          </div>
          <SideTree
            v-if="kb.state.index"
            ref="treeRef"
            :volumes="kb.state.index.volumes"
            @select="onSelectCategory"
          />
        </div>
      </aside>

      <!-- 主内容 -->
      <main class="main">
        <!-- 加载/错误态 -->
        <div v-if="!kb.state.ready && !kb.state.error" class="center-state">
          <a-spin dot :size="28" />
          <div class="ltxt">加载知识库…</div>
        </div>
        <div v-else-if="kb.state.error" class="center-state error">
          <div class="big">!</div>
          <pre>{{ kb.state.error }}</pre>
        </div>

        <template v-else>
          <!-- 面包屑 -->
          <div class="crumb">
            <template v-if="searching">
              <span class="seg cur">搜索 “{{ query }}”</span>
              <span class="hint" style="margin-left:8px">{{ terms.length }} 条结果</span>
            </template>
            <template v-else-if="current">
              <span class="seg" @click="scrollTop">{{ current.volumeTitle }}</span>
              <span class="arr">›</span>
              <span class="seg cur">{{ current.categoryName }}</span>
              <span class="hint" style="margin-left:8px">{{ terms.length }} 个术语</span>
            </template>
            <span v-else class="hint">在左侧展开 体系 › 分类，或直接搜索术语</span>
          </div>

          <!-- 术语网格 -->
          <div v-if="!current && !searching" class="welcome">
            <div class="welcome-card">
              <div class="big">⌘</div>
              <h3>选择一个体系开始构建提示词</h3>
              <p>共 {{ kb.state.index.volumes.length }} 卷 · {{ kb.state.index.total_terms }} 个术语</p>
              <div class="vol-quick">
                <button
                  v-for="v in kb.state.index.volumes"
                  :key="v.code"
                  class="vq"
                  @click="quickOpenVolume(v)"
                >
                  {{ v.title }}<span>{{ v.current_terms }}</span>
                </button>
              </div>
            </div>
          </div>
          <TermGrid
            v-else
            :terms="terms"
            :loading="gridLoading"
            :empty-text="searching ? `没有匹配「${query}」的术语` : '该分类暂无术语'"
            @detail="openDetail"
            @add="onAdd"
          />
        </template>
      </main>
    </div>

    <!-- 详情抽屉 -->
    <DetailDrawer :visible="detailVisible" :term="detailTerm" @close="detailVisible = false" />

    <!-- 底部提示词篮 -->
    <PromptDock />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import SideTree from './components/SideTree.vue'
import TermGrid from './components/TermGrid.vue'
import DetailDrawer from './components/DetailDrawer.vue'
import PromptDock from './components/PromptDock.vue'
import { useKB } from './composables/useKB'

const kb = useKB()
const sideCollapsed = ref(false)
const treeRef = ref(null)

const terms = ref([])
const current = ref(null) // { volumeCode, volumeTitle, categoryName }
const gridLoading = ref(false)

const query = ref('')
const searching = ref(false)
let searchTimer = null

const detailVisible = ref(false)
const detailTerm = ref(null)

onMounted(async () => {
  await kb.init()
  if (kb.state.ready) {
    // 默认展开第一卷
    setTimeout(() => treeRef.value && treeRef.value.expandFirst(), 100)
  }
  window.addEventListener('keydown', onKey)
})
onUnmounted(() => window.removeEventListener('keydown', onKey))

function onKey(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    document.querySelector('.search-wrap input')?.focus()
  }
  if ((e.metaKey || e.ctrlKey) && e.key === '\\') {
    e.preventDefault()
    sideCollapsed.value = !sideCollapsed.value
  }
  if (e.key === 'Escape') detailVisible.value = false
}

async function onSelectCategory({ volume, category }) {
  searching.value = false
  query.value = ''
  current.value = {
    volumeCode: volume.code,
    volumeTitle: volume.title,
    categoryName: category.name
  }
  gridLoading.value = true
  terms.value = []
  try {
    terms.value = await kb.loadCategoryTerms(volume.code, category.name)
  } finally {
    gridLoading.value = false
  }
}

async function quickOpenVolume(v) {
  // 打开第一个有术语的分类
  const cat = v.categories.find((c) => c.term_count > 0) || v.categories[0]
  if (cat) {
    treeRef.value && treeRef.value.expandFirst // no-op safeguard
    await onSelectCategory({ volume: v, category: cat })
  }
}

function onSearchInput() {
  clearTimeout(searchTimer)
  const q = query.value.trim()
  if (!q) {
    clearSearch()
    return
  }
  searchTimer = setTimeout(async () => {
    searching.value = true
    current.value = null
    gridLoading.value = true
    try {
      terms.value = await kb.search(q, 80)
    } finally {
      gridLoading.value = false
    }
  }, 200)
}
function clearSearch() {
  searching.value = false
  query.value = ''
  if (!current.value) terms.value = []
}

function openDetail(t) {
  detailTerm.value = t
  detailVisible.value = true
}
function onAdd() {
  /* Message 已在 TermGrid/Cart 处理，这里留扩展点 */
}
function scrollTop() {
  document.querySelector('.main')?.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 顶栏 */
.topbar {
  height: 48px;
  flex: 0 0 48px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
  background: var(--panel);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--line);
  position: relative;
  z-index: 30;
}
.toggle-side {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ink2);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.toggle-side:hover {
  background: var(--hov);
  transform: scale(1.05);
}
.toggle-side:active {
  transform: scale(0.95);
}
.toggle-side svg {
  width: 17px;
  height: 17px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.app.side-hidden .toggle-side svg {
  transform: scaleX(-1);
}
.brand {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.02em;
}
.brand .dot {
  color: var(--mut);
  margin: 0 6px;
}
.brand .sub {
  color: var(--mut);
  font-weight: 400;
  font-size: 12px;
}
.mode-tag {
  margin-left: 2px;
}
.search-wrap {
  margin-left: auto;
  width: 300px;
  max-width: 40vw;
}

/* 主体 */
.body {
  flex: 1;
  display: flex;
  min-height: 0;
  position: relative;
}

/* 侧边栏 —— width 过渡，响应式状态控制 */
.side {
  width: var(--side-w);
  flex: 0 0 var(--side-w);
  background: var(--panel);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-right: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.32s cubic-bezier(0.4, 0, 0.2, 1), flex-basis 0.32s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.28s ease, border-color 0.28s ease;
}
.app.side-hidden .side {
  width: 0;
  flex-basis: 0;
  opacity: 0;
  border-color: transparent;
  pointer-events: none;
}
.side-inner {
  width: var(--side-w);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  transition: transform 0.32s cubic-bezier(0.4, 0, 0.2, 1);
}
.app.side-hidden .side-inner {
  transform: translateX(-20px);
}
.side-hd {
  padding: 12px 14px 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: var(--mut);
  text-transform: uppercase;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.side-hd .cnt {
  font-weight: 400;
  color: var(--faint);
}

/* 主内容 */
.main {
  flex: 1;
  overflow-y: auto;
  padding: 18px 22px 120px;
  min-width: 0;
  scroll-behavior: smooth;
}
.crumb {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 18px;
  font-size: 12px;
  min-height: 22px;
}
.crumb .seg {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid var(--line);
  color: var(--ink2);
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}
.crumb .seg:hover {
  background: #fff;
  color: var(--ink);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.crumb .seg.cur {
  background: var(--sel);
  color: #fff;
  border-color: var(--sel);
}
.crumb .arr {
  color: var(--faint);
}
.crumb .hint {
  color: var(--mut);
}

/* 加载/错误态 */
.center-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 90px 20px;
  gap: 14px;
  color: var(--mut);
}
.center-state .ltxt {
  font-size: 13px;
}
.center-state.error .big {
  font-size: 34px;
  color: #e06c5e;
}
.center-state pre {
  font-family: var(--font);
  font-size: 13px;
  line-height: 1.8;
  text-align: center;
  white-space: pre-wrap;
}

/* 欢迎页 */
.welcome {
  display: flex;
  justify-content: center;
  padding-top: 40px;
}
.welcome-card {
  text-align: center;
  max-width: 640px;
}
.welcome-card .big {
  font-size: 40px;
  opacity: 0.4;
  margin-bottom: 10px;
}
.welcome-card h3 {
  font-size: 17px;
  margin-bottom: 6px;
}
.welcome-card p {
  color: var(--mut);
  font-size: 13px;
  margin-bottom: 22px;
}
.vol-quick {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
}
.vq {
  background: var(--panel-solid);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 11px 13px;
  cursor: pointer;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--ink2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}
.vq span {
  font-size: 10.5px;
  color: var(--faint);
  background: rgba(0, 0, 0, 0.04);
  padding: 1px 7px;
  border-radius: 9px;
}
.vq:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
  border-color: rgba(0, 0, 0, 0.14);
  color: var(--ink);
}

@media (max-width: 880px) {
  .main {
    padding: 16px 16px 110px;
  }
  .search-wrap {
    width: 200px;
  }
  .side {
    position: absolute;
    height: 100%;
    z-index: 38;
    box-shadow: var(--shadow-lg);
  }
}
</style>

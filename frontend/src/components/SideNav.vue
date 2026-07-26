<template>
  <aside class="side">
    <div class="brand">
      <span class="logo" aria-hidden="true">術</span>
      <span class="bt">
        <span class="n">AI 视觉术语库</span><br>
        <span class="s">提示词构建器<template v-if="mode"> · {{ mode === 'api' ? 'API 模式' : '离线模式' }}</template></span>
      </span>
      <button class="fold" title="折叠/展开侧栏 (Ctrl+\)" @click="$emit('toggle-side')"><Icon name="panelLeft" /></button>
    </div>

    <div class="searchbox">
      <Icon name="search" class="sic" />
      <input
        ref="input"
        :value="q"
        type="search"
        placeholder="搜索全库术语…（Ctrl+K）"
        autocomplete="off"
        @input="$emit('search', $event.target.value)"
      >
      <button class="rand" title="随机术语" :disabled="randomLoading" @click="$emit('random')"><Icon name="shuffle" /></button>
    </div>

    <div class="progress">
      <div class="pline"><span>收录进度</span><b>{{ totalTerms.toLocaleString() }} / {{ targetTotal.toLocaleString() }}</b></div>
      <div class="pbar"><i :style="{ width: progressPct + '%' }"></i></div>
    </div>

    <div class="treezone">
      <div ref="treewrap" class="treewrap" @scroll="syncRibbon">
        <div class="hd">
          <span>体系 / 分类</span>
          <button class="root" @click="$emit('go-root')">总览</button>
        </div>
        <button
          v-for="r in rows"
          :key="r.key"
          class="tnode"
          :class="[r.depth === 0 ? 'vol' : '', { on: r.key === activeKey }]"
          :style="{ paddingLeft: (9 + r.depth * 16) + 'px' }"
          @click="$emit('row-click', r)"
        >
          <span class="caret" :class="{ open: r.open }" @click.stop="$emit('caret', r)">
            <Icon :name="r.hasKids ? 'chevR' : 'dot'" />
          </span>
          <span class="tname">{{ r.title }}</span>
          <span v-if="r.loading" class="tcount">…</span>
          <span v-else class="tcount" :class="{ zero: !r.count }">{{ r.count }}</span>
        </button>
      </div>
      <!-- 书签滑绳：树超出可视高度时出现，按住拖动即可快速定位 -->
      <div
        v-show="ribbonVisible"
        class="ribbon"
        :class="{ dragging }"
        :style="{ top: ribbonTop + 'px' }"
        title="按住拖动，快速滚动分类树"
        @pointerdown.prevent="onRibbonDown"
      ></div>
    </div>

    <!-- 底部栏：与右侧提示词篮（无预览态）等高，放快捷键提示与版本 -->
    <div class="sfoot">
      <span class="kbd">Ctrl K</span><i>搜索</i>
      <span class="kbd">Ctrl \</span><i>折叠</i>
      <span class="ver">V1.0</span>
    </div>
  </aside>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import Icon from './Icon.vue'

const props = defineProps({
  rows: { type: Array, default: () => [] },
  activeKey: { type: String, default: '' },
  q: { type: String, default: '' },
  mode: { type: String, default: '' },
  totalTerms: { type: Number, default: 0 },
  targetTotal: { type: Number, default: 0 },
  progressPct: { type: Number, default: 0 },
  randomLoading: { type: Boolean, default: false },
})
defineEmits(['row-click', 'caret', 'search', 'random', 'go-root', 'toggle-side'])

const input = ref(null)
function focusSearch() { input.value && input.value.focus() }
defineExpose({ focusSearch })

/* ---------- 书签滑绳：自绘滚动把手（全局滚动条已隐藏） ---------- */
const treewrap = ref(null)
const ribbonVisible = ref(false)
const ribbonTop = ref(6)
const dragging = ref(false)
const RIBBON_H = 46
const PAD = 6

function syncRibbon() {
  const el = treewrap.value
  if (!el) return
  const max = el.scrollHeight - el.clientHeight
  ribbonVisible.value = max > 12
  if (!ribbonVisible.value) return
  const track = el.clientHeight - RIBBON_H - PAD * 2
  ribbonTop.value = PAD + (max > 0 ? (el.scrollTop / max) * track : 0)
}

let dragOffY = 0
function onRibbonDown(e) {
  const el = treewrap.value
  if (!el) return
  dragging.value = true
  dragOffY = e.clientY - (el.getBoundingClientRect().top + ribbonTop.value)
  window.addEventListener('pointermove', onRibbonMove)
  window.addEventListener('pointerup', onRibbonUp)
}
function onRibbonMove(e) {
  const el = treewrap.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  const track = el.clientHeight - RIBBON_H - PAD * 2
  if (track <= 0) return
  const y = Math.min(Math.max(e.clientY - rect.top - dragOffY, PAD), PAD + track)
  const max = el.scrollHeight - el.clientHeight
  ribbonTop.value = y  // 把手直接跟手，不等 scroll 事件回写
  el.scrollTop = ((y - PAD) / track) * max
}
function onRibbonUp() {
  dragging.value = false
  window.removeEventListener('pointermove', onRibbonMove)
  window.removeEventListener('pointerup', onRibbonUp)
}

watch(() => props.rows.length, () => nextTick(syncRibbon))
onMounted(() => {
  nextTick(syncRibbon)
  window.addEventListener('resize', syncRibbon)
})
onUnmounted(() => {
  window.removeEventListener('resize', syncRibbon)
  onRibbonUp()
})
</script>

<style scoped>
.side {
  width: 284px; flex: 0 0 284px; display: flex; flex-direction: column; min-height: 0;
  background: var(--bg-side);
  transition: width .25s ease, flex-basis .25s ease, opacity .2s ease;
  overflow: hidden;
}
.brand { display: flex; align-items: center; gap: 11px; padding: 18px 14px 14px 18px; }
/* 墨印：黑底衬线「術」字 */
.logo {
  width: 34px; height: 34px; border-radius: 8px; background: var(--ink); color: #fff;
  display: inline-flex; align-items: center; justify-content: center; flex: 0 0 34px;
  font-family: var(--serif); font-size: 18px; font-weight: 600; user-select: none;
}
.bt { line-height: 1.3; flex: 1; white-space: nowrap; }
.bt .n { font-weight: 700; font-size: 14px; }
.bt .s { font-size: 11px; color: var(--ink-3); }
.fold {
  width: 28px; height: 28px; border-radius: var(--r-sm); color: var(--ink-3);
  display: inline-flex; align-items: center; justify-content: center;
  transition: background-color .15s, color .15s;
}
.fold:hover { background: var(--surface-2); color: var(--ink-2); }
.searchbox { padding: 0 14px 12px; position: relative; display: flex; gap: 8px; }
.searchbox input {
  flex: 1; height: 34px; padding: 0 12px 0 34px; min-width: 0;
  border: 1px solid var(--line-2); border-radius: var(--r);
  background: var(--surface); color: var(--ink);
  font: 12.5px var(--sans);
  transition: border-color .15s, box-shadow .15s;
}
.searchbox input::placeholder { color: var(--ink-3); }
.searchbox input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-tint); }
.searchbox .sic { position: absolute; left: 26px; top: 10px; color: var(--ink-3); }
.searchbox .sic :deep(svg.ic) { width: 14px; height: 14px; }
.rand {
  width: 34px; height: 34px; flex: 0 0 34px; border: 1px solid var(--line-2); border-radius: var(--r);
  background: var(--surface); color: var(--ink-2);
  display: inline-flex; align-items: center; justify-content: center;
  transition: border-color .15s, color .15s;
}
.rand:hover { border-color: var(--ink); color: var(--ink); }
.rand:disabled { opacity: .5; cursor: progress; }
.progress { padding: 2px 18px 14px; }
.pline { display: flex; justify-content: space-between; font-size: 10.5px; color: var(--ink-3); font-family: var(--mono); margin-bottom: 5px; }
.pline b { color: var(--ink-2); font-weight: 550; }
.pbar { height: 4px; border-radius: 999px; background: var(--line); overflow: hidden; }
.pbar i { display: block; height: 100%; border-radius: 999px; background: var(--accent); }
.treezone { flex: 1; min-height: 0; position: relative; display: flex; }
.treewrap { flex: 1; min-width: 0; overflow-y: auto; padding: 10px 18px 24px 10px; }
/* 底部栏：52px 与提示词篮 row1 同高，边线同款 */
.sfoot {
  /* 47 = 46 内容 + 1 上边框（border-box），与提示词篮 row1+border 总高严格对齐 */
  flex: 0 0 auto; height: 47px; border-top: 1px solid var(--line);
  display: flex; align-items: center; gap: 6px; padding: 0 16px;
  font-size: 11px; color: var(--ink-3);
}
.sfoot i { font-style: normal; margin-right: 8px; }
.kbd {
  font-family: var(--mono); font-size: 10px; color: var(--ink-2);
  border: 1px solid var(--line-2); border-radius: 4px;
  background: var(--surface); padding: 1px 6px;
}
.ver { margin-left: auto; font-family: var(--mono); }
@media (max-width: 620px) { .sfoot { display: none; } }
/* 书签滑绳：墨色缎带造型（底部燕尾口），拖动映射滚动位置 */
.ribbon {
  position: absolute; right: 3px; width: 12px; height: 46px;
  background: var(--ink); opacity: .16;
  border-radius: 3px 3px 0 0;
  clip-path: polygon(0 0, 100% 0, 100% 100%, 50% calc(100% - 7px), 0 100%);
  cursor: grab; touch-action: none;
  transition: opacity .15s;
}
.ribbon:hover { opacity: .38; }
.ribbon.dragging { opacity: .55; cursor: grabbing; transition: none; }
.treewrap .hd {
  padding: 4px 10px 8px; font-size: 10.5px; font-weight: 650; color: var(--ink-3);
  letter-spacing: .1em; display: flex; justify-content: space-between; align-items: baseline;
}
.treewrap .hd .root { color: var(--ink-2); font-weight: 550; font-size: 11px; }
.treewrap .hd .root:hover { color: var(--ink); text-decoration: underline; text-underline-offset: 3px; }
.tnode {
  display: flex; align-items: center; gap: 6px; width: 100%;
  padding: 6px 9px; border-radius: var(--r-sm); text-align: left; margin: 1px 0;
  color: var(--ink-2);
  transition: background-color .15s, color .15s;
}
.tnode:hover { background: rgba(255, 255, 255, .7); }
.tnode.on { background: var(--surface); box-shadow: var(--sh-sm); color: var(--accent-deep); }
.tnode.on .tname { font-weight: 650; }
.caret { width: 14px; flex: 0 0 14px; color: var(--ink-3); display: flex; align-items: center; justify-content: center; }
.caret :deep(svg.ic) { width: 12px; height: 12px; transition: transform .18s ease; }
.caret.open :deep(svg.ic) { transform: rotate(90deg); }
.tnode.on .caret { color: var(--accent); }
.tname { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tnode.vol .tname { font-weight: 600; color: var(--ink); }
.tnode.on.vol .tname { color: var(--accent-deep); }
.tcount { font-family: var(--mono); font-size: 10.5px; color: var(--ink-3); }
.tcount.zero { color: var(--line-2); }

/* 中屏 621–880：侧栏 240px 常驻，收紧内边距 */
@media (min-width: 621px) and (max-width: 880px) {
  .brand { padding: 14px 10px 10px 14px; }
  .searchbox { padding: 0 10px 10px; }
  .searchbox .sic { left: 22px; }
  .progress { padding: 2px 14px 12px; }
  .sfoot { padding: 0 12px; }
}
/* 手机抽屉模式：桌面折叠钮无意义，隐藏；触控目标加高 */
@media (max-width: 620px) {
  .fold { display: none; }
  .tnode { padding-top: 8px; padding-bottom: 8px; }
}
</style>

<template>
  <footer class="bar">
    <div class="row1">
      <span class="blbl"><Icon name="grid" />提示词篮<span class="bnum">{{ cart.count.value }}</span></span>
      <div class="chips">
        <span v-if="!cart.items.length" class="ph">在列表或详情中「加入」术语；按 主体→风格→光影→构图→参数 槽位自动排序</span>
        <span
          v-for="t in sortedItems"
          :key="t.term_uid"
          class="chip"
          :class="{ conflict: conflictUids.has(t.term_uid) }"
          :title="(t.volume_code || '') + ' · ' + (t.category || '')"
        >
          <i class="slot">{{ slotOf(t.volume_code).label }}</i>
          {{ t.zh_term }}
          <button aria-label="移除" @click="cart.remove(t.term_uid)"><Icon name="x" /></button>
        </span>
      </div>
      <div class="langs" title="复制语言">
        <button v-for="l in LANGS" :key="l.k" :class="{ on: lang === l.k }" @click="lang = l.k">{{ l.label }}</button>
      </div>
      <div class="langs" title="平台方言：通用纯词 / SD 括号权重 / MJ 双冒号权重">
        <button v-for="d in DIALECTS" :key="d.k" :class="{ on: dialect === d.k }" @click="dialect = d.k">{{ d.label }}</button>
      </div>
      <button class="share" title="复制分享链接（打开即还原整篮）" @click="shareBasket">
        <Icon :name="shared === 'ok' ? 'check' : shared === 'fail' ? 'x' : 'tag'" />
        <span class="sh-t">{{ shared === 'ok' ? '已复制链接' : shared === 'fail' ? '复制失败' : '分享' }}</span>
      </button>
      <button class="copyall" @click="copyAll">
        <Icon :name="copied === 'ok' ? 'check' : copied === 'fail' ? 'x' : 'copy'" />
        {{ copied === 'ok' ? '已复制' : copied === 'fail' ? '复制失败' : '复制提示词' }}
      </button>
    </div>
    <div v-if="cart.items.length" class="preview">
      <span v-if="conflictUids.size" class="cw">同叶互斥 {{ conflictUids.size }} 项（已标红，仍可复制） </span>{{ promptText }}
    </div>
  </footer>
</template>

<script setup>
import { computed, ref } from 'vue'
import Icon from './Icon.vue'
import { useCart } from '../composables/useCart'
import { copyText } from '../utils/clipboard'

const cart = useCart()
const LANGS = [{ k: 'en', label: 'EN' }, { k: 'cn', label: '中' }, { k: 'both', label: '双语' }]
const DIALECTS = [{ k: 'generic', label: '通用' }, { k: 'sd', label: 'SD' }, { k: 'mj', label: 'MJ' }]
const lang = ref('en')
const dialect = ref('generic')
const copied = ref('')   // '' | 'ok' | 'fail'
const shared = ref('')   // '' | 'ok' | 'fail'

/* 槽位映射：卷 → 提示词结构位（主体→风格→光影→构图→参数），未映射的归「其他」。
   与后端无耦合，纯前端组词次序约定。 */
const SLOTS = [
  { key: 'subject', label: '主体', vols: ['V04', 'V10', 'V11', 'V30', 'V31', 'V36', 'V37', 'V38'] },
  { key: 'style', label: '风格', vols: ['V03', 'V07', 'V15', 'V24', 'V25', 'V26', 'V27', 'V29', 'V32', 'V33', 'V35'] },
  { key: 'light', label: '光影', vols: ['V02', 'V06', 'V13', 'V28', 'V34'] },
  { key: 'comp', label: '构图', vols: ['V01', 'V05', 'V09', 'V12', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23'] },
  { key: 'param', label: '参数', vols: ['V08', 'V14'] },
  { key: 'other', label: '其他', vols: [] },
]
const slotIndex = {}
SLOTS.forEach((s, i) => s.vols.forEach((v) => (slotIndex[v] = i)))
function slotOf(volumeCode) {
  const i = slotIndex[volumeCode]
  return i === undefined ? SLOTS[SLOTS.length - 1] : SLOTS[i]
}
const sortedItems = computed(() => {
  const rank = (t) => {
    const i = slotIndex[t.volume_code]
    return i === undefined ? SLOTS.length - 1 : i
  }
  return [...cart.items].sort((a, b) => rank(a) - rank(b))
})

const conflictUids = computed(() => {
  const byPath = {}
  cart.items.forEach((t) => { (byPath[t.category] = byPath[t.category] || []).push(t.term_uid) })
  const s = new Set()
  Object.values(byPath).forEach((a) => { if (a.length > 1) a.forEach((u) => s.add(u)) })
  return s
})

function decorate(text) {
  if (dialect.value === 'sd') return '(' + text + ':1.1)'
  if (dialect.value === 'mj') return text + '::1.1'
  return text
}
const promptText = computed(() =>
  sortedItems.value
    .map((t) => {
      const en = t.en_term || t.zh_term
      const base = lang.value === 'cn' ? t.zh_term : lang.value === 'both' ? en + '（' + t.zh_term + '）' : en
      return decorate(base)
    })
    .filter(Boolean)
    .join(', ')
)

let copyTimer = null
async function copyAll() {
  if (!cart.items.length) return
  const ok = await copyText(promptText.value)
  copied.value = ok ? 'ok' : 'fail'
  clearTimeout(copyTimer)
  copyTimer = setTimeout(() => (copied.value = ''), 1300)
}
let shareTimer = null
async function shareBasket() {
  if (!cart.items.length) return
  const uids = sortedItems.value.map((t) => t.term_uid).join(',')
  const url = location.origin + location.pathname + '#/basket/' + uids
  const ok = await copyText(url)
  shared.value = ok ? 'ok' : 'fail'
  clearTimeout(shareTimer)
  shareTimer = setTimeout(() => (shared.value = ''), 1500)
}
</script>

<style scoped>
.bar { flex: 0 0 auto; background: var(--surface); border-top: 1px solid var(--line); box-shadow: 0 -4px 18px -12px rgba(20, 20, 22, .18); }
.row1 { display: flex; align-items: center; gap: 10px; padding: 0 20px; min-height: 46px; }
.blbl { font-weight: 650; white-space: nowrap; font-size: 13px; display: flex; align-items: center; gap: 8px; }
.blbl :deep(svg.ic) { color: var(--ink-3); }
.bnum {
  font-family: var(--mono); font-size: 11px; color: var(--ink);
  background: var(--accent-tint); border-radius: 999px; min-width: 22px; height: 20px;
  display: inline-flex; align-items: center; justify-content: center; padding: 0 7px;
}
.chips { flex: 1; display: flex; gap: 7px; overflow-x: auto; min-height: 30px; align-items: center; }
.chip {
  background: var(--surface-2); border: 1px solid transparent; border-radius: 999px;
  padding: 3px 6px 3px 6px; white-space: nowrap;
  display: inline-flex; align-items: center; gap: 5px; font-size: 12px; color: var(--ink-2);
}
.chip .slot {
  font-style: normal; font-size: 10px; color: var(--ink-3);
  background: var(--surface); border-radius: 999px; padding: 1px 7px;
}
.chip.conflict { border-color: var(--danger); color: var(--danger); background: #f8edea; }
.chip.conflict .slot { color: var(--danger); }
.chip button { display: flex; color: var(--ink-3); padding: 3px; border-radius: 999px; transition: background-color .15s, color .15s; }
.chip button :deep(svg.ic) { width: 11px; height: 11px; }
.chip button:hover { color: var(--ink); background: var(--line); }
.chip.conflict button { color: var(--danger); }
.ph { color: var(--ink-3); font-size: 12px; }
.langs { display: flex; background: var(--surface-2); border-radius: var(--r); padding: 2px; }
.langs button { padding: 4px 10px; font-size: 11.5px; font-weight: 550; color: var(--ink-3); border-radius: var(--r-sm); transition: background-color .15s, color .15s; }
.langs button.on { background: var(--surface); color: var(--ink); box-shadow: var(--sh-sm); }
.share {
  display: inline-flex; align-items: center; gap: 6px;
  border: 1px solid var(--line-2); border-radius: var(--r); color: var(--ink-2);
  padding: 6px 12px; font-weight: 550; font-size: 12px; white-space: nowrap;
  transition: border-color .15s, color .15s;
}
.share :deep(svg.ic) { width: 12px; height: 12px; }
.share:hover { border-color: var(--ink); color: var(--ink); }
.copyall {
  display: inline-flex; align-items: center; gap: 7px;
  background: var(--accent); color: #fff; border-radius: var(--r);
  padding: 7px 18px; font-weight: 600; font-size: 12.5px; white-space: nowrap;
  transition: background-color .15s;
}
.copyall :deep(svg.ic) { width: 13px; height: 13px; }
.copyall:hover { background: var(--accent-deep); }
.preview {
  border-top: 1px solid var(--line); padding: 7px 20px; background: var(--surface-3);
  font-family: var(--mono); font-size: 11px; color: var(--ink-2);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.cw { color: var(--danger); font-weight: 600; }

/* 窄屏：词条行独占一行在上，控件行在下换行排布 */
@media (max-width: 880px) {
  .row1 { flex-wrap: wrap; row-gap: 8px; padding: 8px 12px; min-height: 0; }
  .chips { order: -1; flex-basis: 100%; }
  .blbl { font-size: 12.5px; }
  .langs button { padding: 4px 8px; font-size: 11px; }
  .share { padding: 6px 10px; }
  .share .sh-t { display: none; }
  .copyall { padding: 6px 14px; margin-left: auto; }
  .preview { padding: 6px 12px; }
}
@media (max-width: 400px) {
  .langs button { padding: 3px 6px; }
  .blbl :deep(svg.ic) { display: none; }
}
</style>

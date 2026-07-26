<template>
  <div v-if="!term" class="dcard">
    <div class="empty">
      <span class="eicon"><Icon name="tag" /></span>
      从列表选择一个术语
    </div>
  </div>
  <div v-else class="dcard">
    <button class="dclose" aria-label="关闭详情" @click="$emit('close')"><Icon name="x" /></button>
    <div class="path">
      <template v-for="(seg, i) in pathSegs" :key="i">{{ seg }}<b v-if="i < pathSegs.length - 1"> / </b></template>
    </div>
    <div class="body">
      <div class="headword">
        {{ term.zh_term }}
        <button class="copy1" @click="copy(term.zh_term, 'zh')">{{ copyLabel('zh') }}</button>
      </div>
      <div class="enline">
        {{ term.en_term || term.term_uid }}
        <button v-if="term.en_term" class="copy1" @click="copy(term.en_term, 'en')">{{ copyLabel('en') }}</button>
      </div>
      <div class="namehint">中文名即中文提示词 · 英文名即英文提示词</div>
      <div class="metaline">
        <span>{{ term.term_uid }}</span>
        <span class="st" :class="term.status"><i></i>{{ statusZh(term.status) }}</span>
        <span v-if="term.version">{{ term.version }}</span>
      </div>

      <div v-if="term.definition_long" class="sect"><div class="lbl">释义</div><div class="txt">{{ term.definition_long }}</div></div>
      <div v-if="term.visual_effect" class="sect"><div class="lbl">视觉表现</div><div class="txt">{{ term.visual_effect }}</div></div>
      <div v-if="term.prompt_usage" class="sect"><div class="lbl">提示词用法</div><div class="txt">{{ term.prompt_usage }}</div></div>

      <div v-if="list(term.use_cases).length" class="sect">
        <div class="lbl">适用场景</div>
        <div class="plainlist"><span v-for="u in list(term.use_cases)" :key="u">{{ u }}</span></div>
      </div>
      <div v-if="list(term.tags).length" class="sect">
        <div class="lbl">标签</div>
        <div class="plainlist"><span v-for="g in list(term.tags)" :key="g">{{ g }}</span></div>
      </div>
      <div v-if="list(term.related_terms).length" class="sect">
        <div class="lbl">相关术语</div>
        <div class="plainlist"><span v-for="r in list(term.related_terms)" :key="r" class="reflink" @click="$emit('jump', r)">{{ r }}</span></div>
      </div>
      <div v-if="list(term.confused_with).length" class="sect">
        <div class="lbl">易混淆</div>
        <div class="plainlist"><span v-for="r in list(term.confused_with)" :key="r" class="reflink" @click="$emit('jump', r)">{{ r }}</span></div>
      </div>

      <button class="d-add" :class="{ in: cart.has(term.term_uid) }" @click="$emit('toggle', term)">
        <Icon :name="cart.has(term.term_uid) ? 'check' : 'plus'" />
        {{ cart.has(term.term_uid) ? '已在提示词栏 · 点击移除' : '加入提示词栏' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import Icon from './Icon.vue'
import { useCart } from '../composables/useCart'
import { copyText } from '../utils/clipboard'

const props = defineProps({ term: { type: Object, default: null } })
defineEmits(['toggle', 'jump', 'close'])

const cart = useCart()
const copied = ref('')
const STATUS_ZH = { published: '已发布', review: '审核中', draft: '草稿', deprecated: '已弃用' }
function statusZh(s) { return STATUS_ZH[s] || s || '—' }
function list(v) {
  if (!v) return []
  return Array.isArray(v) ? v : String(v).split(';').map((x) => x.trim()).filter(Boolean)
}
const pathSegs = computed(() => {
  if (!props.term) return []
  const segs = []
  if (props.term.volume_title) segs.push(props.term.volume_code + ' ' + props.term.volume_title)
  segs.push(...(props.term.category || '未分类').split(' / '))
  segs.push(props.term.zh_term)
  return segs
})
let copyTimer = null
async function copy(text, key) {
  const ok = await copyText(text)
  copied.value = key + (ok ? ':ok' : ':fail')
  clearTimeout(copyTimer)
  copyTimer = setTimeout(() => (copied.value = ''), 1000)
}
function copyLabel(key) {
  if (copied.value === key + ':ok') return '已复制'
  if (copied.value === key + ':fail') return '失败'
  return '复制'
}
</script>

<style scoped>
.dcard { background: none; position: relative; }
.dclose { display: none; }
.path {
  padding: 0 0 12px; border-bottom: 1px solid var(--line);
  font-family: var(--mono); font-size: 10.5px; color: var(--ink-3); line-height: 1.9;
  word-break: break-all;
}
.path b { color: var(--ink-2); font-weight: 550; padding: 0 2px; }
@media (max-width: 1100px) {
  /* sticky：详情抽屉内滚动时关闭钮始终钉在顶部（滚动容器是外层 .detailcol） */
  .dclose {
    display: flex; position: sticky; top: 0; z-index: 2;
    margin-left: auto; margin-bottom: -34px;
    width: 34px; height: 34px; align-items: center; justify-content: center;
    border: 1px solid var(--line-2); border-radius: 999px;
    background: var(--surface); color: var(--ink-2);
  }
  .dclose:hover { border-color: var(--ink); color: var(--ink); }
  .path { padding-right: 40px; }
}
.body { padding: 16px 0 26px; }
/* 词条起始的朱砂短划：词典条目的「印」记 */
.body::before {
  content: ""; display: block;
  width: 26px; height: 3px; border-radius: 1px;
  background: var(--seal);
  margin-bottom: 12px;
}
.headword {
  font-family: var(--serif); font-size: 24px; font-weight: 700; line-height: 1.3;
  display: flex; align-items: baseline; gap: 10px;
}
.enline {
  display: flex; align-items: center; gap: 8px; margin: 6px 0 2px;
  font-family: var(--mono); font-size: 13px; color: var(--ink-2); word-break: break-all;
}
.namehint { font-size: 10.5px; color: var(--ink-3); margin: 4px 0 6px; }
.metaline { font-size: 11px; color: var(--ink-3); font-family: var(--mono); margin: 6px 0 12px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.st { display: inline-flex; align-items: center; gap: 6px; color: var(--ink-2); }
.st i { width: 6px; height: 6px; border-radius: 50%; background: var(--gray); }
.st.published i { background: var(--ok); }
.st.review i { background: var(--review); }
.copy1 {
  display: inline-flex; align-items: center; gap: 5px; flex: 0 0 auto;
  font-size: 10.5px; padding: 1px 8px;
  border: 1px solid var(--line-2); color: var(--ink-3); background: var(--surface);
  border-radius: 3px; font-family: var(--sans); font-weight: 400;
  transition: color .15s, border-color .15s;
}
.copy1:hover { color: var(--ink); border-color: var(--ink); }
.sect { margin-top: 15px; }
.lbl { font-size: 10.5px; font-weight: 700; color: var(--ink-3); letter-spacing: .08em; margin-bottom: 4px; }
.txt { font-size: 13px; color: var(--ink-2); line-height: 1.7; }
.plainlist { display: flex; flex-wrap: wrap; gap: 0 4px; font-size: 12.5px; color: var(--ink-2); }
.plainlist span + span::before { content: "、"; color: var(--ink-3); }
.reflink { color: var(--ink); cursor: pointer; text-decoration: underline; text-underline-offset: 3px; text-decoration-color: var(--line-2); transition: text-decoration-color .15s; }
.reflink:hover { text-decoration-color: var(--ink); }
.d-add {
  margin-top: 22px; width: 100%; padding: 9px 0;
  border: 1px solid var(--ink); border-radius: var(--r-sm);
  color: var(--ink); font-weight: 600; font-size: 13px;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  transition: background-color .15s, color .15s, border-color .15s;
}
.d-add:hover { background: var(--ink); color: #fff; }
.d-add.in { border-color: var(--line-2); color: var(--ink-3); }
.d-add.in:hover { background: var(--surface-2); color: var(--ink-2); }
.empty { padding: 60px 24px; color: var(--ink-3); text-align: center; font-size: 13px; line-height: 2.1; }
.eicon {
  width: 42px; height: 42px; margin: 0 auto 12px; border-radius: 999px;
  background: var(--surface-2); color: var(--ink-3);
  display: flex; align-items: center; justify-content: center;
}
.eicon :deep(svg.ic) { width: 19px; height: 19px; }
</style>

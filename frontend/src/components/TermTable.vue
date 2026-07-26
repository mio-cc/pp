<template>
  <div v-if="!terms.length" class="empty">
    <span class="eicon"><Icon name="inbox" /></span>
    <template v-if="emptyText">{{ emptyText }}</template>
    <template v-else>
      该分支暂无术语。<br>
      可由 AI 按数据契约生成，经 <code>ingest.py check → add-terms</code> 填充。
    </template>
  </div>
  <div v-else class="tgrid">
    <button
      v-for="t in terms"
      :key="t.term_uid"
      class="tcard"
      :class="{ sel: t.term_uid === selectedUid, in: cart.has(t.term_uid) }"
      :title="t.term_uid + ' · ' + statusZh(t.status)"
      @click="$emit('select', t)"
    >
      <span class="tc-top">
        <span class="tzh">{{ t.zh_term }}</span>
        <i v-if="t.status !== 'published'" class="st-dot" :class="t.status"></i>
      </span>
      <span class="ten">{{ t.en_term || '—' }}</span>
      <span
        class="tc-add"
        :class="{ on: cart.has(t.term_uid) }"
        role="button"
        :aria-label="cart.has(t.term_uid) ? '移出提示词篮' : '加入提示词篮'"
        @click.stop="$emit('toggle', t)"
      >
        <Icon :name="cart.has(t.term_uid) ? 'check' : 'plus'" />
      </span>
    </button>
  </div>
</template>

<script setup>
import Icon from './Icon.vue'
import { useCart } from '../composables/useCart'

defineProps({
  terms: { type: Array, default: () => [] },
  selectedUid: { type: String, default: '' },
  emptyText: { type: String, default: '' },
})
defineEmits(['select', 'toggle'])

const cart = useCart()
const STATUS_ZH = { published: '已发布', review: '审核中', draft: '草稿', deprecated: '已弃用' }
function statusZh(s) { return STATUS_ZH[s] || s || '—' }
</script>

<style scoped>
/* 多列紧凑网格：一屏容纳数倍词条，分支膨胀后依然可扫读 */
.tgrid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(178px, 1fr));
  gap: 10px;
}
.tcard {
  position: relative; text-align: left;
  background: var(--surface); border-radius: var(--r);
  padding: 10px 34px 9px 13px;
  min-width: 0;
  transition: background-color .15s, box-shadow .15s;
}
.tcard:hover { box-shadow: var(--sh-sm); }
.tcard.sel { background: var(--accent-tint); box-shadow: inset 3px 0 0 var(--accent); }
.tc-top { display: flex; align-items: center; gap: 6px; min-width: 0; }
.tzh {
  font-weight: 650; font-size: 13.5px; line-height: 1.4;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.st-dot { width: 6px; height: 6px; border-radius: 50%; flex: 0 0 6px; background: var(--gray); }
.st-dot.review { background: var(--review); }
.ten {
  display: block; margin-top: 2px;
  font-family: var(--mono); font-size: 11px; color: var(--ink-3);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.tc-add {
  position: absolute; top: 50%; right: 8px; transform: translateY(-50%);
  width: 24px; height: 24px; border-radius: 999px;
  display: flex; align-items: center; justify-content: center;
  color: var(--ink-3); background: var(--surface-2);
  opacity: 0;
  transition: opacity .15s, background-color .15s, color .15s;
}
.tc-add :deep(svg.ic) { width: 13px; height: 13px; }
.tcard:hover .tc-add { opacity: 1; }
.tc-add:hover { background: var(--accent); color: #fff; }
.tc-add.on { opacity: 1; background: var(--accent); color: #fff; }
/* 触屏无 hover：加号常显 */
@media (pointer: coarse) { .tc-add { opacity: 1; } }

.empty { padding: 60px 24px; color: var(--ink-3); text-align: center; font-size: 13px; line-height: 2.1; }
.eicon {
  width: 42px; height: 42px; margin: 0 auto 12px; border-radius: 999px;
  background: var(--surface-2); color: var(--ink-3);
  display: flex; align-items: center; justify-content: center;
}
.eicon :deep(svg.ic) { width: 19px; height: 19px; }
.empty code {
  font-family: var(--mono); font-size: 11.5px; color: var(--ink-2);
  background: var(--surface-2); border-radius: var(--r-sm); padding: 2px 8px;
}

/* 窄屏：更小的列宽保持双列以上 */
@media (max-width: 620px) {
  .tgrid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }
  .tcard { padding: 9px 30px 8px 11px; }
  .tzh { font-size: 13px; }
}
</style>

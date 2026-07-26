<template>
  <div v-if="!terms.length" class="empty">
    <span class="eicon"><Icon name="inbox" /></span>
    <template v-if="emptyText">{{ emptyText }}</template>
    <template v-else>
      该分支暂无术语。<br>
      可由 AI 按数据契约生成，经 <code>ingest.py check → add-terms</code> 填充。
    </template>
  </div>
  <table v-else class="grid">
    <thead>
      <tr>
        <th>术语（名字即提示词）</th>
        <th style="width:110px">UID</th>
        <th style="width:96px">状态</th>
        <th style="width:96px"></th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="t in terms"
        :key="t.term_uid"
        class="row"
        :class="{ sel: t.term_uid === selectedUid }"
        @click="$emit('select', t)"
      >
        <td>
          <div class="tzh">{{ t.zh_term }}</div>
          <div class="ten">{{ t.en_term || '—' }}</div>
        </td>
        <td class="c-uid">{{ t.term_uid }}</td>
        <td><span class="st" :class="t.status"><i></i>{{ statusZh(t.status) }}</span></td>
        <td style="text-align:right">
          <button class="addbtn" :class="{ in: cart.has(t.term_uid) }" @click.stop="$emit('toggle', t)">
            <Icon :name="cart.has(t.term_uid) ? 'check' : 'plus'" />{{ cart.has(t.term_uid) ? '已选' : '加入' }}
          </button>
        </td>
      </tr>
    </tbody>
  </table>
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
table.grid { width: 100%; border-collapse: collapse; }
th {
  text-align: left; font-size: 10.5px; font-weight: 650; color: var(--ink-3);
  letter-spacing: .08em; padding: 8px 12px;
  border-bottom: 1px solid var(--line-2);
}
td { padding: 11px 12px; border-bottom: 1px solid var(--line); vertical-align: middle; }
tr.row { cursor: pointer; }
tr.row:hover td { background: var(--surface-2); }
tr.row.sel td { background: var(--accent-tint); }
tr.row.sel td:first-child { box-shadow: inset 3px 0 0 var(--accent); }
.tzh { font-weight: 650; font-size: 13.5px; }
.ten { font-family: var(--mono); font-size: 11.5px; color: var(--ink-3); margin-top: 2px; }
.c-uid { font-family: var(--mono); font-size: 11px; color: var(--ink-3); white-space: nowrap; }
.st { display: inline-flex; align-items: center; gap: 6px; font-size: 11.5px; color: var(--ink-2); white-space: nowrap; }
.st i { width: 6px; height: 6px; border-radius: 50%; flex: 0 0 6px; background: var(--gray); }
.st.published i { background: var(--ok); }
.st.review i { background: var(--review); }
.addbtn {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 11.5px; font-weight: 550; padding: 4px 12px; border-radius: 999px;
  border: 1px solid var(--line-2); color: var(--ink-2); background: var(--surface); white-space: nowrap;
  transition: background-color .15s, color .15s, border-color .15s;
}
.addbtn :deep(svg.ic) { width: 12px; height: 12px; }
.addbtn:hover { border-color: var(--accent); color: var(--accent-deep); background: var(--accent-tint); }
.addbtn.in { border-color: transparent; color: #fff; background: var(--accent); }
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

/* 窄屏渐进折叠：先收 UID 列，再收状态列；英文名截断防撑破 */
@media (max-width: 900px) {
  th:nth-child(2), td:nth-child(2) { display: none; }
}
@media (max-width: 620px) {
  th:nth-child(3), td:nth-child(3) { display: none; }
  th, td { padding-left: 10px; padding-right: 10px; }
  .tzh { white-space: normal; }
  .ten { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 52vw; }
  .addbtn { padding: 4px 10px; }
}
</style>

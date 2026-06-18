<template>
  <div class="grid-wrap">
    <div v-if="loading" class="grid-loading">
      <a-spin dot />
      <span style="margin-left: 10px; color: var(--mut)">加载术语…</span>
    </div>

    <template v-else>
      <div v-if="!terms.length" class="grid-empty">
        <div class="big">∅</div>
        <div>{{ emptyText }}</div>
      </div>

      <template v-else>
        <transition-group name="chip" tag="div" class="chips">
          <div
            v-for="t in paged"
            :key="t.term_uid"
            class="cchip"
            :class="{ sel: cart.has(t.term_uid) }"
            @click="$emit('detail', t)"
            @mousemove="onMove"
          >
            <div class="cn">{{ t.zh_term }}</div>
            <div class="ce">{{ t.en_term || t.zh_term || '—' }}</div>
            <span class="add" @click.stop="onAdd(t)">{{ cart.has(t.term_uid) ? '✓' : '+' }}</span>
          </div>
        </transition-group>

        <div v-if="terms.length > pageSize" class="pager">
          <a-pagination
            :total="terms.length"
            :page-size="pageSize"
            :current="page"
            size="small"
            show-total
            @change="(p) => (page = p)"
          />
        </div>
      </template>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useCart } from '../composables/useCart'

const props = defineProps({
  terms: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  emptyText: { type: String, default: '该分类暂无术语' }
})
const emit = defineEmits(['detail', 'add'])
const cart = useCart()

const page = ref(1)
const pageSize = 60
const paged = computed(() => {
  const start = (page.value - 1) * pageSize
  return props.terms.slice(start, start + pageSize)
})
// 切换分类时回到第一页
watch(() => props.terms, () => (page.value = 1))

function onAdd(t) {
  const added = cart.toggle(t)
  emit('add', { term: t, added })
}
function onMove(e) {
  const el = e.currentTarget
  const r = el.getBoundingClientRect()
  el.style.setProperty('--mx', e.clientX - r.left + 'px')
  el.style.setProperty('--my', e.clientY - r.top + 'px')
}
</script>

<style scoped>
.grid-wrap {
  min-height: 200px;
}
.grid-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
}
.grid-empty {
  text-align: center;
  padding: 70px 20px;
  color: var(--mut);
}
.grid-empty .big {
  font-size: 34px;
  margin-bottom: 12px;
  opacity: 0.5;
}
.chips {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 8px;
}
.cchip {
  background: var(--panel-solid);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 9px 11px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.cchip::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(120px 60px at var(--mx, 50%) var(--my, 0%), rgba(10, 132, 255, 0.06), transparent 70%);
  opacity: 0;
  transition: opacity 0.2s;
}
.cchip:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
  border-color: rgba(0, 0, 0, 0.14);
}
.cchip:hover::before {
  opacity: 1;
}
.cchip:active {
  transform: translateY(0) scale(0.98);
}
.cchip .cn {
  font-size: 12.5px;
  font-weight: 550;
  margin-bottom: 2px;
}
.cchip .ce {
  font-size: 10.5px;
  color: var(--mut);
  font-family: var(--mono);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.cchip.sel {
  background: var(--sel);
  border-color: var(--sel);
}
.cchip.sel .cn {
  color: #fff;
}
.cchip.sel .ce {
  color: rgba(255, 255, 255, 0.6);
}
.cchip .add {
  position: absolute;
  top: 7px;
  right: 7px;
  width: 19px;
  height: 19px;
  border-radius: 50%;
  background: var(--sel);
  color: #fff;
  font-size: 13px;
  line-height: 19px;
  text-align: center;
  opacity: 0;
  transform: scale(0.7);
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.cchip:hover .add {
  opacity: 1;
  transform: scale(1);
}
.cchip.sel .add {
  opacity: 1;
  background: #fff;
  color: var(--sel);
}
.pager {
  display: flex;
  justify-content: center;
  margin-top: 18px;
}
/* 卡片入场/移动动画 */
.chip-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.chip-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.chip-move {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>

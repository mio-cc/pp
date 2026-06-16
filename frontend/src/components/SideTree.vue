<template>
  <div class="tree">
    <div v-for="vol in volumes" :key="vol.code" class="tnode">
      <!-- 卷（一级） -->
      <div
        class="trow lv1"
        :class="{ open: expanded.has(vol.code) }"
        @click="toggleVol(vol)"
      >
        <span class="tw">▶</span>
        <span class="ico">◆</span>
        <span class="tn">{{ vol.title }}</span>
        <span class="tc">{{ vol.current_terms }}</span>
      </div>
      <!-- 分类（二级），高度过渡动画 -->
      <transition name="expand">
        <div v-show="expanded.has(vol.code)" class="kids">
          <div
            v-for="cat in vol.categories"
            :key="cat.name"
            class="trow lv2"
            :class="{ on: isActive(vol.code, cat.name) }"
            @click="selectCat(vol, cat)"
          >
            <span class="tn">{{ cat.name }}</span>
            <span class="tc">{{ cat.term_count }}</span>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  volumes: { type: Array, default: () => [] }
})
const emit = defineEmits(['select'])

const expanded = ref(new Set())
const activeKey = ref('')

function toggleVol(vol) {
  const s = new Set(expanded.value)
  if (s.has(vol.code)) s.delete(vol.code)
  else s.add(vol.code)
  expanded.value = s
}
function selectCat(vol, cat) {
  activeKey.value = `${vol.code}::${cat.name}`
  emit('select', { volume: vol, category: cat })
}
function isActive(volCode, catName) {
  return activeKey.value === `${volCode}::${catName}`
}
function expandFirst() {
  if (props.volumes.length) toggleVol(props.volumes[0])
}
defineExpose({ expandFirst })
</script>

<style scoped>
.tree {
  flex: 1;
  overflow-y: auto;
  padding: 2px 8px 14px;
}
.tnode {
  user-select: none;
}
.trow {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 6px 9px;
  cursor: pointer;
  border-radius: 8px;
  margin: 1px 0;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.trow:hover {
  background: var(--hov);
}
.trow:active {
  transform: scale(0.985);
}
.trow.on {
  background: var(--sel);
  color: #fff;
}
.trow.on .tc {
  color: rgba(255, 255, 255, 0.55);
}
.trow .tw {
  width: 14px;
  flex: 0 0 14px;
  text-align: center;
  color: var(--faint);
  font-size: 9px;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.trow.open .tw {
  transform: rotate(90deg);
}
.trow .ico {
  width: 15px;
  flex: 0 0 15px;
  color: var(--mut);
  font-size: 11px;
}
.trow .tn {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.lv1 .tn {
  font-weight: 550;
}
.lv2 {
  padding-left: 30px;
}
.lv2 .tn {
  color: var(--ink2);
  font-size: 12.5px;
}
.trow.on .tn {
  color: #fff;
}
.trow .tc {
  font-size: 10.5px;
  color: var(--faint);
  font-variant-numeric: tabular-nums;
}
.kids {
  overflow: hidden;
}
/* 展开/收起高度动画 */
.expand-enter-active,
.expand-leave-active {
  transition: max-height 0.32s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.25s ease;
  max-height: 1200px;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>

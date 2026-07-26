<template>
  <div class="bgrid">
    <button v-for="c in cards" :key="c.path" class="bcard" @click="$emit('open', c)">
      <span class="bi"><Icon :name="c.childCount ? 'folderTree' : 'tag'" /></span>
      <span class="bx">
        <span class="bn">{{ c.name }}</span>
        <span class="bs">{{ c.childCount ? c.childCount + ' 个子分支 · ' : '' }}{{ c.count }} 词{{ c.count ? '' : ' · 待填充' }}</span>
      </span>
      <span class="arr"><Icon name="chevR" /></span>
    </button>
  </div>
</template>

<script setup>
import Icon from './Icon.vue'

defineProps({ cards: { type: Array, default: () => [] } })
defineEmits(['open'])
</script>

<style scoped>
.bgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 12px; }
.bcard {
  display: flex; align-items: center; gap: 12px; text-align: left; width: 100%;
  background: var(--surface); border-radius: var(--r-lg);
  padding: 14px 16px;
  transition: box-shadow .15s;
}
.bcard:hover { box-shadow: var(--sh-sm); }
.bi {
  width: 34px; height: 34px; flex: 0 0 34px; border-radius: var(--r);
  background: var(--accent-tint); color: var(--ink-2);
  display: flex; align-items: center; justify-content: center;
}
.bi :deep(svg.ic) { width: 16px; height: 16px; }
.bx { flex: 1; min-width: 0; }
.bn { display: block; font-weight: 650; font-size: 13.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bs { display: block; font-size: 11.5px; color: var(--ink-3); margin-top: 1px; }
.arr { color: var(--line-2); transition: color .15s; }
.bcard:hover .arr { color: var(--ink); }
</style>

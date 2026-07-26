<template>
  <div>
    <div class="crumb">
      <template v-for="(s, i) in crumb" :key="i">
        <a v-if="s.fn" @click="s.fn()">{{ s.label }}</a>
        <span v-else class="cur">{{ s.label }}</span>
        <span v-if="i < crumb.length - 1" class="sep"><Icon name="chevR" /></span>
      </template>
    </div>
    <div class="pagehead">
      <h1>{{ title }}</h1>
      <div v-if="desc" class="desc">{{ desc }}</div>
      <div v-if="metas.length" class="metas">
        <span v-for="(m, i) in metas" :key="i" class="mchip">
          <Icon :name="m.icon" />{{ m.label }}<b v-if="m.num !== undefined && m.num !== ''">{{ m.num }}</b>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import Icon from './Icon.vue'

defineProps({
  crumb: { type: Array, default: () => [] },
  title: { type: String, default: '' },
  desc: { type: String, default: '' },
  metas: { type: Array, default: () => [] },
})
</script>

<style scoped>
.crumb {
  display: flex; align-items: center; gap: 7px; flex-wrap: wrap;
  font-size: 12px; margin-bottom: 10px; min-height: 18px;
}
.crumb a { color: var(--ink-3); text-decoration: none; cursor: pointer; transition: color .15s; }
.crumb a:hover { color: var(--accent-deep); }
.sep { color: var(--line-2); display: flex; }
.sep :deep(svg.ic) { width: 12px; height: 12px; }
.cur { color: var(--ink-2); }
.pagehead { margin-bottom: 22px; }
h1 { font-size: 25px; font-weight: 700; letter-spacing: .01em; line-height: 1.3; }
.desc { color: var(--ink-2); font-size: 13px; margin-top: 6px; max-width: 620px; }
.metas { display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap; }
.mchip {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 11.5px; color: var(--ink-2);
  background: var(--surface); border-radius: 999px; padding: 4px 12px;
}
.mchip b { color: var(--ink); font-weight: 650; font-family: var(--mono); font-size: 11px; }
.mchip :deep(svg.ic) { width: 12px; height: 12px; color: var(--ink-3); }

@media (max-width: 880px) {
  h1 { font-size: 20px; }
  .pagehead { margin-bottom: 16px; }
  .crumb { font-size: 11.5px; }
}
</style>

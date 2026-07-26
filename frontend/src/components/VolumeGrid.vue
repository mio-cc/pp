<template>
  <div class="vgrid">
    <button v-for="v in volumes" :key="v.code" class="vcard" @click="$emit('select', v.code)">
      <span class="vc-wm" aria-hidden="true">{{ v.code.replace('V', '') }}</span>
      <span class="vc-top">
        <span class="vc-code">{{ v.code }}</span>
        <span class="vc-title">{{ v.title }}</span>
      </span>
      <div class="vc-nums"><b>{{ v.current_terms }}</b> / {{ v.target_terms }} · {{ pct(v) }}%</div>
      <div class="pbar"><i :style="{ width: Math.max(1.5, pct(v)) + '%' }"></i></div>
    </button>
  </div>
</template>

<script setup>
defineProps({ volumes: { type: Array, default: () => [] } })
defineEmits(['select'])

function pct(v) {
  if (v.completion_percent !== undefined) return Math.round(v.completion_percent)
  return v.target_terms ? Math.round(v.current_terms * 100 / v.target_terms) : 0
}
</script>

<style scoped>
.vgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 14px; }
.vcard {
  background: var(--surface); border-radius: var(--r-lg);
  padding: 16px 16px 14px; text-align: left; display: block; width: 100%;
  transition: box-shadow .15s;
  position: relative; overflow: hidden;
}
.vcard:hover { box-shadow: var(--sh-sm); }
/* 卡角暗纹卷号：衬线大字，近乎不可见的编号纹理 */
.vc-wm {
  position: absolute; right: 8px; bottom: -10px;
  font-family: var(--serif); font-size: 52px; line-height: 1;
  color: rgba(27, 27, 29, .05);
  pointer-events: none; user-select: none;
}
.vc-top { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.vc-code { font-family: var(--mono); font-size: 10.5px; color: var(--ink-2); background: var(--accent-tint); border-radius: var(--r-sm); padding: 2px 8px; }
.vc-title { font-weight: 650; font-size: 14px; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.vc-nums { font-family: var(--mono); font-size: 11px; color: var(--ink-3); margin-bottom: 8px; }
.vc-nums b { color: var(--ink-2); font-weight: 550; }
.pbar { height: 4px; border-radius: 999px; background: var(--line); overflow: hidden; }
.pbar i { display: block; height: 100%; border-radius: 999px; background: var(--accent); }
</style>

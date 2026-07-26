<template>
  <span class="icon-wrap" v-html="svg"></span>
</template>

<script setup>
import { computed } from 'vue'
import { ICONS } from '../icons'

const props = defineProps({ name: { type: String, required: true } })
const svg = computed(() => ICONS[props.name] || '')
</script>

<style scoped>
.icon-wrap { display: inline-flex; align-items: center; justify-content: center; }
</style>

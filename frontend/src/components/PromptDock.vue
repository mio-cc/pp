<template>
  <div class="dock">
    <div class="dock-top">
      <span class="dlbl">
        <span class="icn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z" />
          </svg>
        </span>
        <span class="t">提示词篮</span>
        <span class="num" :class="{ pop }">{{ cart.count }}</span>
      </span>
      <span class="divd"></span>

      <div class="frags">
        <span v-if="!cart.items.length" class="ph">点术语卡右上角 + 添加，可拖动排序</span>
        <transition-group v-else name="frag" tag="div" class="frag-list">
          <span
            v-for="(c, i) in cart.items"
            :key="c.term_uid"
            class="frag"
            draggable="true"
            @dragstart="dragI = i"
            @dragover.prevent
            @drop="onDrop(i)"
          >
            <span class="fg">⠇</span>{{ c.zh_term }}
            <x @click="cart.remove(c.term_uid)">✕</x>
          </span>
        </transition-group>
      </div>

      <div class="acts">
        <button class="ic" :class="{ on: showPrev }" title="预览" @click="showPrev = !showPrev">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
        </button>
        <button class="ic" title="清空" @click="onClear">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6" />
          </svg>
        </button>
        <button class="copy" :class="{ done }" @click="onCopy">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
            <rect x="9" y="9" width="11" height="11" rx="2" />
            <path d="M5 15V5a2 2 0 0 1 2-2h10" />
          </svg>
          <span class="t">{{ done ? '已复制' : '复制' }}</span>
        </button>
      </div>
    </div>

    <transition name="prev">
      <div v-show="showPrev" class="dock-prev">
        <span v-if="cart.items.length">{{ cart.promptText() }}</span>
        <span v-else class="pl">空</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Message } from '@arco-design/web-vue'
import { useCart } from '../composables/useCart'

const cart = useCart()
const showPrev = ref(false)
const done = ref(false)
const pop = ref(false)
const dragI = ref(null)

// 数量变化时弹一下
watch(
  () => cart.count.value,
  () => {
    pop.value = true
    setTimeout(() => (pop.value = false), 300)
  }
)

function onDrop(to) {
  if (dragI.value === null) return
  cart.move(dragI.value, to)
  dragI.value = null
}
function onCopy() {
  if (!cart.items.length) {
    Message.info('提示词篮是空的')
    return
  }
  navigator.clipboard && navigator.clipboard.writeText(cart.promptText())
  done.value = true
  setTimeout(() => (done.value = false), 1100)
  Message.success(`已复制 ${cart.count.value} 个提示词`)
}
function onClear() {
  if (!cart.items.length) return
  cart.clear()
  Message.info('已清空提示词篮')
}
</script>

<style scoped>
.dock {
  position: fixed;
  left: 50%;
  bottom: 16px;
  transform: translateX(-50%);
  width: calc(100% - 32px);
  max-width: 1000px;
  background: rgba(250, 250, 252, 0.85);
  backdrop-filter: saturate(180%) blur(30px);
  -webkit-backdrop-filter: saturate(180%) blur(30px);
  border: 1px solid rgba(0, 0, 0, 0.07);
  border-radius: 18px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.04), 0 10px 34px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.7);
  padding: 9px 11px;
  z-index: 45;
}
.dock-top {
  display: flex;
  align-items: center;
  gap: 10px;
}
.dlbl {
  font-size: 12px;
  color: var(--ink);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 7px;
  white-space: nowrap;
  flex: 0 0 auto;
}
.dlbl .icn {
  width: 26px;
  height: 26px;
  border-radius: 8px;
  background: #fff;
  border: 1px solid var(--line);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.dlbl .icn svg {
  width: 13px;
  height: 13px;
  color: var(--ink2);
}
.dlbl .num {
  background: #ededf0;
  color: var(--ink2);
  font-size: 10.5px;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
  font-weight: 600;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.dlbl .num.pop {
  transform: scale(1.3);
  background: var(--accent);
  color: #fff;
}
.divd {
  width: 1px;
  height: 22px;
  background: var(--line);
  flex: 0 0 auto;
}
.frags {
  flex: 1;
  overflow-x: auto;
  min-height: 34px;
  display: flex;
  align-items: center;
}
.frags::-webkit-scrollbar {
  display: none;
}
.frag-list {
  display: flex;
  gap: 6px;
}
.ph {
  color: var(--mut);
  font-size: 12px;
  white-space: nowrap;
  padding-left: 2px;
}
.frag {
  background: #fff;
  border: 1px solid var(--line);
  color: var(--ink2);
  border-radius: 8px;
  padding: 5px 6px 5px 4px;
  font-size: 12px;
  display: flex;
  gap: 4px;
  align-items: center;
  white-space: nowrap;
  cursor: grab;
  box-shadow: 0 1px 1.5px rgba(0, 0, 0, 0.04);
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}
.frag:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
  border-color: rgba(0, 0, 0, 0.14);
  color: var(--ink);
}
.frag .fg {
  color: var(--faint);
  font-size: 10px;
}
.frag x {
  cursor: pointer;
  color: var(--faint);
  font-size: 12px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
.frag x:hover {
  color: #fff;
  background: #1d1d1f;
  transform: scale(1.15);
}
.acts {
  display: flex;
  gap: 6px;
  align-items: center;
  flex: 0 0 auto;
}
.ic {
  width: 31px;
  height: 31px;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: #fff;
  color: var(--mut);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}
.ic:hover {
  background: var(--hov);
  color: var(--ink2);
  transform: translateY(-1px);
}
.ic.on {
  background: var(--ink);
  color: #fff;
  border-color: var(--ink);
}
.ic svg {
  width: 15px;
  height: 15px;
}
.copy {
  background: var(--ink);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0 15px;
  height: 31px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}
.copy:hover {
  background: #000;
  transform: translateY(-1px);
}
.copy.done {
  background: #28c840;
}
.dock-prev {
  margin-top: 9px;
  padding-top: 9px;
  border-top: 1px solid var(--line);
  font-family: var(--mono);
  font-size: 11.5px;
  color: var(--ink2);
  line-height: 1.55;
  word-break: break-word;
  max-height: 60px;
  overflow: auto;
}
.dock-prev .pl {
  color: var(--faint);
}
.frag-enter-active,
.frag-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.frag-enter-from,
.frag-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
.prev-enter-active,
.prev-leave-active {
  transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}
.prev-enter-from,
.prev-leave-to {
  max-height: 0;
  opacity: 0;
  margin-top: 0;
  padding-top: 0;
}
</style>

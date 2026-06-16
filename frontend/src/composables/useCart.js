import { reactive, computed } from 'vue'

// 提示词篮全局状态（跨组件共享）
const state = reactive({
  items: [] // { term_uid, zh_term, positive_prompt, ... }
})

export function useCart() {
  const count = computed(() => state.items.length)

  function has(uid) {
    return state.items.some((x) => x.term_uid === uid)
  }
  function toggle(term) {
    const i = state.items.findIndex((x) => x.term_uid === term.term_uid)
    if (i >= 0) {
      state.items.splice(i, 1)
      return false
    }
    state.items.push(term)
    return true
  }
  function remove(uid) {
    const i = state.items.findIndex((x) => x.term_uid === uid)
    if (i >= 0) state.items.splice(i, 1)
  }
  function move(from, to) {
    if (from === to) return
    const m = state.items.splice(from, 1)[0]
    state.items.splice(to, 0, m)
  }
  function clear() {
    state.items.length = 0
  }
  function promptText() {
    return state.items
      .map((x) => x.positive_prompt || x.en_term || x.zh_term)
      .filter(Boolean)
      .join(', ')
  }

  return { items: state.items, count, has, toggle, remove, move, clear, promptText }
}

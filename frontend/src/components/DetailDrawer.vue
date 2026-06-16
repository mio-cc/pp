<template>
  <a-drawer
    :visible="visible"
    :width="380"
    :footer="false"
    :header="false"
    @cancel="$emit('close')"
    class="kb-detail-drawer"
  >
    <div v-if="term" class="detail">
      <button class="x" @click="$emit('close')">✕</button>

      <!-- 层级路径 -->
      <div class="lin">
        <span class="step"><b>{{ term.volume_title }}</b><span class="tag">体系 {{ term.volume_code }}</span></span>
        <span class="step">└ <b>{{ term.category || '未分类' }}</b><span class="tag">分类</span></span>
        <span class="step">　└ <b>{{ term.zh_term }}</b><span class="tag">术语</span></span>
      </div>

      <h2>{{ term.zh_term }}</h2>
      <div class="den">{{ term.en_term || term.term_uid }}</div>

      <div v-if="term.definition_short" class="dnote">{{ term.definition_short }}</div>
      <div v-if="term.definition_long" class="section">
        <div class="slabel">详细解释</div>
        <div class="stext">{{ term.definition_long }}</div>
      </div>
      <div v-if="term.visual_effect" class="section">
        <div class="slabel">视觉表现</div>
        <div class="stext">{{ term.visual_effect }}</div>
      </div>

      <!-- 正向提示词 -->
      <div v-if="term.positive_prompt" class="section">
        <div class="slabel">正向提示词</div>
        <div class="pb">
          <button class="cp" @click="copy(term.positive_prompt, $event)">复制</button>
          {{ term.positive_prompt }}
        </div>
      </div>
      <!-- 负向提示词 -->
      <div v-if="term.negative_prompt" class="section">
        <div class="slabel">负向提示词</div>
        <div class="pb neg">
          <button class="cp" @click="copy(term.negative_prompt, $event)">复制</button>
          {{ term.negative_prompt }}
        </div>
      </div>

      <!-- 标签 -->
      <div v-if="term.tags && term.tags.length" class="tags">
        <a-tag v-for="tg in term.tags" :key="tg" size="small" color="gray">{{ tg }}</a-tag>
      </div>

      <button class="dbtn" :class="{ added: inCart }" @click="onToggle">
        {{ inCart ? '✓ 已在提示词篮' : '＋ 加入提示词篮' }}
      </button>
    </div>
  </a-drawer>
</template>

<script setup>
import { computed } from 'vue'
import { Message } from '@arco-design/web-vue'
import { useCart } from '../composables/useCart'

const props = defineProps({
  visible: { type: Boolean, default: false },
  term: { type: Object, default: null }
})
defineEmits(['close'])
const cart = useCart()
const inCart = computed(() => props.term && cart.has(props.term.term_uid))

function onToggle() {
  if (!props.term) return
  const added = cart.toggle(props.term)
  Message.success(added ? `已添加：${props.term.zh_term}` : `已移除：${props.term.zh_term}`)
}
function copy(text, e) {
  navigator.clipboard && navigator.clipboard.writeText(text)
  const btn = e.target
  const o = btn.textContent
  btn.textContent = '已复制'
  setTimeout(() => (btn.textContent = o), 1000)
}
</script>

<style scoped>
.detail {
  position: relative;
  padding: 4px 2px;
}
.x {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  cursor: pointer;
  color: var(--ink2);
  font-size: 14px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.x:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: rotate(90deg);
}
.lin {
  font-size: 11px;
  color: var(--mut);
  line-height: 1.8;
  background: var(--bg);
  border-radius: 12px;
  padding: 11px 13px;
  margin-bottom: 16px;
}
.lin .step {
  display: block;
}
.lin .step b {
  color: var(--ink);
  font-weight: 600;
}
.lin .step .tag {
  font-size: 9px;
  color: var(--mut);
  margin-left: 6px;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 0 4px;
}
h2 {
  font-size: 21px;
  letter-spacing: -0.01em;
  margin-bottom: 3px;
}
.den {
  font-size: 12px;
  color: var(--mut);
  font-family: var(--mono);
  margin-bottom: 14px;
}
.dnote {
  font-size: 13px;
  color: var(--ink2);
  line-height: 1.6;
  margin-bottom: 16px;
}
.section {
  margin-bottom: 14px;
}
.slabel {
  font-size: 11px;
  font-weight: 600;
  color: var(--mut);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 6px;
}
.stext {
  font-size: 13px;
  color: var(--ink2);
  line-height: 1.6;
}
.pb {
  background: #1d1d1f;
  color: #e8e8ea;
  border-radius: 12px;
  padding: 13px 14px;
  font-family: var(--mono);
  font-size: 12px;
  line-height: 1.55;
  word-break: break-word;
  position: relative;
}
.pb.neg {
  background: #3a2a2a;
}
.pb .cp {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.12);
  border: none;
  color: #fff;
  border-radius: 6px;
  padding: 3px 9px;
  font-size: 10px;
  cursor: pointer;
  transition: all 0.15s;
}
.pb .cp:hover {
  background: rgba(255, 255, 255, 0.22);
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 18px;
}
.dbtn {
  width: 100%;
  background: var(--sel);
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-size: 13px;
  font-weight: 550;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.dbtn:hover {
  background: #000;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
}
.dbtn.added {
  background: #28a745;
}
</style>

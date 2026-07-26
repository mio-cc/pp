// 剪贴板写入：安全上下文用 Clipboard API，
// 局域网 http（insecure context，navigator.clipboard 不存在）回退 execCommand。
// 返回是否真的写入成功——调用方只在 true 时显示「已复制」。
export async function copyText(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
      return true
    }
    const ta = document.createElement('textarea')
    ta.value = text
    ta.setAttribute('readonly', '')
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0'
    document.body.appendChild(ta)
    ta.select()
    const ok = document.execCommand('copy')
    ta.remove()
    return ok
  } catch (e) {
    return false
  }
}

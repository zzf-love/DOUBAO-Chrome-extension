const $ = (id) => document.getElementById(id);

let captureDataUrl = null;

function renderMarkdownLike(text) {
  const frag = document.createDocumentFragment();
  const paras = text.split(/\n\s*\n/);
  for (const para of paras) {
    if (!para.trim()) continue;
    const p = document.createElement("p");
    p.textContent = para;
    frag.appendChild(p);
  }
  return frag;
}

function setStatus(text, isError = false) {
  const r = $("result");
  r.classList.remove("done");
  r.innerHTML = "";
  const div = document.createElement("div");
  div.className = "status" + (isError ? " error" : "");
  if (!isError) {
    const sp = document.createElement("span");
    sp.className = "spinner";
    div.appendChild(sp);
  }
  const span = document.createElement("span");
  span.textContent = text;
  div.appendChild(span);
  r.appendChild(div);
}

function setResult(text, isError = false) {
  const r = $("result");
  r.classList.toggle("done", !isError);
  r.innerHTML = "";
  const div = document.createElement("div");
  div.className = "result-text" + (isError ? " error" : "");
  if (isError) {
    div.textContent = text;
  } else {
    div.appendChild(renderMarkdownLike(text));
  }
  r.appendChild(div);

  if (!isError) {
    const actions = document.createElement("div");
    actions.className = "result-actions";
    actions.style.display = "flex";
    actions.style.gap = "8px";
    actions.style.marginTop = "10px";
    const copyBtn = document.createElement("button");
    copyBtn.className = "btn-mini";
    copyBtn.textContent = "复制结果";
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(text).then(() => {
        copyBtn.textContent = "已复制 ✓";
        setTimeout(() => (copyBtn.textContent = "复制结果"), 1500);
      });
    });
    actions.appendChild(copyBtn);
    r.appendChild(actions);
  }
}

async function analyze() {
  if (!captureDataUrl) return;
  $("analyze").disabled = true;
  setStatus("分析中…");
  try {
    const resp = await chrome.runtime.sendMessage({
      type: "EXPLAIN_IMAGE",
      dataUrl: captureDataUrl
    });
    if (!resp || !resp.ok) throw new Error(resp?.error || "解析失败");
    setResult(resp.text, false);
  } catch (e) {
    setResult(e.message || String(e), true);
  } finally {
    $("analyze").disabled = false;
  }
}

async function init() {
  const { pendingCapture, theme } = await chrome.storage.local.get([
    "pendingCapture",
    "theme",
  ]);
  const valid = ["aurora", "dark", "sakura"];
  document.body.dataset.theme = valid.includes(theme) ? theme : "aurora";

  if (!pendingCapture) {
    setResult("没有可解读的内容，请关闭窗口后重新触发 Alt+S。", true);
    $("analyze").disabled = true;
    $("capture").style.display = "none";
    return;
  }

  // One-shot: clear after we've loaded it so a stale capture doesn't pop up
  // next time the user opens this window directly.
  await chrome.storage.local.remove("pendingCapture");

  $("source").textContent = pendingCapture.sourceTitle
    ? `${pendingCapture.sourceTitle} — ${pendingCapture.sourceUrl}`
    : pendingCapture.sourceUrl || "";

  if (!pendingCapture.dataUrl) {
    // Capture (or injection) failed but we still opened this window so the
    // user sees what's wrong instead of pressing Alt+S in confusion.
    const why = pendingCapture.error || "未知原因";
    const hint = /Cannot access contents|chrome:\/\/|extension manifest/i.test(why)
      ? "当前页面禁止扩展注入（常见于带严格 CSP 的站点、chrome:// 页面等）。请试试在其他普通网页上使用。"
      : "可能是浏览器拒绝截屏权限，或当前页面状态不允许截图。可以稍等几秒后重试。";
    setResult("截图失败：" + why + "\n\n" + hint, true);
    $("analyze").disabled = true;
    $("capture").style.display = "none";
    return;
  }

  captureDataUrl = pendingCapture.dataUrl;
  $("capture").src = captureDataUrl;
  // Auto-trigger analysis — user already invoked Alt+S, expects the answer.
  analyze();
}

document.addEventListener("DOMContentLoaded", () => {
  $("analyze").addEventListener("click", analyze);
  $("close").addEventListener("click", () => window.close());
  init();
});

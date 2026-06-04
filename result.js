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
  if (!pendingCapture || !pendingCapture.dataUrl) {
    setResult("没有捕获到截图，请关闭窗口后重新触发 Alt+S。", true);
    $("analyze").disabled = true;
    return;
  }
  captureDataUrl = pendingCapture.dataUrl;
  $("capture").src = captureDataUrl;
  $("source").textContent = pendingCapture.sourceTitle
    ? `${pendingCapture.sourceTitle} — ${pendingCapture.sourceUrl}`
    : pendingCapture.sourceUrl || "";
  // One-shot: clear after we've loaded it so a stale capture doesn't pop up
  // next time the user opens this window directly.
  await chrome.storage.local.remove("pendingCapture");

  // Auto-trigger analysis — user already invoked Alt+S, expects the answer.
  analyze();
}

document.addEventListener("DOMContentLoaded", () => {
  $("analyze").addEventListener("click", analyze);
  $("close").addEventListener("click", () => window.close());
  init();
});

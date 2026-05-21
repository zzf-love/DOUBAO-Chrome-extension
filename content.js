(() => {
  if (window.__aiExplainerInjected) return;
  window.__aiExplainerInjected = true;

  let selecting = false;
  let startX = 0, startY = 0;
  let overlay, box, hint;
  let panel;
  let panelTasks = 0;

  function createOverlay() {
    overlay = document.createElement("div");
    overlay.className = "aie-overlay";
    box = document.createElement("div");
    box.className = "aie-box";
    hint = document.createElement("div");
    hint.className = "aie-hint";
    hint.textContent = "拖动鼠标框选要解读的区域 · Esc 取消";
    overlay.appendChild(box);
    overlay.appendChild(hint);
    document.documentElement.appendChild(overlay);
  }

  function removeOverlay() {
    if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
    overlay = box = hint = null;
    selecting = false;
  }

  function ensurePanel() {
    if (panel && document.documentElement.contains(panel)) return panel;
    panel = document.createElement("div");
    panel.className = "aie-panel";
    panel.innerHTML = `
      <div class="aie-panel-header">
        <span class="aie-panel-title">AI 解读</span>
        <div class="aie-panel-actions">
          <button class="aie-btn aie-collapse" title="折叠/展开">—</button>
          <button class="aie-btn aie-close" title="关闭">×</button>
        </div>
      </div>
      <div class="aie-panel-body"></div>
    `;
    document.documentElement.appendChild(panel);
    panel.querySelector(".aie-close").addEventListener("click", () => {
      panel.remove();
      panel = null;
    });
    panel.querySelector(".aie-collapse").addEventListener("click", () => {
      panel.classList.toggle("aie-collapsed");
    });
    makeDraggable(panel, panel.querySelector(".aie-panel-header"));
    return panel;
  }

  function makeDraggable(el, handle) {
    let dx = 0, dy = 0, dragging = false;
    handle.style.cursor = "move";
    handle.addEventListener("mousedown", (e) => {
      if (e.target.closest(".aie-btn")) return;
      dragging = true;
      const rect = el.getBoundingClientRect();
      dx = e.clientX - rect.left;
      dy = e.clientY - rect.top;
      e.preventDefault();
    });
    window.addEventListener("mousemove", (e) => {
      if (!dragging) return;
      el.style.left = (e.clientX - dx) + "px";
      el.style.top = (e.clientY - dy) + "px";
      el.style.right = "auto";
    });
    window.addEventListener("mouseup", () => { dragging = false; });
  }

  function addTaskCard() {
    const p = ensurePanel();
    const body = p.querySelector(".aie-panel-body");
    const card = document.createElement("div");
    card.className = "aie-card";
    const id = ++panelTasks;
    card.innerHTML = `
      <div class="aie-card-head">
        <span class="aie-card-id">#${id}</span>
        <span class="aie-card-status">分析中…</span>
        <span class="aie-card-spin"></span>
      </div>
      <div class="aie-card-thumb-wrap"></div>
      <div class="aie-card-text">AI 正在阅读这块内容，你可以继续浏览。</div>
    `;
    body.insertBefore(card, body.firstChild);
    return card;
  }

  function setCardThumb(card, dataUrl) {
    const wrap = card.querySelector(".aie-card-thumb-wrap");
    const img = document.createElement("img");
    img.className = "aie-card-thumb";
    img.src = dataUrl;
    wrap.appendChild(img);
  }

  function setCardResult(card, text, ok) {
    card.querySelector(".aie-card-status").textContent = ok ? "完成" : "失败";
    card.querySelector(".aie-card-spin").remove();
    const textEl = card.querySelector(".aie-card-text");
    textEl.textContent = "";
    if (ok) {
      textEl.appendChild(renderMarkdownLike(text));
    } else {
      textEl.classList.add("aie-error");
      textEl.textContent = text;
    }
  }

  function renderMarkdownLike(text) {
    const frag = document.createDocumentFragment();
    const lines = text.split(/\r?\n/);
    let buf = [];
    const flush = () => {
      if (!buf.length) return;
      const p = document.createElement("p");
      p.textContent = buf.join("\n");
      frag.appendChild(p);
      buf = [];
    };
    for (const line of lines) {
      if (!line.trim()) { flush(); continue; }
      buf.push(line);
    }
    flush();
    return frag;
  }

  async function cropImage(dataUrl, rect, dpr) {
    const img = new Image();
    img.src = dataUrl;
    await img.decode();
    const sx = Math.max(0, Math.round(rect.x * dpr));
    const sy = Math.max(0, Math.round(rect.y * dpr));
    const sw = Math.max(1, Math.round(rect.w * dpr));
    const sh = Math.max(1, Math.round(rect.h * dpr));
    const canvas = document.createElement("canvas");
    canvas.width = sw; canvas.height = sh;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, sw, sh);
    return canvas.toDataURL("image/png");
  }

  function sendMsg(msg) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(msg, (resp) => resolve(resp));
    });
  }

  async function handleSelection(rect) {
    const card = addTaskCard();
    try {
      const cap = await sendMsg({ type: "CAPTURE_VISIBLE" });
      if (!cap || !cap.ok) throw new Error(cap?.error || "截屏失败");
      const cropped = await cropImage(cap.dataUrl, rect, window.devicePixelRatio || 1);
      setCardThumb(card, cropped);
      const resp = await sendMsg({ type: "EXPLAIN_IMAGE", dataUrl: cropped });
      if (!resp || !resp.ok) throw new Error(resp?.error || "解析失败");
      setCardResult(card, resp.text, true);
    } catch (e) {
      setCardResult(card, e.message || String(e), false);
    }
  }

  function onMouseDown(e) {
    if (!overlay) return;
    if (e.button !== 0) return;
    selecting = true;
    startX = e.clientX;
    startY = e.clientY;
    box.style.left = startX + "px";
    box.style.top = startY + "px";
    box.style.width = "0px";
    box.style.height = "0px";
    box.style.display = "block";
    e.preventDefault();
  }

  function onMouseMove(e) {
    if (!overlay || !selecting) return;
    const x = Math.min(e.clientX, startX);
    const y = Math.min(e.clientY, startY);
    const w = Math.abs(e.clientX - startX);
    const h = Math.abs(e.clientY - startY);
    box.style.left = x + "px";
    box.style.top = y + "px";
    box.style.width = w + "px";
    box.style.height = h + "px";
  }

  function onMouseUp(e) {
    if (!overlay || !selecting) return;
    selecting = false;
    const rect = box.getBoundingClientRect();
    removeOverlay();
    if (rect.width < 8 || rect.height < 8) return;
    handleSelection({ x: rect.left, y: rect.top, w: rect.width, h: rect.height });
  }

  function onKeyDown(e) {
    if (e.key === "Escape" && overlay) {
      removeOverlay();
    }
  }

  function startSelection() {
    if (overlay) return;
    createOverlay();
    overlay.addEventListener("mousedown", onMouseDown, true);
    window.addEventListener("mousemove", onMouseMove, true);
    window.addEventListener("mouseup", onMouseUp, true);
    window.addEventListener("keydown", onKeyDown, true);
  }

  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg && msg.type === "START_SELECTION") {
      startSelection();
      sendResponse({ ok: true });
    }
    return true;
  });
})();

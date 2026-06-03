const PRESET_IDS = ["general", "ocr", "translate", "visual", "paper", "code"];
const CUSTOM_SLOT_COUNT = 3;
const THEMES = ["aurora", "dark", "sakura", "mono"];

const i18n = (k) => chrome.i18n.getMessage(k) || "";

function preset(id) {
  return {
    id,
    label: i18n(`preset_${id}_label`),
    prompt: i18n(`preset_${id}_prompt`),
  };
}
const PRESETS = PRESET_IDS.map(preset);

const DEFAULTS = {
  apiKey: "",
  endpoint: "https://ark.cn-beijing.volces.com/api/v3/responses",
  model: "doubao-seed-2-0-mini-260428",
  prompt: PRESETS[0].prompt,
  customPrompts: ["", "", ""],
  theme: "aurora",
};

const $ = (id) => document.getElementById(id);

let customPrompts = ["", "", ""];
let activeCustomIndex = null;

function renderPresets() {
  const host = $("presets");
  host.textContent = "";

  for (const p of PRESETS) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "preset";
    btn.dataset.preset = p.id;
    btn.textContent = p.label;
    btn.title = p.prompt.slice(0, 80) + (p.prompt.length > 80 ? "…" : "");
    btn.addEventListener("click", () => selectPreset(p));
    host.appendChild(btn);
  }

  const customLabel = i18n("customLabel") || "自定义";
  const tipEmpty = i18n("customTipEmpty");
  const tipFilled = i18n("customTipFilled");
  for (let i = 0; i < CUSTOM_SLOT_COUNT; i++) {
    const filled = !!customPrompts[i];
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "preset custom" + (filled ? " filled" : "");
    btn.dataset.custom = String(i);
    btn.textContent = `${customLabel} ${i + 1}`;
    btn.title = filled
      ? `${tipFilled}\n\n${customPrompts[i].slice(0, 80)}${customPrompts[i].length > 80 ? "…" : ""}`
      : tipEmpty;
    btn.addEventListener("click", () => selectCustom(i));
    btn.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      clearCustom(i);
    });
    host.appendChild(btn);
  }
  syncActive();
}

function selectPreset(p) {
  activeCustomIndex = null;
  $("prompt").value = p.prompt;
  syncActive();
  schedulePromptSave();
}

// Click a custom slot: select it and load its content (empty = ready to write).
function selectCustom(i) {
  activeCustomIndex = i;
  $("prompt").value = customPrompts[i] || "";
  syncActive();
  $("prompt").focus();
  schedulePromptSave();
}

function clearCustom(i) {
  if (!customPrompts[i]) return;
  if (!confirm(i18n("customConfirmClear") || "清除这个自定义 Prompt？")) return;
  customPrompts[i] = "";
  if (activeCustomIndex === i) $("prompt").value = "";
  chrome.storage.local.set({ customPrompts });
  renderPresets();
  schedulePromptSave();
}

function syncActive() {
  const cur = $("prompt").value.trim();
  for (const btn of $("presets").querySelectorAll(".preset")) {
    let match = false;
    if (btn.dataset.preset) {
      const p = PRESETS.find((x) => x.id === btn.dataset.preset);
      match = activeCustomIndex === null && p && p.prompt.trim() === cur;
    } else if (btn.dataset.custom !== undefined) {
      match = activeCustomIndex === Number(btn.dataset.custom);
    }
    btn.classList.toggle("active", !!match);
  }
}

let saveTimer = null;
function schedulePromptSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    const text = $("prompt").value.trim();
    const patch = { prompt: text || PRESETS[0].prompt };
    // If a custom slot is active, persist edits into that slot too.
    if (activeCustomIndex !== null) {
      customPrompts[activeCustomIndex] = $("prompt").value;
      patch.customPrompts = customPrompts;
    }
    chrome.storage.local.set(patch);
  }, 400);
}

function onPromptInput() {
  if (activeCustomIndex !== null) {
    customPrompts[activeCustomIndex] = $("prompt").value;
    // toggle the slot's filled border live
    const btn = $("presets").querySelector(`.preset.custom[data-custom="${activeCustomIndex}"]`);
    if (btn) btn.classList.toggle("filled", !!$("prompt").value.trim());
  }
  syncActive();
  schedulePromptSave();
}

async function load() {
  const data = await chrome.storage.local.get(Object.keys(DEFAULTS));
  $("apiKey").value = data.apiKey ?? "";
  $("endpoint").value = data.endpoint ?? DEFAULTS.endpoint;
  $("model").value = data.model ?? DEFAULTS.model;
  $("prompt").value = data.prompt ?? DEFAULTS.prompt;
  customPrompts =
    Array.isArray(data.customPrompts) && data.customPrompts.length === CUSTOM_SLOT_COUNT
      ? data.customPrompts.map((s) => (typeof s === "string" ? s : ""))
      : ["", "", ""];
  activeCustomIndex = null;
  applyTheme(data.theme || "aurora", false);

  const noKey = !$("apiKey").value.trim();
  $("noKeyAlert").style.display = noKey ? "block" : "none";
  $("apiKey").classList.toggle("error", noKey);
  renderPresets();
}

async function save() {
  const key = $("apiKey").value.trim();
  const noKey = !key;
  $("noKeyAlert").style.display = noKey ? "block" : "none";
  $("apiKey").classList.toggle("error", noKey);

  await chrome.storage.local.set({
    apiKey: key,
    endpoint: $("endpoint").value.trim() || DEFAULTS.endpoint,
    model: $("model").value.trim() || DEFAULTS.model,
    prompt: $("prompt").value.trim() || DEFAULTS.prompt,
    customPrompts,
  });

  const s = $("status");
  s.className = "status";
  s.textContent = "已保存 ✓";
  setTimeout(() => (s.textContent = ""), 1800);
}

async function reset() {
  // Reset only API / model / endpoint / prompt; keep customPrompts intact.
  await chrome.storage.local.set({
    apiKey: DEFAULTS.apiKey,
    endpoint: DEFAULTS.endpoint,
    model: DEFAULTS.model,
    prompt: DEFAULTS.prompt,
  });
  await load();
  const s = $("status");
  s.className = "status";
  s.textContent = "已恢复默认";
  setTimeout(() => (s.textContent = ""), 1800);
}

function openApiKeyPage(e) {
  e.preventDefault();
  const lang = (chrome.i18n.getUILanguage() || "").toLowerCase();
  const isChinese = lang.startsWith("zh");
  const url = isChinese
    ? "https://xhslink.com/m/6MdPRZW9PL2"
    : "https://x.com/OKLUCKY2026";
  chrome.tabs.create({ url });
}

function openVolcengine(e) {
  e.preventDefault();
  chrome.tabs.create({
    url: "https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey",
  });
}

function openShortcutSettings(e) {
  e.preventDefault();
  // Chrome restricts chrome:// URLs but allows this specific shortcuts page.
  chrome.tabs.create({ url: "chrome://extensions/shortcuts" });
}

function applyI18nLabels() {
  const map = {
    presetLabel: "presetLabel",
    getApiKey: "getApiKey",
    volcengineLink: "volcengineLink",
  };
  for (const [id, key] of Object.entries(map)) {
    const msg = i18n(key);
    if (msg && $(id)) $(id).textContent = msg;
  }
  const v = chrome.runtime.getManifest().version;
  if ($("version")) $("version").textContent = "v" + v;
}

function applyTheme(theme, persist = true) {
  if (!THEMES.includes(theme)) theme = "aurora";
  document.body.dataset.theme = theme;
  for (const btn of document.querySelectorAll(".theme-dot")) {
    btn.classList.toggle("active", btn.dataset.theme === theme);
  }
  if (persist) chrome.storage.local.set({ theme });
}

document.addEventListener("DOMContentLoaded", () => {
  applyI18nLabels();
  load();
  $("save").addEventListener("click", save);
  $("reset").addEventListener("click", reset);
  $("getApiKey").addEventListener("click", openApiKeyPage);
  $("volcengineLink").addEventListener("click", openVolcengine);
  const cs = $("customShortcut");
  if (cs) cs.addEventListener("click", openShortcutSettings);
  $("apiKey").addEventListener("input", () => {
    const noKey = !$("apiKey").value.trim();
    $("noKeyAlert").style.display = noKey ? "block" : "none";
    $("apiKey").classList.toggle("error", noKey);
  });
  $("prompt").addEventListener("input", onPromptInput);
  for (const btn of document.querySelectorAll(".theme-dot")) {
    btn.addEventListener("click", () => applyTheme(btn.dataset.theme));
  }
});

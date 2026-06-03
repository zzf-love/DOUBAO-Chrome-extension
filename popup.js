const PRESET_IDS = ["general", "ocr", "translate", "visual", "paper", "code"];
const CUSTOM_SLOT_COUNT = 3;

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
};

const $ = (id) => document.getElementById(id);

let customPrompts = ["", "", ""];

function renderPresets() {
  const host = $("presets");
  host.textContent = "";

  // built-in presets
  for (const p of PRESETS) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "preset";
    btn.dataset.preset = p.id;
    btn.textContent = p.label;
    btn.title = p.prompt.slice(0, 80) + (p.prompt.length > 80 ? "…" : "");
    btn.addEventListener("click", () => {
      $("prompt").value = p.prompt;
      syncActivePreset();
      schedulePromptSave();
    });
    host.appendChild(btn);
  }

  // custom slots
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
    btn.addEventListener("click", () => handleCustomClick(i));
    btn.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      handleCustomClear(i);
    });
    host.appendChild(btn);
  }
  syncActivePreset();
}

function handleCustomClick(i) {
  if (customPrompts[i]) {
    $("prompt").value = customPrompts[i];
    syncActivePreset();
    schedulePromptSave();
    return;
  }
  const cur = $("prompt").value.trim();
  if (!cur) {
    alert(i18n("customNeedPrompt") || "请先在下方输入要保存的 Prompt");
    return;
  }
  customPrompts[i] = cur;
  chrome.storage.local.set({ customPrompts });
  renderPresets();
}

function handleCustomClear(i) {
  if (!customPrompts[i]) return;
  if (!confirm(i18n("customConfirmClear") || "清除这个自定义 Prompt？")) return;
  customPrompts[i] = "";
  chrome.storage.local.set({ customPrompts });
  renderPresets();
}

function syncActivePreset() {
  const cur = $("prompt").value.trim();
  for (const btn of $("presets").querySelectorAll(".preset")) {
    let match = false;
    if (btn.dataset.preset) {
      const p = PRESETS.find((x) => x.id === btn.dataset.preset);
      match = p && p.prompt.trim() === cur;
    } else if (btn.dataset.custom !== undefined) {
      const slot = customPrompts[Number(btn.dataset.custom)];
      match = !!slot && slot.trim() === cur;
    }
    btn.classList.toggle("active", !!match);
  }
}

let saveTimer = null;
function schedulePromptSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    chrome.storage.local.set({ prompt: $("prompt").value.trim() || PRESETS[0].prompt });
  }, 400);
}

async function load() {
  const data = await chrome.storage.local.get(Object.keys(DEFAULTS));
  $("apiKey").value = data.apiKey ?? "";
  $("endpoint").value = data.endpoint ?? DEFAULTS.endpoint;
  $("model").value = data.model ?? DEFAULTS.model;
  $("prompt").value = data.prompt ?? DEFAULTS.prompt;
  customPrompts = Array.isArray(data.customPrompts) && data.customPrompts.length === CUSTOM_SLOT_COUNT
    ? data.customPrompts.map((s) => (typeof s === "string" ? s : ""))
    : ["", "", ""];

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
  // Reset only API / model / endpoint / prompt; keep customPrompts intact
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

function applyI18nLabels() {
  const presetLabel = i18n("presetLabel");
  if (presetLabel) $("presetLabel").textContent = presetLabel;
  const getKey = i18n("getApiKey");
  if (getKey) $("getApiKey").textContent = getKey;
  const vol = i18n("volcengineLink");
  if (vol) $("volcengineLink").textContent = vol;
}

document.addEventListener("DOMContentLoaded", () => {
  applyI18nLabels();
  load();
  $("save").addEventListener("click", save);
  $("reset").addEventListener("click", reset);
  $("getApiKey").addEventListener("click", openApiKeyPage);
  $("volcengineLink").addEventListener("click", openVolcengine);
  $("apiKey").addEventListener("input", () => {
    const noKey = !$("apiKey").value.trim();
    $("noKeyAlert").style.display = noKey ? "block" : "none";
    $("apiKey").classList.toggle("error", noKey);
  });
  $("prompt").addEventListener("input", () => {
    syncActivePreset();
    schedulePromptSave();
  });
});

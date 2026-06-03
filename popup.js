const PRESET_IDS = ["general", "ocr", "translate", "reverse", "paper", "code"];

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
};

const $ = (id) => document.getElementById(id);

function renderPresets() {
  const host = $("presets");
  host.textContent = "";
  for (const p of PRESETS) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "preset";
    btn.dataset.id = p.id;
    btn.textContent = p.label;
    btn.title = p.prompt.slice(0, 80) + (p.prompt.length > 80 ? "…" : "");
    btn.addEventListener("click", () => {
      $("prompt").value = p.prompt;
      syncActivePreset();
      schedulePromptSave();
    });
    host.appendChild(btn);
  }
}

function syncActivePreset() {
  const cur = $("prompt").value.trim();
  for (const btn of $("presets").querySelectorAll(".preset")) {
    const p = PRESETS.find((x) => x.id === btn.dataset.id);
    btn.classList.toggle("active", p && p.prompt.trim() === cur);
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

  const noKey = !$("apiKey").value.trim();
  $("noKeyAlert").style.display = noKey ? "block" : "none";
  $("apiKey").classList.toggle("error", noKey);
  syncActivePreset();
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
  });

  const s = $("status");
  s.className = "status";
  s.textContent = "已保存 ✓";
  setTimeout(() => (s.textContent = ""), 1800);
}

async function reset() {
  await chrome.storage.local.set(DEFAULTS);
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

function applyI18nLabels() {
  const presetLabel = i18n("presetLabel");
  if (presetLabel) $("presetLabel").textContent = presetLabel;
  const getKey = i18n("getApiKey");
  if (getKey) $("getApiKey").textContent = getKey;
}

document.addEventListener("DOMContentLoaded", () => {
  applyI18nLabels();
  renderPresets();
  load();
  $("save").addEventListener("click", save);
  $("reset").addEventListener("click", reset);
  $("getApiKey").addEventListener("click", openApiKeyPage);
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

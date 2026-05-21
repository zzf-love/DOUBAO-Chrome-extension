const DEFAULTS = {
  apiKey: "",
  endpoint: "https://ark.cn-beijing.volces.com/api/v3/responses",
  model: "doubao-seed-2-0-mini-260428",
  prompt: "请用简体中文解析这张截图里的内容。如果是文字，请先把可见文字完整转录出来（保留结构），再用一段话解释其含义、出处或背景。如果是图表/界面/代码，请说明它在表达什么。回答要准确、简洁，避免空话。"
};

const $ = (id) => document.getElementById(id);

async function load() {
  const data = await chrome.storage.local.get(Object.keys(DEFAULTS));
  $("apiKey").value = data.apiKey ?? "";
  $("endpoint").value = data.endpoint ?? DEFAULTS.endpoint;
  $("model").value = data.model ?? DEFAULTS.model;
  $("prompt").value = data.prompt ?? DEFAULTS.prompt;

  const noKey = !$("apiKey").value.trim();
  $("noKeyAlert").style.display = noKey ? "block" : "none";
  $("apiKey").classList.toggle("error", noKey);
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
    prompt: $("prompt").value.trim() || DEFAULTS.prompt
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

document.addEventListener("DOMContentLoaded", () => {
  load();
  $("save").addEventListener("click", save);
  $("reset").addEventListener("click", reset);
  $("apiKey").addEventListener("input", () => {
    const noKey = !$("apiKey").value.trim();
    $("noKeyAlert").style.display = noKey ? "block" : "none";
    $("apiKey").classList.toggle("error", noKey);
  });
});

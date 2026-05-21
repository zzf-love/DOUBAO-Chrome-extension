const DEFAULT_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/responses";
const DEFAULT_MODEL = "doubao-seed-2-0-mini-260428";
const DEFAULT_PROMPT = "请用简体中文解析这张截图里的内容。如果是文字，请先把可见文字完整转录出来（保留结构），再用一段话解释其含义、出处或背景。如果是图表/界面/代码，请说明它在表达什么。回答要准确、简洁，避免空话。";

async function getConfig() {
  const data = await chrome.storage.local.get(["apiKey", "endpoint", "model", "prompt"]);
  return {
    apiKey: data.apiKey || "",
    endpoint: data.endpoint || DEFAULT_ENDPOINT,
    model: data.model || DEFAULT_MODEL,
    prompt: data.prompt || DEFAULT_PROMPT
  };
}

async function captureVisibleTab(windowId) {
  return new Promise((resolve, reject) => {
    chrome.tabs.captureVisibleTab(windowId, { format: "png" }, (dataUrl) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        resolve(dataUrl);
      }
    });
  });
}

function extractResponseText(json) {
  if (typeof json?.output_text === "string" && json.output_text.length) return json.output_text;
  const parts = [];
  const output = json?.output;
  if (Array.isArray(output)) {
    for (const item of output) {
      const content = item?.content;
      if (Array.isArray(content)) {
        for (const c of content) {
          if (typeof c?.text === "string") parts.push(c.text);
          else if (typeof c?.output_text === "string") parts.push(c.output_text);
        }
      } else if (typeof item?.text === "string") {
        parts.push(item.text);
      }
    }
  }
  if (parts.length) return parts.join("\n");
  const fallback = json?.choices?.[0]?.message?.content;
  if (typeof fallback === "string") return fallback;
  return "";
}

async function callDoubao(imageDataUrl, userPrompt) {
  const cfg = await getConfig();
  if (!cfg.apiKey) throw new Error("未配置 API Key，请在扩展弹窗里填写。");

  const body = {
    model: cfg.model,
    input: [
      {
        role: "user",
        content: [
          { type: "input_image", image_url: imageDataUrl },
          { type: "input_text", text: userPrompt || cfg.prompt }
        ]
      }
    ]
  };

  const resp = await fetch(cfg.endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${cfg.apiKey}`
    },
    body: JSON.stringify(body)
  });

  const text = await resp.text();
  if (!resp.ok) {
    throw new Error(`API ${resp.status}: ${text.slice(0, 500)}`);
  }
  let json;
  try { json = JSON.parse(text); } catch { throw new Error("API 返回非 JSON: " + text.slice(0, 200)); }
  const out = extractResponseText(json);
  if (!out) throw new Error("API 返回缺少文本: " + text.slice(0, 200));
  return out;
}

async function triggerCapture(tab) {
  if (!tab || !tab.id) return;
  if (/^(chrome|edge|about|chrome-extension):/.test(tab.url || "")) {
    return;
  }
  try {
    await chrome.tabs.sendMessage(tab.id, { type: "START_SELECTION" });
  } catch (e) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["content.js"]
      });
      await chrome.scripting.insertCSS({
        target: { tabId: tab.id },
        files: ["content.css"]
      });
      await chrome.tabs.sendMessage(tab.id, { type: "START_SELECTION" });
    } catch (err) {
      console.error("注入失败：", err);
    }
  }
}

chrome.commands.onCommand.addListener(async (command) => {
  if (command !== "start-capture") return;
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  triggerCapture(tab);
});

chrome.action.onClicked.addListener((tab) => {
  triggerCapture(tab);
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "ai-explain-capture",
    title: chrome.i18n.getMessage("contextMenuTitle") || "用 AI 解读这块区域",
    contexts: ["page", "selection", "image"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "ai-explain-capture") triggerCapture(tab);
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    try {
      if (msg.type === "CAPTURE_VISIBLE") {
        const dataUrl = await captureVisibleTab(sender.tab.windowId);
        sendResponse({ ok: true, dataUrl });
      } else if (msg.type === "EXPLAIN_IMAGE") {
        const text = await callDoubao(msg.dataUrl, msg.prompt);
        sendResponse({ ok: true, text });
      } else if (msg.type === "GET_CONFIG") {
        const cfg = await getConfig();
        sendResponse({ ok: true, cfg });
      }
    } catch (e) {
      sendResponse({ ok: false, error: e.message || String(e) });
    }
  })();
  return true;
});

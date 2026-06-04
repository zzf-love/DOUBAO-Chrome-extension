# Chrome Web Store 提交文案

提交时直接复制下面的字段到开发者后台。

---

## 商店名称 (Name) — 最多 45 字

```
AI 截图解读 — Doubao Screenshot Explainer
```

## 简短说明 (Summary) — 最多 132 字

中文：
```
按 Alt+S 拖拽框选网页任意区域，豆包多模态 AI 自动解读截图内容，结果显示在右上角浮动面板，不打断浏览。
```

English:
```
Press Alt+S to drag-select any area on a webpage. The Doubao multimodal AI explains the content in a floating panel without interrupting your browsing.
```

## 详细描述 (Description)

> CWS 后台 zh-CN 和 en 两个语言各有独立"说明"字段。下面分两段，分别粘贴。

### zh-CN

```
【一句话介绍】
按 Alt+S 框选网页任意区域，AI 自动解读截图内容，结果出现在右上角浮动面板，你可以继续浏览不被打断。6 个内置 Prompt 模板覆盖翻译、读论文、视觉解析等高频场景，再加 3 个自定义槽和 3 套皮肤。

【适合谁】
- 看外文（英/日/韩）文档或截图想快速理解、保留原排版的人
- 设计师/创作者想从一张图提取构图、配色、风格关键词
- 研究生/科研人想快速消化论文截图（图表、公式、结果数据）
- 程序员看截图代码、报错信息想要 AI 解读
- 看到图表、术语、UI 想问 AI 是什么意思的人
- 不想为了问一个问题切到 ChatGPT 上传图片的人

【怎么用】
1. 在任意网页按下 Alt+S（备用 Alt+Shift+S，两者都可在 chrome://extensions/shortcuts 自定义；也可以右键菜单"用 AI 解读这块区域"）
2. 鼠标拖拽框选你想问的区域，右键或 Esc 取消
3. 几秒后，右上角浮动面板出现 AI 的解读结果
4. 同一页面可以连续框选多次，每次结果都会作为一张卡片保留
5. PDF / chrome:// 等无法注入的页面会自动切到全屏模式，整页捕获给 AI 解读

【Prompt 模板（v1.3 新功能）】
点 popup 里的药丸标签一键切换，框选时用当前选中的 Prompt：
✦ 通用解读：默认，啥都能问，先转录后解释
✦ 转录文字：纯 OCR，只把图里文字按原版式提取
✦ 翻译：外文 → 简体中文，保留段落/列表/代码结构
✦ 视觉解析：拆解图片构图/光照/配色（带 HEX）/风格，给一段通用 prompt（Midjourney / Stable Diffusion / 即梦 / Nano Banana / ChatGPT / DALL·E / Flux 都能用）
✦ 读论文：按论文领域自动判断（CS / 生医 / 物理化学 / 经济 / 心理 / 人文社科），按该学科审稿习惯输出（核心 claim / 关键方法 / 显著性 / 可疑点）
✦ 代码解释：按段讲解逻辑、标 bug / 性能问题 / 安全隐患，保留标识符不翻译
另有 3 个自定义槽，写你自己的 Prompt 存进去，跟内置模板平起平坐。

【皮肤切换（v1.3 新功能）】
popup 顶部 3 个色点一键切换：
✦ Aurora（默认）：蓝紫渐变
✦ Dark：深色护眼
✦ Sakura：粉系暖色
浮动面板、PDF 全屏窗口同步换肤，已经开着的面板也会实时跟着变色，无需重开。

【特点】
✓ 快捷键触发，不打断浏览节奏（主键 Alt+S，备用键 Alt+Shift+S，都可自定义）
✓ 浮动面板可拖动、可折叠、多任务卡片留存
✓ 6 内置 + 3 自定义 Prompt 模板，覆盖翻译、论文、设计、代码场景
✓ 3 套皮肤实时切换，全局生效
✓ PDF / chrome:// 等受限页面自动回退全屏模式，照样能用
✓ 设置仅存本地（chrome.storage.local），API Key 不上传任何第三方
✓ 默认接火山方舟（豆包 Seed 2.0 多模态），Endpoint / 模型 / Prompt 全部可自定义
✓ 中英文 UI 跟随浏览器语言自动切换

【需要准备】
首次使用前请在扩展弹窗里填入你自己的火山方舟 API Key（ark- 开头）。popup 内"免费领取 Key"和"去火山引擎获取"两个按钮可一键直达。Key 仅存在你本地浏览器，截图直接发往你配置的 API 端点，扩展开发者不接触任何数据。

【隐私】
扩展不收集任何浏览数据，不使用 Cookie，不做分析与广告，不加载任何远程代码。完整隐私政策见：
https://zzf-love.github.io/DOUBAO-Chrome-extension/privacy.html

【开源 / 反馈】
源码与 issue 在 GitHub：
https://github.com/zzf-love/DOUBAO-Chrome-extension
```

### en

```
【One-liner】
Press Alt+S to drag-select any region on a webpage; AI explains the screenshot in a floating panel — without interrupting your browsing. Six built-in Prompt presets cover translation, paper reading, visual analysis, code explanation and more, plus three custom slots and three themes.

【Who it's for】
- Reading foreign documents (English / Japanese / Korean) and want fast comprehension that preserves layout
- Designers / creators wanting to extract composition, color palette, style keywords from an image
- Grad students / researchers digesting paper screenshots (figures, equations, results data)
- Developers reading code or error screenshots and wanting AI to walk through it
- Anyone seeing a chart, term, or UI element they want AI to explain
- Anyone tired of switching to ChatGPT and uploading images just to ask one question

【How to use】
1. Press Alt+S on any webpage (backup: Alt+Shift+S; both customizable via chrome://extensions/shortcuts; or right-click menu "Explain this region with AI")
2. Drag-select the region you want explained; right-click or Esc cancels
3. The AI's explanation appears in a floating panel at the top right within a few seconds
4. Same page can be region-selected multiple times — each result is a card that stays
5. PDF / chrome:// pages that can't be injected automatically fall back to fullscreen mode that captures the whole visible area

【Prompt presets (new in v1.3)】
Switch with one click using the chip row in the popup; whatever is selected gets sent on your next selection:
✦ General: default — handles anything; transcribes then explains
✦ Transcribe: pure OCR, extracts verbatim text preserving structure
✦ Translate: foreign → English, keeps paragraph / list / code structure
✦ Visual analysis: decomposes composition, lighting, color palette (with HEX), style; outputs a generic prompt usable in any AI image tool (Midjourney / Stable Diffusion / Jimeng / Nano Banana / ChatGPT / DALL·E / Flux)
✦ Read paper: auto-detects field (CS / biomedical / physics / chemistry / economics / psychology / humanities), outputs in that field's review conventions (core claim / key methods / significance / red flags)
✦ Explain code: block-by-block walkthrough, flags bugs / perf / security; preserves identifiers
Plus 3 custom slots — write your own prompts and they sit alongside the built-ins.

【Themes (new in v1.3)】
Three theme dots in the popup header:
✦ Aurora (default): blue-purple gradient
✦ Dark: easy on the eyes
✦ Sakura: warm pink
Floating panel and PDF fullscreen window all follow; already-open panels recolor live, no reload needed.

【Features】
✓ Keyboard-driven, doesn't break browsing flow (primary Alt+S, backup Alt+Shift+S, both customizable)
✓ Draggable, collapsible floating panel with multi-task card stacking
✓ 6 built-in + 3 custom Prompt templates for translation, papers, design, code
✓ 3 themes with instant switching across all extension UI
✓ PDF and restricted pages fall back to fullscreen mode automatically
✓ All settings stored locally (chrome.storage.local) — API key never leaves your device
✓ Default endpoint: Volcengine Ark (Doubao Seed 2.0 multimodal); endpoint / model / prompt all customizable
✓ Bilingual UI auto-switching by browser locale

【Setup】
Before first use, paste your own Volcengine Ark API Key (starts with "ark-") in the extension popup. Two in-popup links — "Get free key" and "Volcengine console" — take you directly there. The key is stored locally; screenshots POST directly to your configured endpoint; the extension author never sees your data.

【Privacy】
The extension collects no browsing data, uses no cookies, runs no analytics, serves no ads, loads no remote code. Full privacy policy:
https://zzf-love.github.io/DOUBAO-Chrome-extension/privacy.html

【Open source / Feedback】
Source code and issues on GitHub:
https://github.com/zzf-love/DOUBAO-Chrome-extension
```

## 类别 (Category)

```
Productivity (生产工具)
```

## 语言 (Language)

```
中文（简体）+ English
```

## 单一用途说明 (Single Purpose) — Permission justification

```
This extension has a single purpose: capturing a user-selected screenshot region and sending it to a user-configured multimodal AI endpoint (default: Volcengine Ark / Doubao) to get an explanation displayed in an on-page panel.
```

## 权限使用理由 (Permission Justification)

### activeTab
```
Used to capture a screenshot of the user's current tab only when the user explicitly triggers the capture (via Alt+S, toolbar icon, or context menu). The extension never captures tabs in the background.
```

### tabs
```
Used together with chrome.tabs.captureVisibleTab() to obtain the screenshot of the currently active tab when the user invokes the capture command.
```

### scripting
```
Used to inject the selection-overlay UI and result panel into the active page when the user triggers a capture.
```

### storage
```
Used to persist the user's settings (API Key, model name, endpoint URL, default prompt) locally via chrome.storage.local. Nothing is synced to the cloud.
```

### contextMenus
```
Used to provide a right-click menu entry ("用 AI 解读这块区域") as an alternative to the Alt+S shortcut.
```

### Host permission: https://ark.cn-beijing.volces.com/*
```
The default AI endpoint is Volcengine Ark (Doubao). This host permission is required so the extension's background service worker can POST the captured screenshot to the Responses API for analysis. Users can change the endpoint in settings.
```

### Remote code
```
No remote code is loaded or executed. All JS/CSS is bundled in the extension package. The extension only sends image data to the user-configured API endpoint and renders the returned text.
```

## 隐私政策 URL

```
https://zzf-love.github.io/DOUBAO-Chrome-extension/privacy.html
```

## 数据收集声明 (Data usage disclosures)

提交时需勾选：

- [x] **Personally identifiable information** — No
- [x] **Health information** — No
- [x] **Financial and payment information** — No
- [x] **Authentication information** — Yes（API Key 用户自己填，仅本地存储；声明：not sold, not used for unrelated purposes, not transferred to third parties except for processing on user's behalf）
- [x] **Personal communications** — No
- [x] **Location** — No
- [x] **Web history** — No
- [x] **User activity** — No
- [x] **Website content** — Yes（用户主动框选的截图区域；声明同上，仅按用户请求转发至用户配置的 API）

证书声明三项均勾选：
- [x] I do not sell or transfer user data to third parties, outside of the approved use cases
- [x] I do not use or transfer user data for purposes that are unrelated to my item's single purpose
- [x] I do not use or transfer user data to determine creditworthiness or for lending purposes

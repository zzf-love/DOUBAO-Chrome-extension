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

```
【一句话介绍】
按 Alt+S 框选网页任意区域，AI 自动解读截图内容，结果出现在右上角浮动面板，你可以继续浏览，不被打断。

【适合谁】
- 看英文 / 日文 / 代码截图想快速理解的人
- 看到图表、错误信息、术语想问 AI 是什么意思的人
- 不想为了问一个问题切到 ChatGPT 上传图片的人

【怎么用】
1. 在任意网页按下 Alt + S（也可以点扩展图标、或右键菜单"用 AI 解读这块区域"）
2. 鼠标拖拽框选你想问的区域，右键或 Esc 取消
3. 几秒后，右上角浮动面板出现 AI 的解读结果
4. 同一页面可以连续框选多次，每次结果都会作为一张卡片保留

【特点】
✓ 快捷键触发，不打断浏览节奏
✓ 浮动面板可拖动、可折叠、多任务卡片留存
✓ 设置仅存本地（chrome.storage.local），API Key 不上传任何第三方
✓ 默认接火山方舟（豆包 Seed 2.0 多模态），Endpoint / 模型 / Prompt 可自定义

【需要准备】
首次使用前请在扩展弹窗里填入你自己的火山方舟 API Key（ark- 开头）。Key 仅存在你本地浏览器，截图直接发往你配置的 API 端点，扩展开发者不接触任何数据。

【隐私】
扩展不收集任何浏览数据，不使用 Cookie，不做分析与广告。完整隐私政策见：
https://zzf-love.github.io/DOUBAO-Chrome-extension/privacy.html

【English】
Press Alt+S to drag-select any region on a webpage, the Doubao multimodal AI explains what's inside in a floating panel — perfect for understanding screenshots of foreign text, code, error messages, charts, or unfamiliar terminology without leaving the page. Your API key is stored locally only; the extension never collects or uploads your browsing data.
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

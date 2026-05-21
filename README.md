# AI 截图解读 (Doubao Chrome Extension)

一个 Chrome MV3 扩展：在任意网页按下快捷键，鼠标拖拽框选区域，自动把这块内容交给豆包多模态模型解析，并在网页右上角面板里展示结果。你可以继续浏览或干别的事，结果出来后再回头看。

## 功能

- **快捷键触发框选**：默认 `Alt + Shift + S`，也可以点击扩展图标，或右键菜单 "用 AI 解读这块区域"。
- **拖拽框选**：跟系统截图一样的体验，`Esc` 取消。
- **后台异步解析**：调用接口期间面板显示 "分析中…"，你可以继续滚动浏览。
- **多任务面板**：右上角浮动面板可拖动、可折叠、可关闭。每次框选会新增一张卡片，包含缩略图 + 解析文本。
- **本地存储配置**：API Key / 模型 / Endpoint / 默认 Prompt 都可在弹窗里改，保存在 `chrome.storage.local`，不会发到任何第三方。

## 安装（开发者模式）

1. 打开 `chrome://extensions`
2. 右上角打开 **开发者模式**
3. 点 **加载已解压的扩展程序**，选择本仓库目录
4. （可选）点扩展图标 → 检查 / 修改 API Key 等设置

## 使用

1. 在任意网页按 `Alt + Shift + S`（Mac 同样）
2. 鼠标拖拽框选你不理解的区域
3. 看右上角面板：先出现 "分析中…"，几秒后出现结果
4. 同时可以继续滚动 / 切标签页 / 干别的，结果会留在面板里

## 接口

默认请求火山方舟 (ARK) 的 OpenAI 兼容接口：

```
POST https://ark.cn-beijing.volces.com/api/v3/chat/completions
Authorization: Bearer <API_KEY>

{
  "model": "doubao-1-5-vision-pro-32k-250115",
  "messages": [
    { "role": "user", "content": [
        { "type": "image_url", "image_url": { "url": "data:image/png;base64,..." } },
        { "type": "text",      "text": "请用简体中文解析这张截图里的内容..." }
    ]}
  ]
}
```

如果你需要换成别的视觉模型（例如最新版 `doubao-1.5-vision-*` 或 `doubao-vision-*`），在扩展弹窗里改 `模型` 字段即可。

## 文件结构

```
manifest.json    # MV3 清单 + 快捷键 + 权限
background.js    # service worker：截屏、调用豆包 API
content.js       # 注入网页：框选 UI、裁剪图像、结果面板
content.css      # 覆盖层和结果面板样式
popup.html/.js   # 设置弹窗
```

## 隐私

- 截图只发往你在设置里配置的 endpoint（默认是火山方舟）。
- API Key 仅存在本地 `chrome.storage.local`。
- 扩展不收集、不上报任何数据。

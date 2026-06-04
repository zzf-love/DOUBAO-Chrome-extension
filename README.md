# AI 截图解读 · Doubao Screenshot Explainer

> 在任意网页按 **Alt+S** 拖拽框选，豆包多模态 AI 自动解读截图内容，结果留在右上角浮动面板——不打断浏览。

![status](https://img.shields.io/badge/Chrome%20Web%20Store-审核中-blue)
![version](https://img.shields.io/badge/version-1.3.7-green)
![manifest](https://img.shields.io/badge/manifest-v3-orange)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 截图

| 框选任意区域 | AI 浮动面板解读 |
|---|---|
| ![](store/store-01.png) | ![](store/store-02.png) |
| **本地存储设置** | **多次框选累积留存** |
| ![](store/store-03.png) | ![](store/store-04.png) |

---

## 功能

- **快捷键触发框选**：默认 `Alt+S`，也支持点击扩展图标 / 右键菜单 "用 AI 解读这块区域"
- **拖拽框选**：跟系统截图一样的体验，**右键** 或 `Esc` 取消
- **后台异步解析**：调用 API 期间面板显示 "分析中…"，可继续滚动浏览
- **多任务面板**：右上角浮动面板可拖动、可折叠、可关闭，每次框选累积一张卡片（缩略图 + 解析文本）
- **本地存储配置**：API Key / 模型 / Endpoint / 默认 Prompt 都在弹窗里改，存于 `chrome.storage.local`，不上传任何第三方

## 适合谁

- 看英文 / 日文 / 代码截图想快速理解
- 看到图表、错误信息、术语想直接问 AI
- 不想为了问一个问题切到 ChatGPT 上传图片

---

## 安装

### 方式一：Chrome 应用商店（审核中）

正在审核中，通过后会贴出商店链接。

### 方式二：开发者模式（立即可用）

```bash
git clone https://github.com/zzf-love/DOUBAO-Chrome-extension.git
```

1. 打开 `chrome://extensions`
2. 右上角打开 **开发者模式**
3. 点 **加载已解压的扩展程序**，选择 `DOUBAO-Chrome-extension/` 目录
4. 点扩展图标，填入你自己的 [火山方舟 API Key](https://www.volcengine.com/product/ark)（`ark-` 开头）→ 保存

---

## 使用

1. 在任意网页按 **`Alt+S`**
2. 鼠标拖拽框选你想问的区域
3. 几秒后，右上角浮动面板出现 AI 解读结果
4. 同一页面可以连续框选多次，每次结果都会作为一张卡片留存

---

## 接口

默认请求火山方舟 (ARK) 的 Responses API：

```http
POST https://ark.cn-beijing.volces.com/api/v3/responses
Authorization: Bearer <API_KEY>

{
  "model": "doubao-seed-2-0-mini-260428",
  "input": [
    { "role": "user", "content": [
        { "type": "input_image", "image_url": "data:image/png;base64,..." },
        { "type": "input_text",  "text": "请用简体中文解析这张截图里的内容..." }
    ]}
  ]
}
```

模型 / Endpoint 都可在弹窗里改，理论兼容任何 OpenAI Responses 风格的视觉模型 API。

---

## 文件结构

```
manifest.json         # MV3 清单（权限、快捷键、host_permissions）
background.js         # service worker：截屏、调用 AI API
content.js / .css     # 注入页面：框选 UI、裁剪图像、结果面板
popup.html / .js      # 设置弹窗
privacy.html          # 隐私政策页（GitHub Pages 托管）
icons/                # 16/48/128px 图标
store/                # CWS 上架素材（4 张截图 + 1 张宣传图）
STORE_LISTING.md      # CWS 商店详情页文案
```

---

## 隐私

- 截图只发往你在设置里配置的 endpoint（默认火山方舟）
- API Key 只存在本地 `chrome.storage.local`，扩展不上传、不收集、不分析任何浏览数据
- 完整隐私政策：<https://zzf-love.github.io/DOUBAO-Chrome-extension/privacy.html>

---

## 版本

- **v1.3.7**：去抖只保护全屏回退路径，正常网页框选恢复"秒开"（v1.3.6 误把正常路径也卡了 1 秒）；浮动面板 / 全屏窗口的 Dark 主题顶栏改为深色渐变，跟 popup 一致
- **v1.3.6**：注入失败 / 截图失败时强制弹出结果窗口显示具体原因，避免用户以为按了没反应反复重按；Alt+S 1 秒去抖防止 Chrome 截图频率上限；`captureVisibleTab` 不再依赖可能失效的 `tab.windowId`
- **v1.3.5**：浮动解读面板（content.js）和 PDF 全屏窗口（result.html）现在跟随 popup 的皮肤设置，全局换肤一气呵成；移除 Mono 皮肤，保留 Aurora / Dark / Sakura 三套
- **v1.3.4**：popup 提示区加"自定义"链接，一键跳转 `chrome://extensions/shortcuts` 自行设置快捷键（解决主备两键都冲突的极端场景）
- **v1.3.3**：备用快捷键 `Alt+Shift+S` 显示在 popup 提示区，用户不再依赖 hover tooltip 才能发现
- **v1.3.2**：双快捷键共存——`Alt+S` 主键 + `Alt+Shift+S` 备用键（避免 `Alt+S` 在某些浏览器/网页上无法自动绑定时彻底失灵）
- **v1.3.1**：PDF / chrome:// 等不可注入页面回退到"全屏模式"——自动捕获整页并在弹窗里给 AI 解读；4 套皮肤切换（Aurora / Dark / Sakura / Mono）；Prompt 模板扩到 6 个内置 + 3 个自定义槽；"视觉解析"替换"反推提示词"，输出对所有 AI 绘图工具通用；高级设置（模型/Endpoint）折叠
- **v1.2.0**：i18n（中/英双语自动切换 — 中文名"AI 截图解读"、英文名"AI Screenshot Explainer"）；移除 `<all_urls>` 静态 `content_scripts`，改为 `activeTab` 动态注入（缩窄权限范围、加快审核）
- **v1.1.2**：缩短 manifest description 至 132 字以内（CWS 上传要求）
- **v1.1.1**：浮动面板"关闭"按钮加宽到 48px，更易点击
- **v1.1.0**：产品化（添加图标、移除硬编码 Key、收窄 host 权限、生成隐私政策页）
- **v1.0**：初版，Doubao Seed 2.0 Responses API + Alt+S 框选

## 许可

MIT

## 反馈 / Bug

[GitHub Issues](https://github.com/zzf-love/DOUBAO-Chrome-extension/issues)

# 安装指南 · AI 截图解读

> 没有 VPN、不想等 Chrome 应用商店审核也能用。全程 3 分钟。

---

## 你需要准备的东西

| 项目 | 说明 |
|---|---|
| **Chrome 浏览器** | 或基于 Chromium 的：Edge、Arc、Brave、360 极速、QQ 浏览器都行 |
| **火山方舟 API Key** | 免费额度足够个人使用，下面教怎么领 |
| **3 分钟时间** | 真的不多 |

---

## 第一步：下载插件包

下载 `ai-screenshot-explainer-v1.2.0.zip`。三个渠道（按速度排序）：

- **蓝奏云**：[待补充链接]
- **百度网盘**：[待补充链接]
- **GitHub Release**：<https://github.com/zzf-love/DOUBAO-Chrome-extension/releases/latest>（无 VPN 可能很慢）

下载完**不要解压**，保持 .zip 状态放在桌面或任意位置。

> 等等！其实需要解压一次。Chrome 加载的不是 zip 文件，是解压后的文件夹。把 zip **解压到一个固定位置**（比如 `D:\Tools\ai-explainer\`），后面要一直保留这个文件夹，删掉就用不了了。

---

## 第二步：开发者模式安装

1. 浏览器地址栏输入：`chrome://extensions/` 回车
2. 页面**右上角**打开 **"开发者模式"** 开关
3. 页面左上角出现三个按钮，点 **"加载已解压的扩展程序"**
4. 弹窗里选刚才解压出的那个文件夹（包含 `manifest.json` 那一层）
5. 加载成功后插件就出现在列表里了 ✅

> Edge 浏览器：开关位置在**页面左下角**，文字叫"开发人员模式"，其他都一样。

把扩展图标固定到工具栏：点浏览器右上角的拼图图标 → 找到 "AI 截图解读" → 点旁边的图钉，让它常驻。

---

## 第三步：申请火山方舟 API Key

1. 访问 <https://www.volcengine.com/product/ark>
2. 用手机号注册 / 登录
3. 实名认证（个人，免费）
4. 进入 **"在线推理 → API 调用"** 页面
5. 点 **"创建 API Key"**，复制出来的字符串（以 `ark-` 开头）

> 💡 火山方舟新用户有免费 token 额度，单次截图大概消耗 1k-5k token，免费额度够用很久。

---

## 第四步：配置插件

1. 点工具栏上的插件图标，弹出设置框
2. **API Key** 框填刚才复制的 `ark-xxxxx`
3. 其他三个字段（模型、Endpoint、默认 Prompt）**保持默认**即可
4. 点 **"保存"**，看到绿色 "已保存" 字样就 OK

---

## 第五步：试用一下

1. 打开任何一个网页（推荐先试这个：<https://en.wikipedia.org/wiki/Special:Random>，随机维基百科）
2. 按下快捷键 **`Alt + S`**（Mac 也是 Alt+S）
3. 屏幕变暗，鼠标变成十字光标
4. 按住左键，**拖拽框选**你想问 AI 的那块区域，松开
5. 等几秒钟，右上角浮动面板出现解读结果 🎉

不想用快捷键？**两个备选触发方式**：
- 点工具栏插件图标（前提是已经填过 Key 了）
- 在网页上**右键** → 选 **"用 AI 解读这块区域"**

---

## 常见问题

### Q：按 Alt+S 没反应？

A：可能是快捷键被其他扩展占用。打开 `chrome://extensions/shortcuts/`，找到 "AI 截图解读"，重新设置一个不冲突的快捷键。

### Q：浮动面板显示 "API ... 401" 或 "API Key 无效"？

A：Key 填错或失效。点插件图标重新填入正确的 `ark-xxxxx`。

### Q：浮动面板显示 "API 429"？

A：触发了火山方舟的免费速率限制，等一分钟再试。重度使用可在火山控制台充值开通付费额度（按 token 用量计费，几块钱能用很久）。

### Q：解读结果不准 / 想用别的模型？

A：插件弹窗里改 **模型** 字段。火山方舟支持的视觉模型 ID 在 [火山引擎文档](https://www.volcengine.com/docs/82379) 查。也可以改 **Endpoint** 接其他兼容 OpenAI Responses API 的服务。

### Q：在 `chrome://`、`edge://`、新标签页没反应？

A：浏览器禁止扩展在系统页面运行，正常现象。打开任意普通网页（http/https）就能用。

### Q：能在 PDF 上用吗？

A：浏览器自带 PDF 阅读器是用 `<embed>` 渲染的，截图能截到，但鼠标框选可能被 PDF 自身拦截。建议用 Chrome 自带 PDF 查看器试试，不行的话先把 PDF 截图保存到桌面再上传给豆包。

### Q：截图会被上传到哪里？

A：截图直接从你的浏览器 POST 到你配置的 Endpoint（默认是火山方舟 `ark.cn-beijing.volces.com`），**不经过插件作者的任何服务器**，作者看不到你的截图。完整隐私政策：<https://zzf-love.github.io/DOUBAO-Chrome-extension/privacy.html>

### Q：怎么卸载？

A：`chrome://extensions/` 找到这个扩展，点 "移除"。本地 `chrome.storage.local` 里的 API Key 和设置会一并清除。

---

## 反馈 / 提 Bug / 建议

- **GitHub Issues**：<https://github.com/zzf-love/DOUBAO-Chrome-extension/issues>
- **小红书**：评论区留言 / 私信

如果你帮我点了 Star ⭐ 或转发，会很开心 🙏

<div align="center">
  <h1>Browser Auto Test Skills</h1>
  <p>
    <a href="https://github.com/zhou0928/browser-auto-test/stargazers"><img src="https://img.shields.io/github/stars/zhou0928/browser-auto-test?style=social" alt="GitHub Stars"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  </p>
  <p>
    <strong>让 AI 打开看得见的浏览器，像真人一样帮你测网页。</strong><br>
    AI-driven browser automated testing — visible, interactive, human-like.<br>
    Compatible with Claude Code, OpenCode, Cursor, Gemini CLI, and any tool-calling AI agent.
  </p>
</div>

---

<details>
<summary><b>🌐 中文 (Chinese)</b></summary>

# Browser Auto Test Skills

一个 AI 编程助手的 skill 集合，让 AI 能够打开真实的 Chrome 浏览器，像人类一样点击、填写表单、截图、检查控制台报错和网络请求。**最主要的特点是"看得见"**——Chrome 窗口会弹出来，你可以实时观察 AI 的每一步操作，而不是在黑盒里跑。

## 适用场景

| 场景 | 说明 |
|------|------|
| **探索式测试** | AI 自动遍历页面上所有可交互元素，点击每个链接/按钮/表单，检查有无报错 |
| **回归测试** | 按测试计划（Markdown 用例）逐条执行，截图留证，对比预期结果 |
| **表单验证** | 填写各种表单，测试正常提交、空提交、非法输入 |
| **UI 走查** | 快速过一遍页面所有功能，检查控制台错误和网络请求异常 |
| **CI / 夜间跑** | 切换到 Playwright 无头模式，集成到 CI 流水线 |

## 工作原理

```
       你说"测一下"
             │
             ▼
 ┌─────────────────────────────┐
 │ Chrome 是否在 9222 端口运行？ │
 │ 没有 → 自动启动 Chrome，      │
 │        开启 remote-debugging  │
 └──────────┬──────────────────┘
            │
            ▼
 ┌─────────────────────────────┐
 │ AI 通过 Chrome DevTools 协议  │
 │ 操控浏览器                    │
 └──────────┬──────────────────┘
            │
            ▼
 ┌─────────────────────────────┐
 │ 每次交互：                    │
 │                              │
 │ ① take_snapshot()            │
 │   获取页面 accessibility 树   │
 │   找到所有可交互元素及其 uid  │
 │                              │
 │ ② hover → 确认目标           │
 │   像人一样先悬停再点击        │
 │                              │
 │ ③ click / fill / navigate    │
 │   执行实际操作                │
 │                              │
 │ ④ 等待页面响应 (1-2s)        │
 │                              │
 │ ⑤ list_console_messages()    │
 │   检查有无 JS 报错            │
 │                              │
 │ ⑥ list_network_requests()    │
 │   检查接口有无 4xx/5xx        │
 │                              │
 │ ⑦ take_screenshot()           │
 │   截图留证                    │
 └──────────┬──────────────────┘
            │
            ▼
 ┌─────────────────────────────┐
 │ 输出测试结果：                │
 │ • 每个操作的截图              │
 │ • console error 列表         │
 │ • 网络异常请求列表            │
 │ • 测试用例通过/失败统计       │
 └─────────────────────────────┘
```

## 两种模式

### 模式一：可见模式（默认）

AI 会打开一个 Chrome 窗口，所有操作实时可见。适合日常开发调试、探索式测试。

**优点：**
- 测试过程透明，你看着 AI 操作，随时可以干预
- 能看到页面实际渲染效果
- 调试方便，控制台报错一目了然

**触发方式：** 直接说"测一下"或"测试这个页面"

### 模式二：无头模式

使用 Playwright 无头浏览器，不显示窗口。适合 CI 流水线、夜间自动跑。

**优点：**
- 不占用桌面，适合服务器环境
- 运行速度更快
- 适合集成到 GitHub Actions / Jenkins

**触发方式：** 说"后台跑"或"headless mode"

## 测试计划驱动

你可以编写结构化的测试用例文件，让 AI 按用例逐条执行：

```markdown
# 订单测试

## TC-01: 正常创建订单
| 前置条件 | 操作步骤 | 预期结果 |
|---------|---------|---------|
| 已登录 | 1. 点击"新建订单" | 弹出新建页面 |
| 商品库存充足 | 2. 选择商品 A x 2 | 金额自动计算 |
|           | 3. 点击"提交" | 提示"创建成功" |
|           | 4. 检查控制台 | 无 error |
```

然后说：**"跑一下 订单测试.md"**

AI 会：
1. 读取表格，解析前置条件、操作步骤、预期结果
2. 按顺序执行每一步
3. 每步截图 + 检查 console + 检查网络
4. 对比实际结果和预期结果
5. 输出测试报告（通过/失败 + 证据截图）

## 内置 Skill

| Skill | 目录 | 说明 |
|-------|------|------|
| browser-auto-test | [browser-auto-test/](browser-auto-test/) | 浏览器自动化测试核心 skill |

每个 skill 包含：
- `SKILL.md` — skill 定义，AI 代理读取的工作流说明
- `scripts/` — 辅助脚本
- `{name}.zip` — 可分发的安装包

## 安装

### Claude Code

```bash
# 方法一：直接复制
cp -r browser-auto-test ~/.claude/skills/

# 方法二：从 GitHub 克隆
git clone https://github.com/zhou0928/browser-auto-test.git
ln -s $(pwd)/browser-auto-test/browser-auto-test ~/.claude/skills/browser-auto-test
```

### OpenCode

```bash
cp -r browser-auto-test ~/.config/opencode/skills/
```

### Cursor

把 `browser-auto-test/SKILL.md` 复制到项目根目录的 `.cursor/rules/` 下，或直接在 Cursor 的 Rules 配置中引用。

### Gemini CLI

```bash
gemini skills install https://github.com/zhou0928/browser-auto-test.git
```

### GitHub Copilot

在 `.github/copilot-instructions.md` 中引用 SKILL.md 的内容，或直接复制到项目 instructions 中。

### 验证安装

对你的 AI 助手说"测一下"，如果它自动打开 Chrome 开始测试，说明安装成功。

## 快速开始

### 场景 1：随便测测一个页面

```
你：测一下这个页面
AI：好的，请告诉我 URL
你：http://localhost:5173
AI：[打开 Chrome → 截图 → 开始点击每个元素 → 检查报错 → 输出报告]
```

### 场景 2：按测试计划跑

```
你：跑一下 登录测试.md
AI：[读取用例 → 按步骤执行 → 截图 → 输出通过/失败]
```

### 场景 3：特定功能验证

```
你：帮我测一下这个表单的校验逻辑
AI：好的，我开始填表单：
    1. 不填任何字段点提交 → 截图验证错误提示
    2. 只填用户名点提交 → 截图
    3. 填全部字段点提交 → 截图
    4. 检查所有报错
```

### 场景 4：CI 集成

```yaml
# .github/workflows/test.yml
steps:
  - uses: actions/checkout@v4
  - name: Install skill
    run: |
      git clone https://github.com/zhou0928/browser-auto-test.git
  - name: Run tests
    run: |
      # 启动应用，AI 切换到 headless 模式跑测试
```

## API 参考

所有操作通过 `chrome-devtools_*` 工具执行（可见模式）或 Playwright（无头模式）。

### 导航

| 操作 | 命令 | 说明 |
|------|------|------|
| 打开 URL | `navigate_page(type="url", url=...)` | 导航到指定地址 |
| 刷新 | `navigate_page(type="reload")` | 刷新当前页面 |
| 后退 | `navigate_page(type="back")` | 历史后退 |
| 前进 | `navigate_page(type="forward")` | 历史前进 |

### 页面结构

| 操作 | 命令 | 说明 |
|------|------|------|
| 获取结构 | `take_snapshot()` | 获取 accessibility 树，所有可交互元素及 uid |
| 保存到文件 | `take_snapshot(filePath=...)` | 页面很大时保存到文件 |
| 详情模式 | `take_snapshot(verbose=true)` | 包含所有可用信息 |
| 等待内容 | `wait_for(text=["..."])` | 等待文本出现 |

### 点击与悬停

| 操作 | 命令 | 说明 |
|------|------|------|
| 点击 | `click(uid="ref_xxx")` | 点击元素 |
| 双击 | `click(uid="ref_xxx", dblClick=true)` | 双击 |
| 点击+快照 | `click(uid="ref_xxx", includeSnapshot=true)` | 点击后立刻获取新结构 |
| 悬停 | `hover(uid="ref_xxx")` | 鼠标悬停 |

### 表单操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 批量填表 | `fill_form(elements=[{uid, value}, ...])` | 一次填多个字段，推荐 |
| 单个输入 | `fill(uid="ref_xxx", value="hello")` | 填单个输入框 |
| 键盘输入 | `type_text(text="hello")` | 逐字输入 |
| 提交输入 | `type_text(text="hello", submit=true)` | 输入后按 Enter |
| 键盘按键 | `press_key(key="Enter")` | 按键盘 |
| 组合键 | `press_key(key="Control+A")` | 快捷键 |
| 下拉选择 | `select_option(target="ref_xxx", values=["option1"])` | 选择下拉选项 |

### 截图

| 操作 | 命令 | 说明 |
|------|------|------|
| 截可视区 | `take_screenshot()` | 默认当前可视区域 |
| 截全页 | `take_screenshot(fullPage=true)` | 整个页面 |
| 截元素 | `take_screenshot(uid="ref_xxx")` | 特定元素 |
| 存文件 | `take_screenshot(filePath="...")` | 保存到指定路径 |
| 调整质量 | `take_screenshot(type="jpeg", quality=80)` | JPEG 格式，可调质量 |
| 高清截图 | `take_screenshot(scale="device")` | 设备像素截图 |

### 控制台与网络

| 操作 | 命令 | 说明 |
|------|------|------|
| 检查错误 | `list_console_messages(types=["error"])` | 只看 error |
| 检查警告 | `list_console_messages(types=["error","warn"])` | error + warn |
| 看全部 | `list_console_messages()` | 所有日志 |
| 看详情 | `get_console_message(msgid=0)` | 某条日志详情 |
| API 请求 | `list_network_requests(resourceTypes=["xhr","fetch"])` | 只看 XHR/fetch |
| 页面请求 | `list_network_requests(resourceTypes=["document"])` | 页面导航请求 |
| 请求详情 | `get_network_request(reqid=3)` | 查看请求/响应头、体 |
| 保存响应 | `get_network_request(reqid=3, responseFilePath="...")` | 保存响应体到文件 |

### 弹窗处理

| 操作 | 命令 | 说明 |
|------|------|------|
| 确定 | `handle_dialog(action="accept")` | 接受弹窗 |
| 取消 | `handle_dialog(action="dismiss")` | 取消弹窗 |
| 输入 | `handle_dialog(action="accept", promptText="hello")` | prompt 输入文字 |

### 标签页管理

| 操作 | 命令 | 说明 |
|------|------|------|
| 列出标签 | `list_pages()` | 列出所有标签页 |
| 切换标签 | `select_page(pageId=0)` | 按 ID 选择标签 |
| 新标签 | `new_page(url="https://example.com")` | 打开新标签页 |
| 关闭标签 | `close_page(pageId=1)` | 关闭标签 |
| 调窗口 | `resize_page(width=1920, height=1080)` | 调整窗口大小 |

### 文件上传

| 操作 | 命令 | 说明 |
|------|------|------|
| 上传文件 | `upload_file(uid="ref_xxx", filePath="/path/to/file.pdf")` | 上传文件到 input |

### 模拟

| 操作 | 命令 | 说明 |
|------|------|------|
| 模拟网速 | `emulate(networkConditions="Slow 3G")` | 弱网测试 |
| 模拟设备 | `emulate(viewport="375x812x3,mobile,touch")` | iPhone X 视口 |
| 暗色模式 | `emulate(colorScheme="dark")` | 暗色主题 |
| 亮色模式 | `emulate(colorScheme="light")` | 亮色主题 |
| 模拟定位 | `emulate(geolocation="37.7749,-122.4194")` | 模拟 GPS |
| 用户代理 | `emulate(userAgent="...")` | 自定义 UA |
| CPU 降频 | `emulate(cpuThrottlingRate=4)` | CPU 节流倍率 |

### JavaScript 执行

| 操作 | 命令 | 说明 |
|------|------|------|
| 获取标题 | `evaluate_script(function="() => document.title")` | 页面标题 |
| 获取文本 | `evaluate_script(function="(el) => el.textContent", args=["ref_xxx"])` | 元素文本 |
| 获取尺寸 | `evaluate_script(function="() => window.innerWidth")` | 窗口宽度 |
| 检查状态 | `evaluate_script(function="() => document.querySelector('.error')?.textContent")` | 错误信息 |

### 性能审计

| 操作 | 命令 | 说明 |
|------|------|------|
| LH 审计 | `lighthouse_audit(mode="navigation")` | Lighthouse 性能报告 |
| 快照审计 | `lighthouse_audit(mode="snapshot")` | 当前状态快照审计 |

## 探索式测试详情

### 工作流

当你说"测一下"时，AI 进入探索式测试循环：

```
循环体：
 ① take_snapshot()
    获取页面上所有可交互元素（按钮、链接、输入框、下拉框……）
    每个元素有一个唯一 uid

 ② take_screenshot()
    截当前画面，作为"操作前"证据

 ③ list_console_messages(types=["error"])
    检查当前页面上有没有新产生的 JS 错误

 ④ 元素优先级选择
    从没点过的元素中，按优先级选最高级的

 ⑤ 执行交互
    hover → wait 500ms → click → wait 1-2s

 ⑥ 操作后检查
    list_console_messages(types=["error"])    → 有没有新的报错
    list_network_requests(xhr/fetch)           → 有没有 4xx/5xx
    take_screenshot()                          → "操作后"证据

 ⑦ 判断页面是否变化
    如果变了 → 回到 ① 重新扫描
    如果没变 → 回到 ④ 点下一个元素
```

### 元素优先级表

AI 优先点击更重要的元素：

| 优先级 | 元素类型 | 说明 |
|--------|---------|------|
| P0 🔴 | 链接、Tab、菜单项 | 导航类，改变页面状态 |
| P1 🟠 | 按钮（提交/保存/删除） | 触发关键操作 |
| P2 🟡 | 输入框、开关、复选框 | 数据输入类 |
| P3 🟢 | 下拉框、滑块、日期选择器 | 较复杂的交互 |
| P4 🔵 | 模态框关闭按钮 × | 关闭弹窗 |
| P5 ⚪ | 分页、排序 | 列表操作 |

### 异常处理矩阵

| 现象 | 处理方式 | 是否继续 |
|------|---------|---------|
| Console 有 error | 截图 + 记录错误详情 | ✅ 继续 |
| API 返回 4xx | 截图 + 记录 URL + 状态码 | ✅ 继续 |
| API 返回 5xx | 截图 + 记录 | ✅ 继续 |
| 页面白屏 | 截图 + 记录当前 URL | ⏹ 停止当前路径 |
| 弹出 alert/confirm | 截图弹窗 → dismiss 关掉 | ✅ 继续 |
| 点击后没反应 | 跳过该元素，标记不可交互 | ✅ 继续 |
| 页面跳转了 | 重新扫描新页面结构 | ✅ 继续探索 |

## 常见问题

### Q: 需要提前安装 Chrome 吗？

是的，需要安装 Google Chrome。如果 9222 端口没有 Chrome 运行，AI 会自动启动一个。

### Q: 和 Playwright / Cypress 有什么区别？

Playwright 和 Cypress 是编程框架，需要你写代码脚本。这个 skill 是让 AI 代你操作浏览器——你说需求，AI 执行，零编码。

### Q: 可以在 CI 里用吗？

可以。切换到 headless 模式（说"后台跑"）即可在无 GUI 环境运行。

### Q: Mac 上总是弹 Chrome 窗口？

可见模式就是故意弹窗口的，让你看着 AI 操作。不想看窗口就说"后台跑"。

### Q: 支持多标签页吗？

支持。AI 可以打开新标签、切换标签、关闭标签，就像你手动操作一样。

### Q: 能测移动端页面吗？

可以。使用 `emulate(viewport="375x812x3,mobile,touch")` 模拟移动端视口。

## 开发计划

- [ ] 添加更多 demo 截图到 README
- [ ] 示例测试计划模板
- [ ] GitHub Actions CI 集成示例
- [ ] 多语言 skill 支持

## 目录结构

```
browser-auto-test/
├── README.md
├── LICENSE
└── browser-auto-test/              ← browser-auto-test skill
    ├── SKILL.md                    ←   AI 代理读取的 skill 定义
    ├── scripts/
    │   ├── test_env.py             ←   本地开发服务器启动脚本
    │   └── snapshot_diff.py        ←   截图对比脚本 (ImageMagick)
    └── browser-auto-test.zip       ←   可分发的 skill 安装包
```

## 贡献

欢迎 PR！如果是新功能或新 skill，请先开 issue 讨论。

## License

MIT

---

</details>

<details>
<summary><b>🇬🇧 English</b></summary>

# Browser Auto Test Skills

A collection of AI agent skills for browser automated testing. The AI opens a real Chrome window and interacts with web pages like a human — clicking, filling forms, taking screenshots, checking console errors, and inspecting network requests. **The key difference: you can see everything.** The Chrome window pops up and you watch the AI work in real time.

## When to Use

| Scenario | Description |
|----------|-------------|
| **Exploratory testing** | AI systematically clicks every link, button, and form on a page, checking for errors |
| **Regression testing** | Execute structured test plans (Markdown format), capture evidence, compare results |
| **Form validation** | Test form submission with valid/invalid/empty inputs |
| **UI walkthrough** | Quick scan through all page features, checking console and network health |
| **CI / Nightly runs** | Switch to Playwright headless mode, integrate into CI pipelines |

## How It Works

```
      You say "test this"
             │
             ▼
 ┌─────────────────────────────────┐
 │ Check Chrome on port 9222       │
 │ Not running → auto-launch with  │
 │       --remote-debugging-port   │
 └──────────┬──────────────────────┘
            │
            ▼
 ┌─────────────────────────────────┐
 │ AI drives browser via CDP       │
 └──────────┬──────────────────────┘
            │
            ▼
 ┌─────────────────────────────────┐
 │ Per interaction:                 │
 │ ① take_snapshot()                │
 │ ② hover → confirm target         │
 │ ③ click / fill / navigate        │
 │ ④ wait (1-2s)                    │
 │ ⑤ check console errors           │
 │ ⑥ check network requests         │
 │ ⑦ take_screenshot()              │
 └──────────┬──────────────────────┘
            │
            ▼
 ┌─────────────────────────────────┐
 │ Report: screenshots + errors    │
 │         + pass/fail summary     │
 └─────────────────────────────────┘
```

## Quick Start

```bash
# Install
cp -r browser-auto-test ~/.claude/skills/

# Or with OpenCode
cp -r browser-auto-test ~/.config/opencode/skills/

# Or with Gemini CLI
gemini skills install https://github.com/zhou0928/browser-auto-test.git
```

Tell your AI agent:

> **"Test this page"** — opens Chrome, starts exploratory testing

> **"Run login.md"** — executes structured test cases from a file

> **"Headless mode"** — switches to Playwright headless

## Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| browser-auto-test | [browser-auto-test/](browser-auto-test/) | Core browser automation skill — visible Chrome or headless Playwright |

## Repository Structure

```
browser-auto-test/
├── README.md
├── LICENSE
└── browser-auto-test/
    ├── SKILL.md
    ├── scripts/
    │   ├── test_env.py
    │   └── snapshot_diff.py
    └── browser-auto-test.zip
```

## License

MIT

</details>

---

<p align="center"><em>Built for AI agents who deserve a browser they can actually see.</em></p>

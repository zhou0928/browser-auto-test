# Browser Auto Test

> **让 AI 帮你跑浏览器测试，你看着它点 — 跟真人操作一样。**

[English](#english) · [中文](#中文)

---

<a id="中文"></a>

# 中文文档

AI 编程助手（Claude Code、OpenCode、Cursor、Gemini CLI）的浏览器自动化测试 skill。打开一个看得见的 Chrome 窗口，AI 像真人一样点击、填表单、截图、检查报错，你在旁边看着它操作。

> 说一句 **"测一下"**，AI 自动打开 Chrome 开始测试。

---

## 特性

- **👁️ 默认可见模式** — Chrome 窗口弹出，你看着 AI 操作，不是黑盒跑
- **🤖 类人操作** — 先 snapshot 看结构 → hover 确认 → 点击 → 等待 → 检查结果
- **🔍 探索式测试** — AI 自动点遍每个链接/按钮/表单，每步检查 console error
- **📸 截图留证** — 关键步骤自动截图，可追溯
- **🕸️ 网络感知** — 每次交互后自动检查 XHR/fetch 有无 4xx/5xx
- **📝 测试计划驱动** — 按结构化 Markdown 用例执行，前置条件/步骤/预期结果一目了然
- **🎭 支持无头模式** — 说"后台跑"切换到 Playwright 无头模式，适合 CI
- **🔌 零配置** — 自动检测 Chrome 9222 端口，没有就自动启动

---

## 工作原理

```
        你说 "测一下"
              │
              ▼
 ┌───────────────────────────────┐
 │  Chrome 是否运行在 9222 端口  │
 │  没有 → 自动启动 Chrome 并     │
 │         开启 remote-debugging  │
 └───────────┬───────────────────┘
             │
             ▼
 ┌───────────────────────────────┐
 │  AI 通过 Chrome DevTools       │
 │  协议操控浏览器                │
 └───────────┬───────────────────┘
             │
             ▼
 ┌───────────────────────────────┐
 │  每次交互：                    │
 │  ① snapshot → 获取页面结构     │
 │  ② hover    → 确认目标元素    │
 │  ③ click / fill / navigate    │
 │  ④ 等待页面响应               │
 │  ⑤ 检查 console error         │
 │  ⑥ 检查网络请求               │
 │  ⑦ 截图留证                   │
 └───────────┬───────────────────┘
             │
             ▼
 ┌───────────────────────────────┐
 │  输出测试报告（截图 + 日志）    │
 └───────────────────────────────┘
```

---

## 安装

### Claude Code

```bash
cp -r browser-auto-test ~/.claude/skills/
```

### OpenCode

```bash
cp -r browser-auto-test ~/.config/opencode/skills/
```

### Cursor

把 `SKILL.md` 复制到 `.cursor/rules/` 目录下。

### Gemini CLI

```bash
gemini skills install https://github.com/zhou0928/browser-auto-test.git
```

### 其他 AI 工具

Skill 就是纯 Markdown 文件，把 `SKILL.md` 加到你的系统提示词或指令文件中即可。

---

## 快速开始

### 1. 交互模式（可见浏览器）

对你的 AI 编程助手说：

> **"测一下这个页面"**

AI 会：
1. 打开/连接 Chrome（会弹出窗口，端口 9222）
2. 问你要测哪个 URL
3. 获取页面结构（snapshot）
4. 开始点击元素、填表单、跳转页面
5. 每步检查 console error 和网络请求
6. 输出测试结果，附带截图

### 2. 按测试计划跑

创建测试用例文件，比如 `login.md`：

```markdown
# 登录测试

## TC-01: 正常登录
| 前置条件 | 操作步骤 | 预期结果 |
|---------|---------|---------|
| 已打开登录页 | 1. 输入用户名 admin | 登录成功 |
|            | 2. 输入密码 123456 | 跳转首页 |
|            | 3. 点击登录按钮 | 无控制台报错 |
```

然后说：

> **"跑一下 login.md"**

### 3. 无头模式（不弹窗口）

> **"后台跑一下这个测试"**

切换为 Playwright 无头浏览器，操作逻辑完全相同，但不显示 Chrome 窗口。

---

## API 参考

| 操作 | 工具 | 说明 |
|------|------|------|
| 导航 | `navigate_page(type="url", url=...)` | 打开 URL |
| 刷新 | `navigate_page(type="reload")` | 刷新页面 |
| 后退 | `navigate_page(type="back")` | 后退 |
| 结构 | `take_snapshot()` | 获取 accessibility 树 |
| 截图 | `take_screenshot()` | 截当前可视区域 |
| 全页截图 | `take_screenshot(fullPage=true)` | 截完整页面 |
| 元素截图 | `take_screenshot(uid="...")` | 截特定元素 |
| 点击 | `click(uid="...")` | 点击元素 |
| 双击 | `click(uid="...", dblClick=true)` | 双击 |
| 悬停 | `hover(uid="...")` | 鼠标悬停 |
| 批量填表 | `fill_form(elements=[...])` | 一次填多个字段 |
| 填输入框 | `fill(uid="...", value="...")` | 单个输入 |
| 键盘输入 | `type_text(text="...")` | 逐字输入 |
| 按键 | `press_key(key="Enter")` | 键盘按键 |
| 执行 JS | `evaluate_script(function="...")` | 运行 JavaScript |
| 控制台错误 | `list_console_messages(types=["error"])` | 检查报错 |
| 网络请求 | `list_network_requests(resourceTypes=["xhr","fetch"])` | 检查 API |
| 请求详情 | `get_network_request(reqid=3)` | 查看完整请求 |
| 弹窗 | `handle_dialog(action="accept"/"dismiss")` | 处理弹窗 |
| 拖拽 | `drag(from_uid="...", to_uid="...")` | 拖拽元素 |
| 调窗口 | `resize_page(width=1920, height=1080)` | 改分辨率 |
| 标签管理 | `list_pages()` / `select_page(pageId=0)` | 多标签页 |
| 新标签 | `new_page(url="...")` | 打开新标签 |
| 关标签 | `close_page(pageId=1)` | 关闭标签 |
| 文件上传 | `upload_file(uid="...", filePath="...")` | 上传文件 |

---

## 探索式测试

AI 执行以下循环进行无固定脚本的探索式测试：

```
循环：
  ① take_snapshot()              → 获取所有可交互元素
  ② take_screenshot()            → 截当前画面
  ③ list_console_messages(error) → 检查报错
  ④ 按优先级选一个没点过的元素
  ⑤ hover → 等 0.5s → click → 等 1-2s
  ⑥ 操作后检查
  ⑦ 页面变了 → 重新扫描
```

### 元素优先级

| 优先级 | 元素 |
|--------|------|
| P0 | 链接、Tab、菜单项 |
| P1 | 按钮（提交/保存/删除） |
| P2 | 输入框、开关、复选框 |
| P3 | 下拉框、滑块、日期选择器 |
| P4 | 模态框关闭按钮 × |
| P5 | 分页、排序 |

### 操作后检查

```
1. 等 1-2 秒让页面响应
2. list_console_messages(types=["error"])
3. list_network_requests(resourceTypes=["xhr","fetch"])
4. take_screenshot() → 保存证据
```

### 异常处理

| 现象 | 处理 |
|------|------|
| 控制台有 error | 截图 + 记录，继续 |
| API 4xx/5xx | 截图 + 记录，继续 |
| 白屏 | 截图 + 记录 URL |
| 弹窗 | 截图弹窗 → 关掉 |
| 点了没反应 | 跳过，继续下一个 |
| 页面变了 | 重新扫描 |

---

## 测试计划格式

测试计划用 Markdown 表格写用例：

```markdown
# 页面名称

## TC-01: 测试用例描述
| 前置条件 | 操作步骤 | 预期结果 |
|---------|---------|---------|
| 条件1    | 1. 步骤1 | 结果1    |
| 条件2    | 2. 步骤2 | 结果2    |

## TC-02: 另一个用例
...
```

每张表格 3 列：**前置条件**、**操作步骤**、**预期结果**。

---

## 辅助脚本

### `test-env.sh`

启动本地开发服务器，等待端口就绪：

```bash
bash scripts/test-env.sh                  # 默认 5173 端口
bash scripts/test-env.sh 3000             # 自定义端口
bash scripts/test-env.sh 8080 "npm start" # 自定义命令
```

### `snapshot-diff.sh`

对比两张截图（基于 ImageMagick）：

```bash
bash scripts/snapshot-diff.sh baseline.png current.png diff.png
```

---

## 环境要求

- Google Chrome
- macOS / Linux（Windows 用 WSL）
- 支持工具调用的 AI 编程助手（Claude Code、OpenCode、Cursor 等）

---

## License

MIT

---

<a id="english"></a>

# English

*This section is a compact reference. See the [Chinese version](#中文) above for full documentation.*

**Browser Auto Test** — An AI agent skill for visible, interactive browser testing. The AI opens a real Chrome window and performs clicks, form fills, and navigation while you watch.

### Install

```bash
# Claude Code
cp -r browser-auto-test ~/.claude/skills/

# OpenCode
cp -r browser-auto-test ~/.config/opencode/skills/

# Gemini CLI
gemini skills install https://github.com/zhou0928/browser-auto-test.git
```

### Usage

- **"Test this page"** → AI opens Chrome, starts exploratory testing
- **"Run login.md"** → AI executes structured test cases from file
- **"Headless mode"** → Switch to Playwright headless for CI

### Key Features

- Visible Chrome window — not headless, you see every interaction
- Snapshot-first approach: get accessibility tree before clicking
- Automatic console error & network check after every action
- Exploratory testing: systematically click all elements, report failures
- Test plan driven: structured Markdown test cases with pass/fail reporting
- Headless fallback for CI pipelines

### API Operations

Navigate, snapshot, click, hover, fill forms, screenshot, execute JS, check console/network, handle dialogs, keyboard, tabs, file upload, emulation — all via Chrome DevTools Protocol.

### Scripts

- `test-env.sh` — start dev server and wait for ready
- `snapshot-diff.sh` — ImageMagick screenshot comparison

### Requirements

Chrome, macOS/Linux, AI agent with tool-calling support. MIT license.

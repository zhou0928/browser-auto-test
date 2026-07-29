---
name: browser-auto-test
description: "Browser automated testing with a visible Chrome window — the AI drives a real browser and you watch every interaction in real time. Uses Chrome DevTools Protocol (CDP) for visible mode, Playwright for headless/CI mode. Use when: running exploratory tests on web apps, clicking every element systematically, filling and submitting forms, checking console errors and network requests, capturing screenshots, automating multi-step test workflows from structured test plans. Supports both interactive (visible) and headless modes. Triggers: '测一下', '测试', '跑测试', '点一点', '探索测试', '人工测试', '打开浏览器', '跑一下', 'check this page', 'test this', 'exploratory test', 'browser test', 'automated test', 'run tests'."
---

# Browser Auto Test

浏览器自动化测试 skill。AI 打开可见的 Chrome 窗口，像真人一样点击、填表单、截图、检查报错，你在旁边看着它操作。

---

## 工作模式

### 模式一：可见模式（默认）

AI 自动检测 Chrome 9222 端口，没有就自动启动 `--remote-debugging-port=9222`。浏览器窗口会弹出来，所有操作实时可见。

### 模式二：无头模式

说 **"后台跑"** 或 **"headless mode"** 切换到 Playwright 无头浏览器。操作逻辑完全一样，但不弹窗口，适合 CI。

---

## 核心原则

1. **Snapshot 优先** — 任何交互前先 `take_snapshot()` 获取页面结构和元素 uid
2. **先 hover 再 click** — 模拟真人操作轨迹
3. **批量填表单** — 用 `fill_form()` 一次提交多个字段
4. **操作后必检查** — console error + 网络异常 + 页面状态变化
5. **截图留证** — 关键步骤后截图，可追溯
6. **网络感知** — 表单提交后检查 XHR/fetch 有无 4xx/5xx

---

## 快速开始

```
1. navigate_page(type="url", url="<target-url>")  → 打开页面
2. take_snapshot()                                  → 获取页面结构
3. click / fill / hover                             → 交互操作
4. take_screenshot()                                → 截图留证
5. list_console_messages(types=["error"])           → 检查报错
```

---

## 操作全参考

### 导航 Navigation

| 操作 | 命令 | 说明 |
|------|------|------|
| 打开 URL | `navigate_page(type="url", url=...)` | 导航到指定地址 |
| 刷新 | `navigate_page(type="reload")` | 刷新当前页 |
| 后退 | `navigate_page(type="back")` | 历史后退 |
| 前进 | `navigate_page(type="forward")` | 历史前进 |

```
navigate_page(type="url", url="https://example.com")
navigate_page(type="reload")
navigate_page(type="back")
navigate_page(type="forward")
```

### 页面结构 Page Structure

| 操作 | 命令 | 说明 |
|------|------|------|
| 获取结构 | `take_snapshot()` | 获取 accessibility 树，所有可交互元素及 uid |
| 保存到文件 | `take_snapshot(filePath=...)` | 页面很大时保存到文件 |
| 详情模式 | `take_snapshot(verbose=true)` | 包含所有可用信息 |
| 等待内容 | `wait_for(text=["..."])` | 等待文本出现 |

```
take_snapshot()                                → 全量 accessibility 树
take_snapshot(filePath="/tmp/page.txt")        → 大页面时存文件
take_snapshot(verbose=true)                    → 包含所有信息
wait_for(text=["登录成功"])                    → 等待文本出现
```

### 点击与悬停 Click & Hover

| 操作 | 命令 | 说明 |
|------|------|------|
| 点击 | `click(uid="ref_xxx")` | 点击元素 |
| 双击 | `click(uid="ref_xxx", dblClick=true)` | 双击 |
| 点击+快照 | `click(uid="ref_xxx", includeSnapshot=true)` | 点击后立刻获取新结构 |
| 悬停 | `hover(uid="ref_xxx")` | 鼠标悬停 |
| 拖拽 | `drag(from_uid="...", to_uid="...")` | 元素拖拽 |

```
click(uid="ref_xxx")                               → 单次点击
click(uid="ref_xxx", dblClick=true)                → 双击
click(uid="ref_xxx", includeSnapshot=true)         → 点击 + 返回更新结构
hover(uid="ref_xxx")                               → 悬停确认
drag(from_uid="ref_a", to_uid="ref_b")             → 拖拽
```

### 表单操作 Form Filling

| 操作 | 命令 | 说明 |
|------|------|------|
| 批量填表 | `fill_form(elements=[...])` | ✅ 推荐：一次填多个 |
| 单个输入 | `fill(uid="...", value="...")` | 单个输入框 |
| 键盘输入 | `type_text(text="...")` | 逐字输入 |
| 输入+提交 | `type_text(text="...", submit=true)` | 输入后按 Enter |
| 按键 | `press_key(key="Enter")` | 按键盘 |
| 组合键 | `press_key(key="Control+A")` | 快捷键 |
| 下拉选择 | `select_option(target="ref_xxx", values=["opt1"])` | 选择框 |

```
// ✅ 多个字段一次填完（推荐）
fill_form(elements=[
  {uid: "ref_xxx", value: "admin"},
  {uid: "ref_yyy", value: "password123"},
  {uid: "ref_zzz", value: "true"},                 // 复选框
])

// 单个输入
fill(uid="ref_xxx", value="hello")

// 键盘输入
press_key(key="Tab")
type_text(text="hello")
type_text(text="hello", submit=true)                // 输入后按回车

// 下拉选择
select_option(target="ref_xxx", values=["option1"])
```

### 截图 Screenshots

| 操作 | 命令 | 说明 |
|------|------|------|
| 截可视区 | `take_screenshot()` | 默认当前可视区域 |
| 截全页 | `take_screenshot(fullPage=true)` | 截整个页面 |
| 截元素 | `take_screenshot(uid="ref_xxx")` | 截特定元素 |
| 存文件 | `take_screenshot(filePath="...")` | 保存到指定路径 |
| 调质量 | `take_screenshot(type="jpeg", quality=80)` | JPEG 格式可调质量 |
| 高清 | `take_screenshot(scale="device")` | 设备像素 |

```
take_screenshot()                                   → 可视区域
take_screenshot(fullPage=true)                      → 全页面
take_screenshot(uid="ref_xxx")                      → 特定元素
take_screenshot(filePath="/tmp/screenshot.png")     → 存文件
take_screenshot(type="jpeg", quality=80)            → JPEG
take_screenshot(scale="device")                     → 高清
```

### 控制台与网络 Console & Network

| 操作 | 命令 | 说明 |
|------|------|------|
| 检查错误 | `list_console_messages(types=["error"])` | 只看 error |
| 检查警告 | `list_console_messages(types=["error","warn"])` | error + warn |
| 看全部 | `list_console_messages()` | 所有日志 |
| 看详情 | `get_console_message(msgid=0)` | 某条日志详情 |
| API 请求 | `list_network_requests(resourceTypes=["xhr","fetch"])` | 只看 XHR/fetch |
| 页面请求 | `list_network_requests(resourceTypes=["document"])` | 页面导航 |
| 请求详情 | `get_network_request(reqid=3)` | 查看请求/响应详情 |
| 保存响应 | `get_network_request(reqid=3, responseFilePath="...")` | 保存响应体 |

```
// Console
list_console_messages(types=["error"])              → 只看错误
list_console_messages(types=["error", "warn"])      → 错误 + 警告
list_console_messages()                             → 所有日志
get_console_message(msgid=0)                        → 特定日志详情

// Network
list_network_requests(resourceTypes=["xhr", "fetch"])  → API 请求
list_network_requests(resourceTypes=["document"])      → 页面导航
get_network_request(reqid=3)                           → 请求/响应详情
get_network_request(reqid=3, responseFilePath="/tmp/resp.json")  → 保存响应体
```

### 弹窗处理 Dialogs

| 操作 | 命令 | 说明 |
|------|------|------|
| 确定 | `handle_dialog(action="accept")` | 接受弹窗 |
| 取消 | `handle_dialog(action="dismiss")` | 取消弹窗 |
| 输入 | `handle_dialog(action="accept", promptText="hello")` | prompt 输入文字 |

```
handle_dialog(action="accept")                      → 确定
handle_dialog(action="dismiss")                     → 取消
handle_dialog(action="accept", promptText="hello")  → prompt 输入
```

### 键盘 Keyboard

```
press_key(key="Enter")
press_key(key="Escape")
press_key(key="Tab")
press_key(key="Control+A")
press_key(key="Control+C")
press_key(key="Control+V")
press_key(key="ArrowDown")
press_key(key="Control+Shift+R")    → 强制刷新
```

### 标签页管理 Tab Management

| 操作 | 命令 | 说明 |
|------|------|------|
| 列出标签 | `list_pages()` | 列出所有标签页 |
| 切换标签 | `select_page(pageId=0)` | 按 ID 选择标签 |
| 新标签 | `new_page(url="https://example.com")` | 打开新标签页 |
| 关闭标签 | `close_page(pageId=1)` | 关闭标签 |
| 调窗口 | `resize_page(width=1920, height=1080)` | 调整窗口大小 |

```
list_pages()                                        → 列出标签
select_page(pageId=0)                               → 切换到标签 0
new_page(url="https://example.com")                 → 打开新标签
close_page(pageId=1)                                → 关闭标签 1
resize_page(width=1920, height=1080)                → 调整窗口
```

### 文件上传 File Upload

```
// 先 snapshot 找到 file input 的 uid
upload_file(uid="ref_xxx", filePath="/path/to/file.pdf")
```

### 模拟 Emulation

| 操作 | 命令 | 说明 |
|------|------|------|
| 模拟网速 | `emulate(networkConditions="Slow 3G")` | 弱网测试 |
| 模拟设备 | `emulate(viewport="375x812x3,mobile,touch")` | iPhone X 视口 |
| 暗色模式 | `emulate(colorScheme="dark")` | 暗色主题 |
| 亮色模式 | `emulate(colorScheme="light")` | 亮色主题 |
| 模拟定位 | `emulate(geolocation="37.7749,-122.4194")` | 模拟 GPS |
| 用户代理 | `emulate(userAgent="...")` | 自定义 UA |
| CPU 降频 | `emulate(cpuThrottlingRate=4)` | CPU 节流测试 |

```
// 网络
emulate(networkConditions="Slow 3G")
emulate(networkConditions="Fast 4G")

// 设备视口
emulate(viewport="375x812x3,mobile,touch")          // iPhone X
emulate(viewport="414x896x3,mobile,touch,landscape")// iPhone 横屏

// 主题
emulate(colorScheme="dark")
emulate(colorScheme="light")

// 定位 / UA
emulate(geolocation="37.7749,-122.4194")
emulate(userAgent="Mozilla/5.0 ...")
```

### JavaScript 执行

```
evaluate_script(function="() => document.title")
evaluate_script(function="() => window.innerWidth")
evaluate_script(function="(el) => el.textContent", args=["ref_xxx"])
evaluate_script(function="() => document.querySelector('.error')?.textContent")
```

### 性能审计 Performance

| 操作 | 命令 | 说明 |
|------|------|------|
| LH 审计 | `lighthouse_audit(mode="navigation")` | 加载时 Lighthouse |
| 快照审计 | `lighthouse_audit(mode="snapshot")` | 当前状态审计 |
| 性能追踪 | `performance_start_trace(reload=true)` | 开始性能记录 |

---

## 探索式测试流程

当你说"测一下"时，执行以下循环：

```
循环体：
 ① take_snapshot()
    获取页面上所有可交互元素及其 uid

 ② take_screenshot()
    截当前画面做"操作前"证据

 ③ list_console_messages(types=["error"])
    检查当前是否有 JS 报错

 ④ 按优先级选一个没点过的元素

 ⑤ 交互
    hover → wait 500ms → click → wait 1-2s

 ⑥ 操作后检查
    - list_console_messages(types=["error"])
    - list_network_requests(xhr/fetch)
    - take_screenshot()

 ⑦ 判断
    页面变了 → 回到 ① 重新扫描
    没变化   → 回到 ④ 点下一个
```

### 元素优先级

| 优先级 | 元素 | 说明 |
|--------|------|------|
| P0 🔴 | 链接、Tab、菜单项 | 导航类，改变页面状态 |
| P1 🟠 | 按钮（提交/保存/删除） | 触发关键操作 |
| P2 🟡 | 输入框、开关、复选框 | 数据输入类 |
| P3 🟢 | 下拉框、滑块、日期选择器 | 较复杂交互 |
| P4 🔵 | 模态框关闭按钮 × | 关闭弹窗 |
| P5 ⚪ | 分页、排序 | 列表操作 |

### 操作后检查清单

```
1. 等待 1-2s 让页面响应
2. list_console_messages(types=["error"])
3. list_network_requests(resourceTypes=["xhr","fetch"])
4. take_screenshot() → 保存证据
```

### 异常处理

| 现象 | 处理方式 | 是否继续 |
|------|---------|:-------:|
| Console 有 error | 截图 + 记录错误详情 | ✅ 继续 |
| API 4xx | 截图 + 记录 URL + 状态码 | ✅ 继续 |
| API 5xx | 截图 + 记录 | ✅ 继续 |
| 页面白屏 | 截图 + 记录当前 URL | ⏹ 停止路径 |
| 弹出 alert/confirm | 截图弹窗 → dismiss 关掉 | ✅ 继续 |
| 点击后没反应 | 跳过该元素，标记不可交互 | ✅ 继续 |
| 页面跳转了 | 重新扫描新页面结构 | ✅ 继续探索 |

---

## 测试计划执行

用户创建结构化测试用例 Markdown 文件，AI 按用例逐条执行。

### 用例格式

```markdown
## TC-01: 正常登录
| 前置条件 | 操作步骤 | 预期结果 |
|---------|---------|---------|
| 已打开登录页 | 1. 输入用户名 admin | 登录成功 |
|            | 2. 输入密码 123456 | 跳转首页 |
|            | 3. 点击登录按钮 | 无控制台报错 |
```

表格固定 3 列：**前置条件**、**操作步骤**、**预期结果**。

仓库 `examples/` 目录提供可直接运行的示例测试计划，复制修改即可使用。

### 执行流程

1. 解析 Markdown 表格，提取每个 TC 的前置条件、步骤、预期
2. 确保前置条件满足（页面状态、登录态等）
3. 按顺序执行每一步操作
4. 每步后截图 + 检查 console + 检查网络
5. 对比实际结果与预期结果
6. 输出测试报告（通过/失败 + 证据截图）

---

## 辅助脚本

仓库 `scripts/` 目录提供两个 Python 辅助脚本（纯 stdlib，无外部依赖）：

### test_env.py

启动本地开发服务器，等待端口就绪：

```bash
python scripts/test_env.py                          # 默认 5173 端口
python scripts/test_env.py --port 3000              # 自定义端口
python scripts/test_env.py --port 8080 --cmd "npm start"
```

### snapshot_diff.py

对比两张截图（需安装 ImageMagick）：

```bash
python scripts/snapshot_diff.py baseline.png current.png diff.png
```

---

## 反模式

| 反模式 | 正确做法 |
|--------|---------|
| 不 snapshot 直接点 | 先 snapshot 确认元素存在和 uid |
| 操作后不等 | 等页面响应再下一步 |
| 不看 console | 每步后检查 console error |
| 不截图 | 关键步骤截图留证 |
| 只测 happy path | 也测取消、关闭、空提交 |
| 弹窗不处理 | 截图后再关 |
| 从不看 network | API 错误比 UI 错误更隐蔽 |

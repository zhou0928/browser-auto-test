# Browser Auto Test

**Watch your AI agent drive a real browser in real time.**

A reusable skill for AI coding agents (Claude Code, OpenCode, Cursor, Gemini CLI, Copilot) that enables visible, interactive browser automated testing. Every click, hover, form fill, and navigation happens in a live Chrome window — you watch the AI test your web app like a human would.

> "测一下" — and the AI opens Chrome, clicks around, fills forms, checks console errors, and reports what it finds.

---

## Features

- **👁️ Visible by default** — Chrome window pops up, you watch everything in real time. No headless mystery.
- **🤖 Human-like interaction** — Snapshot first, hover to confirm, click, wait, check. Not a robot hammering XHR.
- **🔍 Exploratory mode** — AI systematically clicks every link, button, and form, checking for console errors and API failures after each step.
- **📸 Screenshot evidence** — Key steps are screenshot'd for traceability and visual verification.
- **🕸️ Network-aware** — Automatically checks XHR/fetch requests for 4xx/5xx after every interaction.
- **📝 Test plan driven** — Follow structured `.md` test cases with preconditions, steps, and expected results.
- **🎭 Headless available** — Say "后台跑" to switch to Playwright headless mode for CI or quiet runs.
- **🔌 Zero config** — Auto-detects Chrome on port 9222 or launches a new instance.

---

## How It Works

```
                You say "测一下"
                      │
                      ▼
      ┌───────────────────────────────┐
      │  Chrome running on :9222?     │
      │  No → launch Chrome with      │
      │       --remote-debugging-port │
      └───────────┬───────────────────┘
                  │
                  ▼
      ┌───────────────────────────────┐
      │  AI drives browser via        │
      │  Chrome DevTools Protocol     │
      │  (chrome-devtools_* tools)    │
      └───────────┬───────────────────┘
                  │
                  ▼
      ┌───────────────────────────────┐
      │  Per interaction:             │
      │  1. snapshot → get page tree  │
      │  2. hover → confirm target    │
      │  3. click / fill / navigate   │
      │  4. wait for response         │
      │  5. check console errors      │
      │  6. check network requests    │
      │  7. screenshot                │
      └───────────┬───────────────────┘
                  │
                  ▼
      ┌───────────────────────────────┐
      │  Report results with          │
      │  screenshots & error logs     │
      └───────────────────────────────┘
```

---

## Installation

### Option 1: Claude Code

```bash
# Copy skill to Claude Code skills directory
cp -r browser-auto-test ~/.claude/skills/
```

### Option 2: OpenCode

```bash
# Skills are auto-discovered from ~/.config/opencode/skills/
cp -r browser-auto-test ~/.config/opencode/skills/
```

### Option 3: Cursor

Copy `SKILL.md` into `.cursor/rules/` as a rule file.

### Option 4: Gemini CLI

```bash
gemini skills install https://github.com/zhou0928/browser-auto-test.git
```

### Option 5: Other AI Agents

Skills are plain Markdown. Reference `SKILL.md` in your agent's system prompt or instruction file.

---

## Quick Start

### 1. Interactive mode (visible browser)

Say to your AI agent:

> **"测一下这个页面"**

The AI will:
1. Open/connect to Chrome (visible window, port 9222)
2. Ask for the URL to test
3. Take a snapshot of the page
4. Start clicking elements, filling forms, navigating
5. Check console errors and network failures after each step
6. Report findings with screenshots

### 2. Run a test plan

Create a test plan file like `login.md`:

```markdown
# 登录测试

## TC-01: 正常登录
| 前置条件 | 操作步骤 | 预期结果 |
|---------|---------|---------|
| 已打开登录页 | 1. 输入用户名 admin | 登录成功 |
|            | 2. 输入密码 123456 | 跳转首页 |
|            | 3. 点击登录按钮 | 无控制台报错 |
```

Then say:

> **"跑一下 login.md"**

### 3. Headless mode (no window)

> **"后台跑一下这个测试"**

Switches to Playwright headless — same operations, no visible window.

---

## API Reference

| Operation | Tool | Description |
|-----------|------|-------------|
| Navigate | `navigate_page(type="url", url=...)` | Open a URL |
| Reload | `navigate_page(type="reload")` | Reload page |
| Snapshot | `take_snapshot()` | Get accessibility tree |
| Screenshot | `take_screenshot()` | Capture visible area |
| Full page | `take_screenshot(fullPage=true)` | Capture entire page |
| Element shot | `take_screenshot(uid="...")` | Capture element only |
| Click | `click(uid="...")` | Click element |
| Double click | `click(uid="...", dblClick=true)` | Double click |
| Hover | `hover(uid="...")` | Hover over element |
| Fill form | `fill_form(elements=[...])` | Batch fill fields |
| Fill input | `fill(uid="...", value="...")` | Single input |
| Type text | `type_text(text="...")` | Keyboard type |
| Press key | `press_key(key="Enter")` | Key press |
| Execute JS | `evaluate_script(function="...")` | Run JavaScript |
| Console errors | `list_console_messages(types=["error"])` | Check errors |
| Network requests | `list_network_requests(resourceTypes=["xhr","fetch"])` | Check APIs |
| Request detail | `get_network_request(reqid=3)` | Full request info |
| Dialog | `handle_dialog(action="accept"/"dismiss")` | Handle alert/confirm |
| Drag | `drag(from_uid="...", to_uid="...")` | Drag & drop |
| Resize | `resize_page(width=1920, height=1080)` | Resize window |
| Tabs | `list_pages()` / `select_page(pageId=0)` | Tab management |
| New tab | `new_page(url="...")` | Open new tab |
| Close tab | `close_page(pageId=1)` | Close tab |
| File upload | `upload_file(uid="...", filePath="...")` | Upload file |

---

## Exploratory Testing Workflow

The AI follows this loop when doing open-ended testing:

```
Loop:
  1. take_snapshot()              → get all interactive elements
  2. take_screenshot()            → capture current state
  3. list_console_messages(error) → check for errors
  4. pick next unclicked element (priority order)
  5. hover → wait 0.5s → click → wait 1-2s
  6. post-action checks
  7. page changed? → rescan
```

**Element priority:**
| Priority | Elements |
|----------|----------|
| P0 | Links, tabs, menu items |
| P1 | Buttons (submit/save/delete) |
| P2 | Inputs, toggles, checkboxes |
| P3 | Dropdowns, sliders, date pickers |
| P4 | Modal close buttons |
| P5 | Pagination, sorting |

**Post-action checklist:**
1. Wait 1-2 seconds for page response
2. `list_console_messages(types=["error"])`
3. `list_network_requests(resourceTypes=["xhr","fetch"])`
4. `take_screenshot()` — save evidence

---

## Test Plan Format

Test plans are Markdown files with structured tables. Place them in any directory and reference by path:

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

Each test case table has 3 columns: **前置条件** (preconditions), **操作步骤** (steps), **预期结果** (expected results).

---

## Scripts

### `test-env.sh`

Start a local dev server and wait for it to become ready:

```bash
bash scripts/test-env.sh          # default port 5173
bash scripts/test-env.sh 3000     # custom port
bash scripts/test-env.sh 8080 "npm start"  # custom command
```

### `snapshot-diff.sh`

Compare two screenshots using ImageMagick:

```bash
bash scripts/snapshot-diff.sh baseline.png current.png diff.png
```

---

## Requirements

- Google Chrome
- macOS / Linux (Windows via WSL)
- AI agent with tool-calling support (Claude Code, OpenCode, Cursor, etc.)

---

## License

MIT

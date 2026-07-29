---
name: browser-auto-test
description: "Browser automated testing with a visible Chrome window — the AI drives a real browser and you watch every interaction in real time. Uses Chrome DevTools Protocol (CDP) for visible mode, Playwright for headless/CI mode. Use when: running exploratory tests on web apps, clicking every element systematically, filling and submitting forms, checking console errors and network requests, capturing screenshots, automating multi-step test workflows from structured test plans. Supports both interactive (visible) and headless modes. Triggers: '测一下', '测试', '跑测试', '点一点', '探索测试', '人工测试', '打开浏览器', '跑一下', 'check this page', 'test this', 'exploratory test', 'browser test', 'automated test', 'run tests'."
---

# Browser Auto Test

A browser automated testing skill for AI agents. Drives a real Chrome window visible to the user — every click, hover, form fill, and navigation is observable in real time.

## Mode: Visible by Default

The AI automatically opens or connects to Chrome (port 9222 with `--remote-debugging-port`). The browser window appears on screen — the user watches every interaction as it happens.

**Say "后台跑" to switch to headless Playwright mode** (for CI, background runs, or when no Chrome is available).

## Core Principles

1. **Snapshot first** — Always call `take_snapshot()` before any interaction to get the current accessibility tree and element UIDs.
2. **Hover before click** — Mimic human behavior: hover to confirm the target, then click.
3. **Batch form fills** — Use `fill_form()` with multiple fields at once, not individual `fill()` calls.
4. **Post-action checks** — After every interaction: check console errors + network anomalies + page state change.
5. **Screenshot evidence** — Capture screenshots at key steps for traceability.
6. **Network-aware** — Check XHR/fetch responses after form submissions and navigations.

## Quick Start

```
1. navigate_page(type="url", url="https://example.com")  → open page
2. take_snapshot()                                        → get page structure
3. click / fill / hover                                   → interact
4. take_screenshot()                                      → capture evidence
5. list_console_messages(types=["error"])                 → check errors
```

## Operation Reference

### Navigation

```
navigate_page(type="url", url="https://example.com")
navigate_page(type="reload")
navigate_page(type="back")
navigate_page(type="forward")
```

### Page Structure

```
take_snapshot()                                    → full accessibility tree
take_snapshot(filePath="/tmp/page.txt")            → save to file (large pages)
take_snapshot(verbose=true)                        → include all available info
```

### Click & Hover

```
click(uid="ref_xxx")                               → single click
click(uid="ref_xxx", dblClick=true)                → double click
click(uid="ref_xxx", includeSnapshot=true)         → click + return updated snapshot
hover(uid="ref_xxx")                               → hover over element
```

### Form Filling

```
// ✅ Multiple fields at once (preferred)
fill_form(elements=[
  {uid: "ref_xxx", value: "admin"},
  {uid: "ref_yyy", value: "password123"},
  {uid: "ref_zzz", value: "true"},                 // checkbox
])

// Single field
fill(uid="ref_xxx", value="hello")

// Keyboard input
press_key(key="Tab")
type_text(text="hello")
type_text(text="hello", submit=true)                // press Enter after typing
```

### Screenshots

```
take_screenshot()                                   → visible viewport
take_screenshot(fullPage=true)                      → full scrollable page
take_screenshot(uid="ref_xxx")                      → specific element
take_screenshot(filePath="/tmp/screenshot.png")     → save to file
take_screenshot(type="jpeg", quality=80)            → JPEG format
take_screenshot(scale="device")                     → device pixel resolution
```

### JavaScript Execution

```
evaluate_script(function="() => document.title")
evaluate_script(function="() => window.innerWidth")
evaluate_script(function="(el) => el.textContent", args=["ref_xxx"])
evaluate_script(function="() => document.querySelector('.error').textContent")
```

### Console & Network Inspection

```
// Console
list_console_messages(types=["error"])              → errors only
list_console_messages(types=["error", "warn"])      → errors + warnings
list_console_messages()                             → all messages
get_console_message(msgid=0)                         → specific message

// Network
list_network_requests(resourceTypes=["xhr", "fetch"])  → API requests only
list_network_requests(resourceTypes=["document"])      → page navigations
get_network_request(reqid=3)                           → full request details

// Performance
lighthouse_audit(mode="navigation")                 → Lighthouse report
lighthouse_audit(mode="snapshot")                   → snapshot audit
```

### Dialogs

```
handle_dialog(action="accept")                      → OK / Confirm
handle_dialog(action="dismiss")                     → Cancel
handle_dialog(action="accept", promptText="hello")  → Prompt with text
```

### Keyboard

```
press_key(key="Enter")
press_key(key="Escape")
press_key(key="Tab")
press_key(key="Control+A")
press_key(key="Control+C")
press_key(key="Control+V")
press_key(key="ArrowDown")
```

### Tab Management

```
list_pages()                                        → list open tabs
select_page(pageId=0)                               → select tab by ID
new_page(url="https://example.com")                 → open new tab
close_page(pageId=1)                                → close tab
resize_page(width=1920, height=1080)                → resize window
```

### File Upload

```
// 1. Take snapshot to find file input element
// 2. Upload file
upload_file(uid="ref_xxx", filePath="/path/to/file.pdf")
```

### Emulation

```
// Network conditions
emulate(networkConditions="Slow 3G")
emulate(networkConditions="Fast 4G")

// Device / viewport
emulate(viewport="375x812x3,mobile,touch")          // iPhone X
emulate(viewport="414x896x3,mobile,touch,landscape")// iPhone landscape

// Color scheme
emulate(colorScheme="dark")
emulate(colorScheme="light")

// Geolocation
emulate(geolocation="37.7749,-122.4194")           // San Francisco
```

---

## Exploratory Testing Workflow

The AI executes this loop for open-ended / ad-hoc testing:

```
Each cycle:
  1. take_snapshot()                 → discover all interactive elements
  2. take_screenshot()               → capture current visual state
  3. list_console_messages(error)    → check for JS errors
  4. Pick highest-priority unvisited element
  5. hover → wait 0.5s → click → wait 1-2s
  6. Post-action checks
  7. If page changed → rescan from step 1
```

### Element Priority

| Priority | Elements |
|----------|----------|
| P0 | Links, tabs, menu items |
| P1 | Buttons (submit/save/delete) |
| P2 | Inputs, toggles, checkboxes |
| P3 | Dropdowns, sliders, date pickers |
| P4 | Modal close buttons |
| P5 | Pagination, sorting |

### Post-Action Checks

```
1. wait(1-2s) for page to respond
2. list_console_messages(types=["error"])
3. list_network_requests(resourceTypes=["xhr","fetch"])
4. take_screenshot() → save evidence
```

### Error Handling

| Symptom | Action |
|---------|--------|
| Console error | Screenshot + record, continue |
| API 4xx/5xx | Screenshot + record, continue |
| Blank page | Screenshot + record URL |
| Dialog appeared | Screenshot dialog → dismiss |
| Click did nothing | Skip, try next element |
| Page changed | Rescan page structure |

---

## Test Plan Execution

Create structured test cases in Markdown files and reference them by path:

**Test case format:**

```markdown
## TC-01: Login with valid credentials
| 前置条件 | 操作步骤 | 预期结果 |
|---------|---------|---------|
| Login page is open | 1. Enter username "admin" | Login succeeds |
|                    | 2. Enter password "123456" | Redirected to dashboard |
|                    | 3. Click login button | No console errors |
```

The AI reads each test case, executes steps in order, compares results to expected outcomes, and records pass/fail with screenshots.

---

## Headless Mode

For CI pipelines or quiet runs, say **"后台跑"** or **"headless mode"**.

The AI switches to Playwright headless browser. All operations remain identical — same snapshot/click/fill/check workflow — but no Chrome window appears.

---

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|-------------|------------------|
| Clicking without snapshot | Always snapshot first to confirm element exists and get uid |
| Not waiting after action | Wait for page to respond before next step |
| Skipping console checks | Check console errors after every interaction |
| No screenshots | Capture screenshots at key steps |
| Happy path only | Also test cancel, close, empty submissions |
| Ignoring dialogs | Screenshot dialog before dismissing |
| Never checking network | API errors are more subtle than UI errors |

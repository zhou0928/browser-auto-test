<div align="center">
  <h1>Browser Auto Test Skills</h1>
  <p>
    <a href="https://github.com/zhou0928/browser-auto-test/stargazers"><img src="https://img.shields.io/github/stars/zhou0928/browser-auto-test?style=social" alt="GitHub Stars"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
    <br><br>
    <strong>让 AI 打开看得见的浏览器，像真人一样帮你测网页。</strong>
    <br>
    AI-driven browser automated testing — visible, interactive, human-like.
  </p>
</div>

---

## Skills

| Skill | Description |
|-------|-------------|
| [browser-auto-test](browser-auto-test/) | 浏览器自动化测试 skill — Chrome 可见模式 / Playwright 无头模式。AI 自动点击、填表单、截图、检查 console 报错和 API 异常。 |

### 安装

```bash
# Claude Code
cp -r browser-auto-test ~/.claude/skills/

# OpenCode
cp -r browser-auto-test ~/.config/opencode/skills/

# Gemini CLI
gemini skills install https://github.com/zhou0928/browser-auto-test.git
```

### 快速使用

> **"测一下这个页面"** — AI 打开 Chrome，开始探索式测试

> **"跑一下 login.md"** — AI 按测试计划文件执行用例

> **"后台跑"** — 切换 Playwright 无头模式（适合 CI）

---

## 特性

- **👁️ 看得见的浏览器** — Chrome 窗口实时弹出来，AI 的每一步操作你都能看到
- **🤖 类人操作** — Snapshot 获取页面结构 → hover 确认 → 点击 → 等待 → 检查结果
- **🔍 探索式测试** — AI 自动遍历每个链接/按钮/表单，每步检查 console error 和 API
- **📸 截图留证** — 关键步骤自动截图，可追溯
- **📝 测试计划驱动** — 按结构化 Markdown 测试用例执行
- **🎭 无头模式** — 支持 Playwright headless 模式，方便 CI 集成
- **🔌 零配置启动** — 自动检测或启动 Chrome

---

## 仓库结构

```
browser-auto-test/
├── README.md                       # 本文件 — 仓库总览
├── LICENSE                         # MIT
├── browser-auto-test/              # browser-auto-test skill
│   ├── SKILL.md                    #   Skill 定义
│   ├── scripts/
│   │   ├── test-env.sh             #   启动开发服务器
│   │   └── snapshot-diff.sh        #   截图对比
│   └── browser-auto-test.zip       #   安装包
└── ...                             # 后续可继续加新 skill
```

---

## License

MIT

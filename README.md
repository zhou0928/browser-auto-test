<div align="center">
  <h1>Browser Auto Test Skills</h1>
  <p>
    <a href="https://github.com/zhou0928/browser-auto-test/stargazers"><img src="https://img.shields.io/github/stars/zhou0928/browser-auto-test?style=social" alt="GitHub Stars"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  </p>
  <p>
    <strong>让 AI 打开看得见的浏览器，像真人一样帮你测网页。</strong><br>
    AI-driven browser automated testing — visible, interactive, human-like.
  </p>
</div>

---

## Skills

| Skill | Description |
|-------|-------------|
| [browser-auto-test](browser-auto-test/) | 浏览器自动化测试 skill。AI 打开可见的 Chrome 窗口，执行点击、填表、截图、报错检查，你在旁边实时观看。支持无头模式 (Playwright) 用于 CI。 |

## Quick Start

```bash
# 安装
cp -r browser-auto-test ~/.claude/skills/          # Claude Code
cp -r browser-auto-test ~/.config/opencode/skills/ # OpenCode
```

对你的 AI 助手说：

> **"测一下这个页面"** — AI 打开 Chrome，开始探索式测试
>
> **"跑一下 login.md"** — AI 按测试计划文件执行用例
>
> **"后台跑"** — 切换 Playwright 无头模式

## Features

- **👁️ 可见模式** — Chrome 窗口实时弹出，操作全程可见
- **🤖 类人操作** — Snapshot → hover → click → wait → check
- **🔍 探索式测试** — 自动遍历所有可交互元素，检查 error
- **📝 测试计划驱动** — 按结构化 Markdown 用例逐条执行
- **📸 截图留证** — 关键步骤自动截图
- **🎭 无头模式** — Playwright headless，适合 CI
- **🔌 零配置** — 自动检测或启动 Chrome 9222

## Structure

```
browser-auto-test/
├── README.md
├── LICENSE
└── browser-auto-test/          ← skill 目录
    ├── SKILL.md                ← AI 加载的完整操作文档
    ├── scripts/
    │   ├── test_env.py         ← 启动开发服务器
    │   └── snapshot_diff.py    ← 截图对比 (ImageMagick)
    └── browser-auto-test.zip   ← 安装包
```

## License

MIT

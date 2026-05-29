# Design-to-Frontend

从 Figma / MasterGo / 截图 / 手稿 等任何设计稿生成完整的前端项目。

## 特性

- **多来源输入**: Figma 链接 / MasterGo 链接 / 设计截图 / 文字描述
- **默认 Vue 3 + Element Plus**: 完整 Vite 项目，组件化结构
- **React 18 + Ant Design**: 按需选择
- **单 HTML 原型**: 快速预览用
- **ECharts 5.x**: 图表统一用 ECharts
- **色彩自动映射**: 从设计稿提取色板并应用到主题配置

## 输出模式

| 模式 | 技术栈 | 适用场景 |
|------|--------|---------|
| 完整项目（默认） | Vue 3 + Element Plus + ECharts | 多页面、复杂应用 |
| React 项目 | React 18 + Ant Design 5.x + ECharts | 用户指定时 |
| 单 HTML | React 18 + Ant Design 5.x（CDN） | 原型 / Landing Page |

## 快速开始

```bash
# Figma 设计稿数据获取
python3 scripts/figma_fetch.py "<figma_url>"

# MasterGo 设计稿数据获取
python3 scripts/mastergo_fetch.py "<mastergo_url>"
```

## 环境变量

- `FIGMA_TOKEN` — Figma REST API 访问令牌
- `MASTERGO_TOKEN` — MasterGo DSL API 访问令牌

## Skill 文件结构

```
design-to-frontend/
├── SKILL.md                      # 主说明 — 工作流、组件映射规则、项目模板
├── scripts/
│   ├── figma_fetch.py            # Figma REST API 数据抓取
│   └── mastergo_fetch.py         # MasterGo DSL API 数据抓取
└── references/
    ├── antd-echarts-patterns.md  # 单 HTML 模式模板
    └── deployment.md             # 部署指南
```

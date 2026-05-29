# Design-to-Frontend

从 Figma / MasterGo / 截图 / 手稿等任何设计稿生成完整的前端页面。

## 特性

- **多来源输入**: Figma 链接 / MasterGo 链接 / 设计截图 / 文字描述
- **Ant Design 5.x**: 自动映射设计元素到 Ant Design 组件
- **ECharts 5.x**: 内置图表支持
- **单文件输出**: 一个 HTML 搞定，零构建
- **色彩映射**: 自动从设计稿提取色板并应用到主题

## 快速开始

```bash
# Figma 设计稿数据获取
python3 scripts/figma_fetch.py "<figma_url>"

# 然后 AI 自动分析数据生成前端页面
```

## 依赖

- Python 3.10+
- 环境变量: `FIGMA_TOKEN` (Figma API 令牌)
- 环境变量: `MASTERGO_TOKEN` (MasterGo API 令牌)

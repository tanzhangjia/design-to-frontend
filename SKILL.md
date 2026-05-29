---
name: design-to-frontend
description: 从 Figma / MasterGo / 截图 / 手稿 等任何设计稿生成完整的前端页面。当用户提供设计链接、截图或描述要求生成前端代码时使用。输出为自包含的 HTML 文件，基于 React + Ant Design + ECharts 组件库。自动将设计稿中的颜色、字体、排版、间距等视觉属性映射到 Ant Design 主题配置和前端组件中。
---

# Design-to-Frontend Skill

从任何设计稿一键生成前端页面。

## 输入来源

支持以下任意输入：
- **Figma 链接** — 通过 REST API 获取节点树、颜色、字体、截图
- **MasterGo 链接** — 通过 DSL API 获取设计结构
- **设计截图** — 直接分析图片生成对应风格的前端
- **文字描述** — 纯 Prompt 驱动的 UI 生成

## 工作流程

### Step 1: 获取设计数据

根据输入类型选择对应方式：

**Figma 链接:**
```bash
python3 scripts/figma_fetch.py "<figma_url>"
```

**MasterGo 链接:**
```bash
# 通过 MasterGo DSL API 获取
python3 /path/to/mastergo/scripts/mastergo_analyze.py "<mastergo_url>"
python3 /path/to/mastergo/scripts/mastergo_get_dsl.py "<mastergo_url>"
```

**其他输入（截图 / 描述）:**
直接用视觉分析或 Prompt 理解设计意图，直接跳到 Step 2。

输出包含：页面结构、节点树、颜色、字体、尺寸、布局信息。

### Step 2: 分析设计结构

从获取的数据中提取关键信息：
- **页面布局**：Section 划分、导航结构、内容区块
- **色彩体系**：主色、辅色、背景色、文本色
- **排版**：标题、正文、小字的字号字重
- **组件类型**：卡片、表格、按钮、图表（ECharts）、表单等
- **响应式设计**：设计稿可能只有一种尺寸，需要自己处理响应式

### Step 3: 生成前端页面

**核心规约：**
- 输出为单个 HTML 文件，自包含
- **组件库：Ant Design 5.x**（通过 unpkg CDN 加载）
- **图表：ECharts 5.x**（通过 unpkg CDN 加载）
- 用 Ant Design 的 `ConfigProvider` + `theme` 配置实现设计稿的色彩方案
- Unicode 而非 Font Awesome/Bootstrap Icons（使用 Ant Design 内置图标或 Unicode）

**Ant Design 组件映射规则：**
| 设计元素 | Ant Design 组件 |
|----------|----------------|
| 导航栏 | `Layout.Header` + `Menu` |
| 卡片区块 | `Card` |
| 表格数据 | `Table` |
| 表单 | `Form` + `Input` / `Select` / `DatePicker` |
| 按钮 | `Button`（type=primary / default） |
| 标签/选项卡 | `Tabs` |
| 分页 | `Pagination` |
| 图表 | ECharts（`echarts.init`） |
| 统计数字 | `Statistic` |
| 列表 | `List` |
| 弹窗 | `Modal` / `Drawer` |
| 进度 | `Progress` |
| 徽标 | `Badge` |
| 提示 | `Alert` / `message` / `notification` |
| 空态 | `Empty` |

**CSS 方案：**
- Ant Design 5.x 使用 CSS-in-JS（@ant-design/cssinjs），不需要额外引入 CSS 文件
- 额外的自定义样式使用 `<style>` 标签覆盖

**色彩主题映射：**
```javascript
<ConfigProvider theme={{
  token: {
    colorPrimary: '#...',       // 设计稿主色
    colorSuccess: '#...',
    colorWarning: '#...',
    colorError: '#...',
    colorInfo: '#...',
    borderRadius: X,
    colorBgContainer: '#...',
    fontSize: X,
  }
}}>
```

### Step 4: 部署

```bash
# 启动一个静态文件服务器
npx http-server -p <port> --cors -c-1 -a 0.0.0.0
```

## 组件文档参考

当需要查阅组件用法时：
- Ant Design: https://ant.design/components/overview/
- ECharts: https://echarts.apache.org/en/option.html

## 已知限制

- Figma Community 文件（/site/ 路径）不能通过 API 获取完整节点树，只能获取截图
- MasterGo 需要 Team Edition 账号且文件在 Team Projects 中

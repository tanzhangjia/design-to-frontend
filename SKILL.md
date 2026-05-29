---
name: design-to-frontend
description: 从 Figma / MasterGo / 截图 / 手稿 等任何设计稿生成完整的前端项目。当用户提供设计链接、截图或描述要求生成前端代码时使用。默认生成完整 Vue 3 + Element Plus 项目，也可按需生成 React + Ant Design 或单 HTML。图表统一用 ECharts。自动将设计稿中的颜色、字体、排版、间距等视觉属性映射到前端主题配置和组件中。
---

# Design-to-Frontend Skill

从任何设计稿生成完整的前端项目。

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
# 需要通过 MasterGo DSL API 获取
# 外部已有对应的 mastergo skill
```

**其他输入（截图 / 描述）:**
直接用视觉分析或 Prompt 理解设计意图，直接跳到 Step 2。

### Step 2: 分析设计结构

从获取的数据中提取关键信息：
- **页面布局**：Section 划分、导航结构、内容区块
- **色彩体系**：主色、辅色、背景色、文本色
- **排版**：标题、正文、小字的字号字重
- **组件类型**：卡片、表格、按钮、图表（ECharts）、表单等
- **响应式设计**：设计稿可能只有一种尺寸，需要自己处理响应式
- **路由结构**：多页应用需要规划路由

### Step 3: 生成前端项目

**选择输出模式：**

| 模式 | 适用场景 | 技术栈 |
|------|---------|--------|
| **完整项目（默认）** | 多页面、复杂应用 | Vue 3 + Element Plus + ECharts |
| **React 项目** | 用户指定 React | React 18 + Ant Design 5.x + ECharts |
| **单 HTML** | 原型/Landing Page | React 18 + Ant Design 5.x + ECharts（CDN） |

#### 模式一：Vue 3 + Element Plus 完整项目（默认）

使用 Vite 作为构建工具。项目结构：

```
project-name/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   │   └── index.js
│   ├── views/
│   │   ├── Home.vue
│   │   ├── ... (按设计稿的页面/区块划分)
│   ├── components/
│   │   ├── Header.vue
│   │   ├── HeroSection.vue
│   │   ├── FeaturesSection.vue
│   │   ├── ChartSection.vue
│   │   ├── PricingSection.vue
│   │   └── Footer.vue
│   ├── assets/
│   │   └── styles/
│   │       └── theme.scss       # 设计稿色板变量
│   ├── composables/
│   │   └── useECharts.js        # ECharts 通用 hooks
│   └── api/
│       └── index.js             # 模拟 API 数据
```

**核心依赖：**
```json
{
  "vue": "^3.4",
  "vue-router": "^4.3",
  "element-plus": "^2.7",
  "echarts": "^5.5",
  "axios": "^1.7",
  "@element-plus/icons-vue": "^2.3"
}
```

**Element Plus 组件映射规则：**
| 设计元素 | Element Plus 组件 |
|----------|-----------------|
| 导航栏 | `el-menu` + `el-header` |
| 卡片区块 | `el-card` |
| 表格数据 | `el-table` |
| 表单 | `el-form` + `el-input` / `el-select` / `el-date-picker` |
| 按钮 | `el-button`（type=primary/default） |
| 标签/选项卡 | `el-tabs` |
| 分页 | `el-pagination` |
| 图表 | ECharts（通过 `composables/useECharts`） |
| 统计数字 | 自定义组件或用 `el-statistic` |
| 列表 | `el-table` / 自定义 |
| 弹窗 | `el-dialog` / `el-drawer` |
| 进度 | `el-progress` |
| 徽标 | `el-badge` |
| 提示 | `el-alert` / `ElMessage` / `ElNotification` |
| 空态 | `el-empty` |
| 布局 | `el-row` + `el-col` |

**色彩主题配置：**
```scss
// src/assets/styles/element-variables.scss
// 通过 Element Plus 的 CSS 变量覆盖
:root {
  --el-color-primary: #...;
  --el-color-success: #...;
  --el-color-warning: #...;
  --el-color-danger: #...;
  --el-color-info: #...;
  --el-border-radius-base: 8px;
}
```

然后在 `vite.config.js` 中引入：
```javascript
import ElementPlus from 'unplugin-element-plus/vite'

export default {
  plugins: [
    ElementPlus({ useSource: true }),
  ],
}
```

**ECharts 组合式函数 `useECharts.js`：**
```javascript
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

export function useECharts(chartRef) {
  const chartInstance = ref(null)

  function initChart(options) {
    chartInstance.value = echarts.init(chartRef.value)
    chartInstance.value.setOption(options)
  }

  function resizeChart() {
    chartInstance.value?.resize()
  }

  onMounted(() => {
    window.addEventListener('resize', resizeChart)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', resizeChart)
    chartInstance.value?.dispose()
  })

  return { chartInstance, initChart }
}
```

#### 模式二：React 18 + Ant Design 完整项目（用户指定）

使用 Vite + React。项目结构类似 Vue 版：

```
project-name/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── router/
│   │   └── index.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   └── ...
│   ├── components/
│   │   ├── ...
│   ├── config/
│   │   └── theme.js          # Ant Design 主题 token
│   └── hooks/
│       └── useECharts.js
```

**Ant Design 组件映射规则：**
| 设计元素 | Ant Design 组件 |
|----------|----------------|
| 导航栏 | `Layout.Header` + `Menu` |
| 卡片区块 | `Card` |
| 表格数据 | `Table` |
| 表单 | `Form` + `Input` / `Select` / `DatePicker` |
| 按钮 | `Button` |
| 标签/选项卡 | `Tabs` |
| 分页 | `Pagination` |
| 图表 | ECharts（`useECharts` hook） |
| 统计数字 | `Statistic` |
| 弹窗 | `Modal` / `Drawer` |
| 进度 | `Progress` |
| 徽标 | `Badge` |
| 提示 | `Alert` / `message` / `notification` |

**色彩主题配置：**
```javascript
// src/config/theme.js
export default {
  token: {
    colorPrimary: '#...',
    colorSuccess: '#...',
    colorWarning: '#...',
    colorError: '#...',
    colorInfo: '#...',
    borderRadius: 8,
    colorBgContainer: '#...',
  }
}
```

在 App.jsx 中用 `<ConfigProvider theme={theme}>` 包裹。

#### 模式三：单 HTML 文件（简单原型用）

仅适用于 Landing Page、简单原型等场景。用 React 18 UMD + Ant Design UMD + ECharts UMD。
参考 `references/antd-echarts-patterns.md`。

### Step 4: 启动开发服务器

```bash
cd project-name
npm install
npm run dev
```

部署时用 `npm run build` 生成 `dist/`。

## Figma 数据获取脚本

`scripts/figma_fetch.py` 通过 Figma REST API 获取文件结构和截图。

要求环境变量 `FIGMA_TOKEN` 已设置。

支持的链接格式：
- `https://www.figma.com/file/XXX/...`
- `https://www.figma.com/site/XXX/...`
- 仅 file key 字符串

输出：JSON 包含节点树、尺寸、颜色、字体、截图 URL。

## 组件文档参考

- Element Plus: https://element-plus.org/en-US/component/button.html
- Ant Design: https://ant.design/components/overview/
- ECharts: https://echarts.apache.org/en/option.html

## 已知限制

- Figma Community 文件（/site/ 路径）不能通过 API 获取完整节点树，只能获取截图。此时基于截图视觉分析生成代码
- MasterGo 需要 Team Edition 账号且文件在 Team Projects 中，Drafts 不可用
- 色彩映射是近似映射，可能需要人工微调

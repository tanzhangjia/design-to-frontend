# Ant Design + ECharts 单文件 HTML 模板模式

## 单文件 HTML 模板结构

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Title</title>
  <!-- React 18 + ReactDOM -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <!-- Ant Design 5.x ESM -->
  <script type="importmap">
  {
    "imports": {
      "antd": "https://unpkg.com/antd@5/dist/antd.min.js",
      "echarts": "https://unpkg.com/echarts@5/dist/echarts.min.js"
    }
  }
  </script>
  <!-- Babel standalone for JSX -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    /* Custom styles here */
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { ConfigProvider, Layout, Menu, Card, Button, Table, ... } = antd;
    const echarts = window.echarts;

    function App() {
      return (
        <ConfigProvider theme={{ token: { colorPrimary: '#...' } }}>
          {/* App content */}
        </ConfigProvider>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

## ECharts 在 React 中的用法

```javascript
// 用 useRef + useEffect 初始化
const chartRef = React.useRef(null);
const chartInstanceRef = React.useRef(null);

React.useEffect(() => {
  const chart = echarts.init(chartRef.current);
  chartInstanceRef.current = chart;

  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed'] },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: [120, 200, 150] }],
  });

  window.addEventListener('resize', () => chart.resize());

  return () => {
    window.removeEventListener('resize', () => chart.resize());
    chart.dispose();
  };
}, []);

return <div ref={chartRef} style={{ width: '100%', height: 400 }} />;
```

## 常用 ECharts 图表类型

| 类型 | type 值 | 适用场景 |
|------|---------|---------|
| 柱状图 | `bar` | 分类比较 |
| 折线图 | `line` | 趋势变化 |
| 饼图 | `pie` | 占比分布 |
| 散点图 | `scatter` | 相关性 |
| 雷达图 | `radar` | 多维度对比 |
| 仪表盘 | `gauge` | 进度/指标 |

## Ant Design 常用组件导入

```javascript
// 全部从命名空间导入
const { 
  ConfigProvider, Layout, Menu, Card, Button, Table, Form, 
  Input, Select, DatePicker, Tabs, Pagination, Statistic, 
  List, Modal, Drawer, Progress, Badge, Alert, Empty,
  Row, Col, Typography, Space, Divider, Tag, Avatar,
  InputNumber, Switch, Radio, Checkbox, Dropdown, Breadcrumb,
  message, notification,
} = antd;

const { Header, Content, Footer, Sider } = Layout;
const { Title, Text, Paragraph } = Typography;
```

## 常见布局模式

### Landing Page
```
Header (Logo + Navigation Menu)
Hero Section (背景大图 + 标题 + CTA按钮)
Features Section (3列Card)
Stats Section (4个Statistic)
Content Section (图文混排)
Testimonials (Card轮播)
Footer (链接 + 版权)
```

### Dashboard
```
Header (Logo + User Menu)
Sider (Menu导航)
Content:
  Row Row Row...
    Col: Statistic Card
    Col: Statistic Card
  Row:
    Col: ECharts Chart (span=12)
    Col: ECharts Chart (span=12)
  Row:
    Col: Ant Table (span=24)
Footer
```

## 响应式布局

```javascript
// Ant Design Row/Col 的响应式断点
<Row gutter={[24, 24]}>
  <Col xs={24} sm={12} md={8} lg={6} xl={6}>
    <Card>...</Card>
  </Col>
</Row>
```

断点：xs < 576px, sm ≥ 576, md ≥ 768, lg ≥ 992, xl ≥ 1200, xxl ≥ 1600

## 重要：使用 antd.min.js 简化方案（推荐）

为兼容 Babel + importmap，推荐直接用 antd 的 UMD 包（注意不是 ESM）：

```html
<script crossorigin src="https://unpkg.com/antd@5/dist/antd.min.js"></script>
```

这样 `antd` 会作为全局变量使用，不需要 importmap。

ECharts 同样用 UMD：
```html
<script src="https://unpkg.com/echarts@5/dist/echarts.min.js"></script>
```

⚠️ 使用 UMD 方案时，不要混用 importmap + babel/standalone 的 script type="text/babel"。
实际上更简单的方案：

```html
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/antd@5/dist/antd.min.js"></script>
<script src="https://unpkg.com/echarts@5/dist/echarts.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

<div id="root"></div>
<script type="text/babel">
const { ConfigProvider, Layout, Card, Row, Col, ... } = antd;
// ... use React hooks normally
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
```

这个方案最稳定，babel/standalone 会自动处理 JSX。

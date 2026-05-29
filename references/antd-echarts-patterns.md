# Ant Design + ECharts 单文件 HTML 模板模式

用于模式三（单 HTML 原型）的场景。

## HTML 模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Title</title>
  <!-- React 18 -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <!-- Ant Design 5.x UMD -->
  <script crossorigin src="https://unpkg.com/antd@5/dist/antd.min.js"></script>
  <!-- ECharts 5.x -->
  <script src="https://unpkg.com/echarts@5/dist/echarts.min.js"></script>
  <!-- Babel standalone for JSX -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    /* Custom styles */
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { ConfigProvider, Layout, Card, Row, Col, Button, Typography, Space, Tag } = antd;
    const { Header, Content, Footer } = Layout;
    const { Title, Text } = Typography;
    const echarts = window.echarts;

    function App() {
      return (
        <ConfigProvider theme={{ token: { colorPrimary: '#818cf8' } }}>
          {/* App content */}
        </ConfigProvider>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

## 常用 Ant Design 组件导入

```javascript
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

## ECharts 使用方式

```javascript
const chartRef = React.useRef(null);

React.useEffect(() => {
  const chart = echarts.init(chartRef.current);
  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed'] },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: [120, 200, 150] }],
  });

  const handleResize = () => chart.resize();
  window.addEventListener('resize', handleResize);

  return () => {
    window.removeEventListener('resize', handleResize);
    chart.dispose();
  };
}, []);

return <div ref={chartRef} style={{ width: '100%', height: 400 }} />;
```

## 响应式布局（Ant Design Row/Col）

```javascript
<Row gutter={[24, 24]}>
  <Col xs={24} sm={12} md={8} lg={6}>
    <Card>...</Card>
  </Col>
</Row>
```

断点：xs < 576, sm ≥ 576, md ≥ 768, lg ≥ 992, xl ≥ 1200, xxl ≥ 1600

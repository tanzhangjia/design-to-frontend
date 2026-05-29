# 部署指南

## 单文件 HTML 部署

```bash
# 写入 HTML 文件
cat > output.html << 'EOF'
...
EOF

# 启动静态文件服务器
npx http-server -p <port> --cors -c-1 -a 0.0.0.0
```

或者用 Python:
```bash
python3 -m http.server <port> --bind 0.0.0.0
```

## 后台运行

```bash
nohup npx http-server -p <port> --cors -c-1 -a 0.0.0.0 > /tmp/http-server.log 2>&1 &
```

## 防火墙

确保部署的端口已放行（云服务器安全组 / iptables）。

#!/usr/bin/env python3
"""飞书Webhook服务器 — 通过Tailscale Funnel接收飞书事件推送。"""
import json, os, sys, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """多线程HTTP服务器，避免单线程阻塞"""
    allow_reuse_address = True
    daemon_threads = True

INBOX = os.path.expanduser("~/.bridge/feishu_inbox.md")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """健康检查"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "service": "feishu webhook"}).encode())

    def _reply_json(self, code, body):
        try:
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())
        except:
            pass  # 客户端断开时忽略

    def do_POST(self):
        # 先读body
        try:
            length = int(self.headers.get('Content-Length', 0))
            body_data = self.rfile.read(length)
        except:
            body_data = b""

        # 立即返回200，防止飞书3秒超时
        self._reply_json(200, {"code": 0})

        # 后台异步处理
        if body_data:
            threading.Thread(target=self._process, args=(body_data,), daemon=True).start()

    def _process(self, body_data):
        try:
            data = json.loads(body_data.decode())

            # 飞书事件订阅验证
            if data.get('challenge'):
                return

            # 解析消息
            text = ""
            event = data.get('event', {})
            msg = event.get('message', {})
            if msg:
                content_str = msg.get('content', '{}')
                mtype = msg.get('message_type', '')
                try:
                    content = json.loads(content_str)
                    if mtype == 'text':
                        text = content.get('text', '')
                except:
                    text = content_str

            if text and text.strip():
                with open(INBOX, 'a') as f:
                    f.write(f"\n## [webhook] 飞书消息\n**内容**: {text.strip()}\n\n")
                print(f"[Webhook] 收到消息: {text.strip()[:50]}")
        except Exception as e:
            print(f"[Webhook] 处理出错: {e}")

    def log_message(self, format, *args):
        print(f"[Webhook] {args}")

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    server = ThreadedHTTPServer(('0.0.0.0', port), Handler)
    print(f"Webhook服务器运行在 :{port} (多线程模式)")
    server.serve_forever()

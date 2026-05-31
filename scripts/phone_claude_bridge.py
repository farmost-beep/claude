#!/usr/bin/env python3
"""Mobile-friendly web bridge to Claude Code — accessible from phone browser on same WiFi.

Usage:
  python3 scripts/phone_claude_bridge.py              # default port 9090
  python3 scripts/phone_claude_bridge.py --port 8888  # custom port
  python3 scripts/phone_claude_bridge.py --no-open    # don't open browser

Then on your phone, open: http://<mac-ip>:9090
"""

import subprocess, json, os, sys, html, re, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PORT = 9090
CLAUDE_BIN = "/opt/homebrew/bin/claude"
WORK_DIR = os.path.expanduser("~/claude")
MAX_HISTORY = 20

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>Claude Code</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Helvetica Neue",sans-serif;
  background:#1a1a2e;height:100dvh;display:flex;flex-direction:column}
header{background:#16213e;padding:10px 16px;text-align:center;color:#c9a96e;font-size:13px;font-weight:600;
  letter-spacing:0.5px;border-bottom:1px solid #0f3460;flex-shrink:0}
#messages{flex:1;overflow-y:auto;padding:12px;-webkit-overflow-scrolling:touch;
  display:flex;flex-direction:column;gap:10px}
.msg{max-width:90%;padding:10px 14px;border-radius:16px;font-size:14px;line-height:1.55;
  word-break:break-word;white-space:pre-wrap;animation:fadeIn 0.2s}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.msg.user{align-self:flex-end;background:#0f3460;color:#e8e8e8;border-bottom-right-radius:4px}
.msg.assistant{align-self:flex-start;background:#e8e8e8;color:#1a1a2e;border-bottom-left-radius:4px}
.msg.system{align-self:center;background:transparent;color:#888;font-size:12px;text-align:center}
.loading{display:flex;align-items:center;gap:8px;padding:10px 14px;color:#888;font-size:13px}
.spinner{width:16px;height:16px;border:2px solid #333;border-top-color:#c9a96e;border-radius:50%;
  animation:spin 0.7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#input-area{display:flex;gap:8px;padding:10px 12px;padding-bottom:max(10px,env(safe-area-inset-bottom));
  background:#16213e;border-top:1px solid #0f3460;flex-shrink:0}
#input-area textarea{flex:1;background:#1a1a2e;border:1px solid #0f3460;border-radius:12px;
  color:#e8e8e8;font-size:15px;padding:10px 14px;resize:none;min-height:42px;max-height:120px;
  font-family:inherit;outline:none}
#input-area textarea:focus{border-color:#c9a96e}
#input-area button{background:#c9a96e;color:#1a1a2e;border:none;border-radius:12px;padding:0 16px;
  font-size:14px;font-weight:600;cursor:pointer;min-width:52px}
#input-area button:active{opacity:0.8}
#input-area button:disabled{opacity:0.4}
code{background:rgba(0,0,0,0.08);padding:1px 5px;border-radius:4px;font-size:13px}
pre{background:rgba(0,0,0,0.08);padding:8px 10px;border-radius:8px;overflow-x:auto;font-size:12px;
  margin:6px 0}
</style>
</head>
<body>
<header>Claude Code</header>
<div id="messages"></div>
<div id="input-area">
  <textarea id="input" rows="1" placeholder="输入消息..." autofocus></textarea>
  <button id="send" onclick="doSend()">发送</button>
</div>
<script>
const msgs=document.getElementById("messages");
const input=document.getElementById("input");
const sendBtn=document.getElementById("send");
let loading=null;

function scrollBottom(){
  msgs.scrollTop=msgs.scrollHeight;
}

function addMsg(role,text){
  if(loading){loading.remove();loading=null;}
  const d=document.createElement("div");
  d.className="msg "+role;
  d.textContent=text;
  msgs.appendChild(d);
  scrollBottom();
}

function showLoading(){
  loading=document.createElement("div");
  loading.className="loading";
  loading.innerHTML='<div class="spinner"></div>思考中...';
  msgs.appendChild(loading);
  scrollBottom();
}

function escapeHtml(t){
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

async function doSend(){
  const text=input.value.trim();
  if(!text||sendBtn.disabled)return;
  addMsg("user",text);
  input.value="";
  input.style.height="auto";
  showLoading();
  sendBtn.disabled=true;
  try{
    const res=await fetch("/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:text})
    });
    const data=await res.json();
    if(loading){loading.remove();loading=null;}
    if(data.error){
      addMsg("system","错误: "+data.error);
    }else{
      addMsg("assistant",data.response);
    }
  }catch(e){
    if(loading){loading.remove();loading=null;}
    addMsg("system","连接失败: "+e.message);
  }
  sendBtn.disabled=false;
  input.focus();
}

input.addEventListener("keydown",e=>{
  if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();doSend();}
});
input.addEventListener("input",()=>{
  input.style.height="auto";
  input.style.height=Math.min(input.scrollHeight,120)+"px";
});
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress logs

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_html()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/chat":
            self._handle_chat()
        else:
            self.send_error(404)

    def _serve_html(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(HTML.encode())

    def _handle_chat(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            message = data.get("message", "").strip()
        except json.JSONDecodeError:
            self._json_reply({"error": "Invalid JSON"})
            return
        if not message:
            self._json_reply({"error": "Empty message"})
            return
        if len(message) > 4000:
            self._json_reply({"error": "Message too long (max 4000 chars)"})
            return

        try:
            # Run Claude CLI in one-shot mode
            proc = subprocess.run(
                [CLAUDE_BIN, "-p", message],
                cwd=WORK_DIR,
                capture_output=True,
                text=True,
                timeout=300,  # 5 min timeout
                env={**os.environ, "NO_COLOR": "1"},
            )
            response = proc.stdout.strip()
            if proc.returncode != 0 and not response:
                response = proc.stderr.strip() or f"(exit code {proc.returncode})"
        except subprocess.TimeoutExpired:
            response = "(请求超时，请尝试更简短的问题)"
        except FileNotFoundError:
            response = "(Claude CLI 未找到，请检查安装)"
        except Exception as e:
            response = f"(执行错误: {e})"

        self._json_reply({"response": response})

    def _json_reply(self, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def get_ip():
    """Get local network IP for user-friendly display."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    parser = argparse.ArgumentParser(description="Claude Code phone bridge")
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()

    ip = get_ip()
    url = f"http://{ip}:{args.port}"

    print(f"""
╔══════════════════════════════════════════╗
║     Claude Code Phone Bridge            ║
╠══════════════════════════════════════════╣
║  Mac:  {url:<32} ║
║                                          ║
║  在手机浏览器打开上方地址即可            ║
║  按 Ctrl+C 停止服务                      ║
╚══════════════════════════════════════════╝
""")

    server = HTTPServer(("0.0.0.0", args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
        server.server_close()


if __name__ == "__main__":
    main()

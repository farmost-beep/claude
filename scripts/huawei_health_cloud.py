#!/usr/bin/env python3
"""华为Health Kit Cloud API — 健康数据自动读取

用法:
  python3 scripts/huawei_health_cloud.py --auth      # 首次授权（手机扫码）
  python3 scripts/huawei_health_cloud.py --fetch     # 读取今日健康数据
  python3 scripts/huawei_health_cloud.py --fetch-all # 读取最近7天数据
"""

import os, sys, json, webbrowser, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs
from datetime import datetime, date, timedelta

import urllib.request

# 导入凭证
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from huawei_credentials import APP_ID, APP_SECRET, REDIRECT_URI

# 文件路径
TOKEN_FILE = os.path.expanduser("~/.huawei_health_token.json")
TRACKING_FILE = os.path.expanduser("~/claude/deliverables/health/路线图/华为手表数据.md")

# OAuth 端点
OAUTH_AUTHORIZE = "https://oauth-login.cloud.huawei.com/oauth2/v3/authorize"
OAUTH_TOKEN = "https://oauth-login.cloud.huawei.com/oauth2/v3/token"
HEALTH_API = "https://health-api.cloud.huawei.com/healthkit/v1"

# 数据范围
SCOPES = [
    "https://www.huawei.com/healthkit/steps.read",
    "https://www.huawei.com/healthkit/heartrate.read",
    "https://www.huawei.com/healthkit/sleep.read",
    "https://www.huawei.com/healthkit/bloodoxygen.read",
    "https://www.huawei.com/healthkit/heightweight.read",
    "https://www.huawei.com/healthkit/activity.read",
]
SCOPE_STR = " ".join(SCOPES)


# ─── OAuth 授权 ───────────────────────────────────────────────

class CallbackHandler(BaseHTTPRequestHandler):
    """捕获授权回调的简易HTTP服务器"""
    auth_code = None

    def do_GET(self):
        params = parse_qs(self.path.split("?")[-1])
        CallbackHandler.auth_code = params.get("code", [None])[0]
        if CallbackHandler.auth_code:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>OK</h1><p>Auth success! You can close this window.</p></body></html>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Fail</h1><p>No auth code received.</p></body></html>")

    def log_message(self, format, *args):
        pass  # 不打印HTTP日志


def do_auth():
    """首次授权：打开浏览器扫码 → 启动本地服务器接收回调"""
    print("\n🔑 华为Health Kit 首次授权")
    print("=" * 50)

    # 构建授权URL
    params = {
        "response_type": "code",
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE_STR,
    }
    auth_url = f"{OAUTH_AUTHORIZE}?{urlencode(params)}"

    # 启动本地服务器接收回调
    server = HTTPServer(("localhost", 8080), CallbackHandler)
    print(f"  1. 本地回调服务器已启动 (port 8080)")
    print(f"  2. 正在打开浏览器...")

    webbrowser.open(auth_url)

    print(f"  3. 如果浏览器未自动打开，请手动访问：")
    print(f"     {auth_url}")
    print(f"  4. 用**手机上的华为账号**登录并授权")
    print(f"\n  ⏳ 等待授权回调...")

    server.handle_request()  # 只处理一次请求

    code = CallbackHandler.auth_code
    if not code:
        print("  ❌ 未获取到授权码")
        return False

    print(f"  ✅ 获取到授权码，正在换取token...")

    # 交换 token
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    token_bytes = json.dumps(token_data).encode()
    req = urllib.request.Request(OAUTH_TOKEN, data=token_bytes,
                                 headers={"Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
    except Exception as e:
        print(f"  ❌ Token换取失败: {e}")
        return False

    # 保存token
    token_info = {
        "access_token": resp.get("access_token"),
        "refresh_token": resp.get("refresh_token"),
        "expires_in": resp.get("expires_in", 7200),
        "acquired_at": int(time.time()),
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_info, f, indent=2)
    print(f"  ✅ Token已保存到 {TOKEN_FILE}")
    print(f"  ⏳ 有效期: {token_info['expires_in']}秒 (约2小时)")
    print(f"\n🎉 授权完成！现在可以运行 --fetch 读取健康数据了。")
    return True


def refresh_access_token(refresh_token):
    """刷新access_token"""
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
    }
    req = urllib.request.Request(OAUTH_TOKEN,
                                  data=json.dumps(data).encode(),
                                  headers={"Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
        token_info = {
            "access_token": resp.get("access_token"),
            "refresh_token": resp.get("refresh_token", refresh_token),
            "expires_in": resp.get("expires_in", 7200),
            "acquired_at": int(time.time()),
        }
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_info, f, indent=2)
        return token_info["access_token"]
    except Exception as e:
        print(f"  ❌ Token刷新失败: {e}")
        return None


def get_token():
    """获取有效的access_token（自动刷新）"""
    if not os.path.exists(TOKEN_FILE):
        print("  ❌ 未找到token，请先运行 --auth")
        return None

    with open(TOKEN_FILE) as f:
        token_info = json.load(f)

    # 检查是否过期（留5分钟缓冲）
    elapsed = int(time.time()) - token_info.get("acquired_at", 0)
    if elapsed > token_info.get("expires_in", 7200) - 300:
        print("  ⏳ Token已过期，正在刷新...")
        return refresh_access_token(token_info.get("refresh_token"))

    return token_info.get("access_token")


def api_get(endpoint, access_token, params=None):
    """调用Health Kit REST API"""
    if params:
        url = f"{endpoint}?{urlencode(params)}"
    else:
        url = endpoint
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {access_token}",
        "x-client-id": APP_ID,
    })
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  ❌ API请求失败: {e.code} {e.read().decode()[:200]}")
        return None


# ─── 数据读取 ───────────────────────────────────────────────

def get_user_id(access_token):
    """获取用户ID（首次调用REST API时获取）"""
    resp = api_get(f"{HEALTH_API}/users/-/userInfo", access_token)
    if resp and "userId" in resp:
        return resp["userId"]
    return None


def get_steps(access_token, user_id, start_ms, end_ms):
    """读取步数数据"""
    resp = api_get(f"{HEALTH_API}/users/{user_id}/steps", access_token, {
        "startTime": start_ms, "endTime": end_ms
    })
    if resp and "steps" in resp:
        total = sum(int(s.get("count", 0)) for s in resp["steps"])
        return total
    return 0


def get_heart_rate(access_token, user_id, start_ms, end_ms):
    """读取心率数据"""
    resp = api_get(f"{HEALTH_API}/users/{user_id}/heartRate", access_token, {
        "startTime": start_ms, "endTime": end_ms
    })
    if resp and "heartRate" in resp:
        rates = [int(h.get("value", 0)) for h in resp["heartRate"] if h.get("value")]
        if rates:
            avg = sum(rates) // len(rates)
            return {"avg": avg, "min": min(rates), "max": max(rates)}
    return None


def get_sleep(access_token, user_id, start_ms, end_ms):
    """读取睡眠数据"""
    resp = api_get(f"{HEALTH_API}/users/{user_id}/sleep", access_token, {
        "startTime": start_ms, "endTime": end_ms
    })
    if resp and "sleep" in resp:
        total_minutes = sum(int(s.get("duration", 0)) for s in resp["sleep"]) // 60
        return total_minutes
    return 0


def get_blood_oxygen(access_token, user_id, start_ms, end_ms):
    """读取血氧数据"""
    resp = api_get(f"{HEALTH_API}/users/{user_id}/bloodOxygen", access_token, {
        "startTime": start_ms, "endTime": end_ms
    })
    if resp and "bloodOxygen" in resp:
        values = [int(b.get("value", 0)) for b in resp["bloodOxygen"] if b.get("value")]
        if values:
            return sum(values) // len(values)
    return None


# ─── 主流程 ───────────────────────────────────────────────

def ms_of_date(d):
    """将date对象转为毫秒级时间戳"""
    return int(d.timestamp() * 1000)


def fetch_health_data(access_token, user_id, start_date, end_date):
    """读取指定日期范围的健康数据"""
    start_ms = ms_of_date(start_date)
    end_ms = ms_of_date(end_date)

    print(f"  📊 读取 {start_date} ~ {end_date} 健康数据...")

    data = {}
    data["步数"] = get_steps(access_token, user_id, start_ms, end_ms)
    data["心率"] = get_heart_rate(access_token, user_id, start_ms, end_ms)
    data["睡眠"] = get_sleep(access_token, user_id, start_ms, end_ms)
    data["血氧"] = get_blood_oxygen(access_token, user_id, start_ms, end_ms)

    return data


def save_to_tracking(data, report_date=None):
    """写入追踪文件"""
    if not report_date:
        report_date = date.today()

    os.makedirs(os.path.dirname(TRACKING_FILE), exist_ok=True)

    with open(TRACKING_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n## {report_date}\n")
        f.write("| 指标 | 数值 | 来源 |\n")
        f.write("|------|------|------|\n")

        hr = data.get("心率")
        if hr:
            f.write(f"| 心率 | {hr['avg']}bpm (min={hr['min']} max={hr['max']}) | 华为Health Kit |\n")
        else:
            f.write(f"| 心率 | - | 华为Health Kit |\n")

        f.write(f"| 步数 | {data.get('步数', '-')} | 华为Health Kit |\n")

        sleep_h = data.get("睡眠", 0)
        if sleep_h > 0:
            f.write(f"| 睡眠 | {sleep_h//60}h{sleep_h%60}m | 华为Health Kit |\n")
        else:
            f.write(f"| 睡眠 | - | 华为Health Kit |\n")

        spo2 = data.get("血氧")
        if spo2:
            f.write(f"| 血氧 | {spo2}% | 华为Health Kit |\n")
        else:
            f.write(f"| 血氧 | - | 华为Health Kit |\n")

    print(f"  📝 已写入: {TRACKING_FILE}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "--auth":
        do_auth()
        return

    if cmd in ("--fetch", "--fetch-all"):
        print(f"\n🔍 华为Health Kit 数据读取")
        print("=" * 50)

        access_token = get_token()
        if not access_token:
            return

        user_id = get_user_id(access_token)
        if not user_id:
            print("  ❌ 无法获取用户ID，请检查授权状态")
            return
        print(f"  ✅ 用户ID: {user_id}")

        today = date.today()
        if cmd == "--fetch":
            dates = [today]
        else:
            dates = [today - timedelta(days=i) for i in range(7)]

        for day in dates:
            data = fetch_health_data(access_token, user_id, day, day + timedelta(days=1))
            if any(v for v in data.values()):
                save_to_tracking(data, day)
                print(f"  ✅ {day}: 步数={data['步数']} 心率={data['心率']} 睡眠={data['睡眠']} 血氧={data['血氧']}")
            else:
                print(f"  ⚠️ {day}: 无数据（手机可能未同步）")

        print(f"\n✅ 读取完成")
        return

    print(f"未知命令: {cmd}")
    print(__doc__)


if __name__ == "__main__":
    main()

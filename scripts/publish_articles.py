#!/usr/bin/env python3
"""自动发布文章到财新博客和微信公众号——增强版

功能:
  --preview      预览所有文章内容
  --caixin       发布到财新博客（支持cookie持久化，首次需手动登录）
  --wechat       发布到微信公众号（半自动，需扫码登录后自动填入）
  --all          发布到所有平台
  --status       查看所有文章发布状态
  --mark ID      标记某篇文章为已发布
  --schedule     根据发布计划设置cron定时任务
  --publish-plan 按发布计划执行当天应发布的文章
  --add-article  交互式添加新文章到配置

配置:
  文章配置: scripts/.publish_articles.json  （JSON格式，可手动编辑）
  发布状态: scripts/.publish_status.json    （自动维护）
  cookie:   scripts/.publish_cookies/       （自动保存）

依赖: playwright (pip3 install playwright && playwright install chromium)
"""

import os, sys, json, time, argparse, re
from pathlib import Path
from datetime import date, datetime

HEADLESS = False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = PROJECT_ROOT / "deliverables"
SCRIPTS_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPTS_DIR / ".publish_articles.json"
STATUS_FILE = SCRIPTS_DIR / ".publish_status.json"
COOKIE_DIR = SCRIPTS_DIR / ".publish_cookies"
CAIXIN_COOKIE = COOKIE_DIR / "caixin.json"

DEFAULT_ARTICLES = [
    {
        "id": 1,
        "title": "科技金融的第三条道路：从财务信用到技术信用的银行转型框架",
        "file": "career/发表文章/公众号文章_科技金融第三条道路_20260528.md",
        "tags_caixin": "金融,银行,科技金融,科创金融",
        "tags_wechat": "#科技金融 #银行转型 #科创金融 #信贷创新",
        "summary": "在国有大行靠规模碾压、互联网银行靠流量获客之外，科技金融是否存在第三条道路？本文提出五层生态位框架。",
        "plan_date_caixin": "2026-05-29",
        "plan_date_wechat": "2026-06-01",
        "platform": "both"
    },
    {
        "id": 2,
        "title": "含科量：一套让银行看得懂科技企业的评分体系",
        "file": "career/发表文章/公众号文章_含科量五维评分_20260528.md",
        "tags_caixin": "金融,银行,信用评估,科创企业",
        "tags_wechat": "#科技金融 #信用评估 #科创企业 #银行实务",
        "summary": "五维评分（研发强度、专利密度、技术壁垒、人才结构、产业位势）+TRL技术成熟度分层，将技术评估转化为可操作的信贷决策流程。",
        "plan_date_caixin": "2026-05-30",
        "plan_date_wechat": "2026-06-04",
        "platform": "both"
    },
    {
        "id": 3,
        "title": "万亿俱乐部：16家银行科技金融实力排名揭示了什么",
        "file": "career/发表文章/公众号文章_万亿俱乐部排名_20260528.md",
        "tags_caixin": "金融,银行,行业分析,数据报告",
        "tags_wechat": "#科技金融 #银行排名 #行业分析 #数据报告",
        "summary": "规模不等于能力：真正的科技金融竞争力体现在并购贷款深度、成长期企业占比和技术评价体系老练程度上。",
        "plan_date_caixin": "2026-05-31",
        "plan_date_wechat": "2026-06-08",
        "platform": "both"
    },
]


# ── 配置管理 ───────────────────────────────────────────

def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return DEFAULT_ARTICLES


def save_config(articles):
    CONFIG_FILE.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")


def load_status():
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    return {}


def save_status(status):
    STATUS_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_dir():
    os.makedirs(COOKIE_DIR, exist_ok=True)


# ── 内容读取与格式化 ────────────────────────────────────

def read_article_body(rel_path):
    full_path = DELIVERABLES / rel_path
    if not full_path.exists():
        print(f"  ✗ 文件不存在: {full_path}")
        return None
    with open(full_path, encoding="utf-8") as f:
        content = f.read()

    # Strip YAML frontmatter if present (only at the very top, between first two --- lines)
    if content.startswith("---"):
        second_sep = content.find("---", 3)
        if second_sep != -1:
            content = content[second_sep + 3:]

    # Find the first ## heading — body starts there
    body_start = content.find("\n## ")
    if body_start == -1:
        body_start = 0
    body = content[body_start:].strip()
    return body


def format_for_caixin(body):
    """财新博客格式：基础HTML兼容，表格转列表"""
    lines = body.split("\n")
    formatted = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                formatted.append("")
                in_table = True
            cells = [c.strip() for c in stripped.split("|") if c.strip()]
            if cells and not all(c.startswith("---") or c.startswith(":--") for c in cells):
                formatted.append("▪ " + " | ".join(cells))
            continue
        else:
            if in_table:
                formatted.append("")
                in_table = False

        if not stripped:
            formatted.append("")
            continue

        if stripped.startswith("## "):
            formatted.extend(["", stripped[3:], "─" * 30, ""])
        elif stripped.startswith("### "):
            formatted.extend(["", stripped[4:], "─" * 20, ""])
        elif stripped.startswith("**") and "**" in stripped[2:]:
            formatted.extend(["", stripped.strip("*"), ""])
        elif stripped.startswith("> "):
            formatted.append("  " + stripped[2:])
        else:
            formatted.append(stripped)

    return "\n".join(formatted)


def format_for_wechat_html(body):
    """Markdown转微信兼容HTML"""
    html_parts = ['<section style="font-size:16px;color:#333;line-height:1.8;letter-spacing:0.5px;">']

    lines = body.split("\n")
    in_table = False
    table_rows = []
    in_quote = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c.strip() for c in stripped.split("|") if c.strip()]
            if all(c.startswith("---") or c.startswith(":--") for c in cells):
                continue
            table_rows.append(cells)
            continue
        else:
            if in_table:
                html_parts.append('<table style="width:100%;border-collapse:collapse;font-size:14px;margin:10px 0;">')
                for row in table_rows:
                    html_parts.append("<tr>")
                    for cell in row:
                        html_parts.append(f'<td style="border:1px solid #ddd;padding:6px 8px;">{cell}</td>')
                    html_parts.append("</tr>")
                html_parts.append("</table>")
                in_table = False
                table_rows = []

        if not stripped:
            if in_quote:
                html_parts.append("</blockquote>")
                in_quote = False
            html_parts.append("<br/>")
            continue

        if stripped.startswith("## "):
            if in_quote:
                html_parts.append("</blockquote>")
                in_quote = False
            html_parts.append(f'<h2 style="font-size:20px;color:#1a3a5c;margin:20px 0 10px;border-left:4px solid #d4a853;padding-left:10px;">{stripped[3:]}</h2>')
        elif stripped.startswith("### "):
            if in_quote:
                html_parts.append("</blockquote>")
                in_quote = False
            html_parts.append(f'<h3 style="font-size:18px;color:#2a5a8c;margin:16px 0 8px;">{stripped[4:]}</h3>')
        elif stripped.startswith("#### "):
            html_parts.append(f'<h4 style="font-size:16px;color:#333;margin:12px 0 6px;font-weight:bold;">{stripped[5:]}</h4>')
        elif stripped.startswith("> "):
            if not in_quote:
                html_parts.append('<blockquote style="border-left:4px solid #d4a853;padding:8px 12px;margin:8px 0;background:#f9f7f2;color:#666;">')
                in_quote = True
            html_parts.append(f"<p>{stripped[2:]}</p>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            html_parts.append(f'<p style="margin:4px 0 4px 20px;">• {stripped[2:]}</p>')
        elif re.match(r'^\d+[\.\)]\s', stripped):
            content = re.sub(r'^\d+[\.\)]\s*', '', stripped)
            html_parts.append(f'<p style="margin:4px 0 4px 20px;">{content}</p>')
        elif stripped.startswith("**") and "**" in stripped[2:]:
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            html_parts.append(f'<p style="margin:8px 0;font-weight:bold;">{text}</p>')
        else:
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            html_parts.append(f"<p>{text}</p>")

    if in_quote:
        html_parts.append("</blockquote>")
    html_parts.append("</section>")
    return "\n".join(html_parts)


def get_word_count(body):
    return len(body.replace("\n", "").replace(" ", ""))


# ── 发布状态管理 ─────────────────────────────────────────

def get_article_status(article_id):
    status = load_status()
    key = str(article_id)
    return status.get(key, {"caixin": "draft", "wechat": "draft"})


def mark_published(article_id, platform):
    status = load_status()
    key = str(article_id)
    if key not in status:
        status[key] = {"caixin": "draft", "wechat": "draft"}
    status[key][platform] = "published"
    status[key][f"{platform}_date"] = date.today().isoformat()
    save_status(status)
    print(f"  ✓ 文章 [{article_id}] {platform} 已标记为已发布")


def show_status():
    articles = load_config()
    status = load_status()

    print("\n文章发布状态总览\n" + "=" * 60)
    for a in articles:
        s = status.get(str(a["id"]), {"caixin": "draft", "wechat": "draft"})
        c_date = s.get("caixin_date", "-")
        w_date = s.get("wechat_date", "-")

        c_icon = "✅" if s.get("caixin") == "published" else "⬜"
        w_icon = "✅" if s.get("wechat") == "published" else "⬜"

        print(f"\n  [{a['id']}] {a['title'][:40]}...")
        print(f"      财新: {c_icon} {s.get('caixin', 'draft'):>9}  {c_date}")
        print(f"      公众号: {w_icon} {s.get('wechat', 'draft'):>9}  {w_date}")

    print(f"\n共 {len(articles)} 篇文章")

    # 检查今天是否应按计划发布
    today = date.today().isoformat()
    due_today = []
    for a in articles:
        s = status.get(str(a["id"]), {})
        if a.get("plan_date_caixin") == today and s.get("caixin") != "published":
            due_today.append((a["id"], "caixin", a["title"][:30]))
        if a.get("plan_date_wechat") == today and s.get("wechat") != "published":
            due_today.append((a["id"], "wechat", a["title"][:30]))

    if due_today:
        print(f"\n📅 今天({today})应发布:")
        for aid, plat, title in due_today:
            print(f"  [{aid}] {plat}: {title}...")
    else:
        print(f"\n📅 今天({today})无待发布文章")


# ── 发布到财新博客 ──────────────────────────────────────

def publish_caixin(article_ids=None):
    ensure_dir()
    from playwright.sync_api import sync_playwright

    articles = load_config()
    targets = [a for a in articles if article_ids is None or a["id"] in article_ids]
    targets = [a for a in targets if get_article_status(a["id"]).get("caixin") != "published"]

    if not targets:
        print("所有选择的文章已在财新发布")
        return

    print(f"\n{'='*60}")
    print(f"财新博客发布: {len(targets)} 篇待发")
    print(f"{'='*60}")

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=HEADLESS, channel="chrome" if not HEADLESS else None)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 900}, locale="zh-CN",
        storage_state=CAIXIN_COOKIE if CAIXIN_COOKIE.exists() else None,
    )
    page = ctx.new_page()

    try:
        page.goto("https://blog.caixin.com")
        time.sleep(2)

        if "login" in page.url.lower() or "登录" in page.title():
            print("\n  ⚠️ 需要登录财新博客，请在浏览器中完成登录")
            page.goto("https://blog.caixin.com/login")
            try:
                page.wait_for_url(lambda u: "blog.caixin.com" in u and "login" not in u.lower(), timeout=120000)
                ctx.storage_state(path=CAIXIN_COOKIE)
                print("  ✓ 登录成功，session已保存")
            except:
                print("  ⚠️ 登录超时，请确保已登录后重试")
                return
        else:
            print("  ✓ 已登录")

        for article in targets:
            print(f"\n  [{article['id']}] {article['title'][:40]}")
            body = read_article_body(article["file"])
            if not body:
                continue

            formatted = format_for_caixin(body)
            print(f"      字数: ~{get_word_count(formatted)}")

            page.goto("https://blog.caixin.com/write")
            time.sleep(2)

            title_input = page.locator("input[placeholder*='标题'], #title, .title-input").first
            if title_input.count() > 0:
                title_input.fill(article["title"])
                print("  ✓ 标题已填入")

            content_area = page.locator("textarea, .ql-editor, [contenteditable='true'], #content").first
            if content_area.count() > 0:
                content_area.fill(formatted)
                print("  ✓ 正文已填入")

            tag_input = page.locator("input[placeholder*='标签'], .tag-input, #tags").first
            if tag_input.count() > 0:
                tag_input.fill(article.get("tags_caixin", ""))

            print(f"  📌 请在浏览器中检查内容并点击发布")
            print(f"  📌 发布后运行: python3 scripts/publish_articles.py --mark {article['id']} caixin")

        print(f"\n  等待发布完成...关闭浏览器窗口后继续")
        page.wait_for_event('close', timeout=600000)

    finally:
        browser.close()
        p.stop()


# ── 发布到微信公众号 ─────────────────────────────────────

def publish_wechat(article_ids=None):
    ensure_dir()
    from playwright.sync_api import sync_playwright

    articles = load_config()
    targets = [a for a in articles if article_ids is None or a["id"] in article_ids]
    targets = [a for a in targets if get_article_status(a["id"]).get("wechat") != "published"]

    if not targets:
        print("所有选择的文章已在微信公众号发布")
        return

    print(f"\n{'='*60}")
    print(f"微信公众号发布: {len(targets)} 篇待发")
    print(f"{'='*60}")

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False, channel="chrome")
    ctx = browser.new_context(viewport={"width": 1280, "height": 900}, locale="zh-CN")
    page = ctx.new_page()

    try:
        page.goto("https://mp.weixin.qq.com")
        print("\n  ⚠️ 请扫码登录微信公众号")
        try:
            page.wait_for_url(lambda u: "mp.weixin.qq.com" in u and "token=" in u, timeout=300000)
            print("  ✓ 登录成功")
        except:
            print("  ⚠️ 登录超时")
            return

        for article in targets:
            print(f"\n  [{article['id']}] {article['title'][:40]}")
            body = read_article_body(article["file"])
            if not body:
                continue

            html_body = format_for_wechat_html(body)
            print(f"      字数: ~{get_word_count(body)}")

            # 打开首页，用户手动进入编辑器
            page.goto("https://mp.weixin.qq.com/cgi-bin/home?t=home/index")
            time.sleep(3)

            # 保存HTML备用
            tmp = SCRIPTS_DIR / f"_wechat_article_{article['id']}.html"
            tmp.write_text(html_body, encoding="utf-8")
            print(f"  📁 HTML文件已生成: {tmp}")

            print(f"")
            print(f"  ┌─────────────────────────────────────────┐")
            print(f"  │  请按以下步骤手动操作：                    │")
            print(f"  │  1. 在浏览器中点击「新建图文」              │")
            print(f"  │  2. 标题填入：                            │")
            print(f"  │     {article['title'][:35]}...            │")
            print(f"  │  3. 正文：打开下方HTML文件，全选复制         │")
            print(f"  │     粘贴到编辑器（Ctrl+V）                  │")
            print(f"  │  4. 调整格式后保存/群发                     │")
            print(f"  └─────────────────────────────────────────┘")
            print(f"")
            print(f"  📌 发布后运行: python3 scripts/publish_articles.py --mark {article['id']} wechat")
            print(f"  ⏸  浏览器保持打开5分钟...")
            time.sleep(300)

        print(f"\n  全部 {len(targets)} 篇文章已填入编辑器")

    finally:
        browser.close()
        p.stop()


# ── Cron定时发布 ─────────────────────────────────────────

def setup_cron_schedule():
    """根据发布计划中的日期设置cron定时提醒"""
    articles = load_config()
    status = load_status()
    today = date.today().isoformat()

    print(f"\n检查发布计划 (今天: {today})\n" + "=" * 60)

    upcoming = []
    for a in articles:
        for plat, date_key in [("caixin", "plan_date_caixin"), ("wechat", "plan_date_wechat")]:
            plan_date = a.get(date_key)
            if not plan_date:
                continue
            s = status.get(str(a["id"]), {})
            if s.get(plat) == "published":
                continue
            if plan_date >= today:
                upcoming.append((plan_date, a["id"], plat, a["title"][:30], a.get("summary", "")[:60]))

    upcoming.sort()

    if not upcoming:
        print("\n所有文章已发布或已过计划日期，无需设置定时任务")
        return

    print("\n待发布文章:")
    for plan_date, aid, plat, title, _ in upcoming:
        days_until = (date.fromisoformat(plan_date) - date.today()).days
        print(f"  {plan_date} ({days_until}天后) [{aid}] {plat}: {title}")

    # 为每个即将到来的发布日期设置提醒
    # 在发布前一天晚上20:00提醒准备，发布当天8:00提醒执行
    scheduled_dates = set()
    for plan_date, aid, plat, title, summary in upcoming:
        if plan_date in scheduled_dates:
            continue
        scheduled_dates.add(plan_date)

        y, m, d = plan_date.split("-")
        cron_day = f"{int(d)}"
        cron_month = f"{int(m)}"

        # 提前一天提醒准备
        prep_y, prep_m, prep_d = plan_date.split("-")
        from datetime import timedelta
        prep_date = date.fromisoformat(plan_date) - timedelta(days=1)
        cron_prep_d = f"{prep_date.day}"
        cron_prep_m = f"{prep_date.month}"

        # 当天8:00提醒
        prompt = f"今天({plan_date})应发布文章到{'财新和公众号' if plat == 'both' else plat}。运行: python3 scripts/publish_articles.py --publish-plan。文章: {title}"
        cron_expr = f"0 8 {cron_day} {cron_month} *"
        print(f"\n  建议cron: {cron_expr}")
        print(f"    {prompt}")

    print(f"\n💡 要自动设置这些cron提醒，运行:")
    print(f"   python3 scripts/publish_articles.py --schedule  (当前版本：显示计划)")
    print(f"\n💡 手动发布当天文章:")
    print(f"   python3 scripts/publish_articles.py --publish-plan")


def publish_plan_today():
    """按发布计划发布今天的文章"""
    today = date.today().isoformat()
    articles = load_config()
    status = load_status()

    due = []
    for a in articles:
        s = status.get(str(a["id"]), {})
        if a.get("plan_date_caixin") == today and s.get("caixin") != "published":
            due.append(("caixin", a))
        if a.get("plan_date_wechat") == today and s.get("wechat") != "published":
            due.append(("wechat", a))

    if not due:
        print(f"今天({today})没有待发布的文章")
        return

    print(f"今天({today})待发布 {len(due)} 篇:")
    for plat, a in due:
        print(f"  [{a['id']}] {plat}: {a['title'][:40]}")

    caixin_ids = [a["id"] for plat, a in due if plat == "caixin"]
    wechat_ids = [a["id"] for plat, a in due if plat == "wechat"]

    if caixin_ids:
        print("\n▶ 开始发布财新博客...")
        publish_caixin(list(set(caixin_ids)))

    if wechat_ids:
        print("\n▶ 开始发布微信公众号...")
        publish_wechat(list(set(wechat_ids)))

    # 发布完成后推送微信通知
    notify_publish_complete(due)


def notify_publish_complete(published):
    """发布完成后推送微信通知"""
    if not published:
        return
    push_script = SCRIPTS_DIR / "wechat_push.py"
    if not push_script.exists():
        return

    today_str = date.today().strftime("%Y年%m月%d日")
    parts = [f"## 文章发布通知 | {today_str}\n"]
    for plat, a in published:
        parts.append(f"- [{plat}] {a['title'][:30]}...")
    parts.append(f"\n总计 {len(published)} 篇")

    import subprocess
    try:
        subprocess.run(
            ["python3", str(push_script), f"文章发布 | {today_str}", "\n".join(parts)],
            capture_output=True, timeout=15,
        )
    except:
        pass


# ── 交互式添加文章 ───────────────────────────────────────

def add_article_interactive():
    articles = load_config()
    new_id = max(a["id"] for a in articles) + 1 if articles else 1

    print(f"\n添加新文章 (ID: {new_id})")
    print("=" * 40)
    title = input("标题: ").strip()
    if not title:
        print("取消")
        return

    file_path = input("文章文件路径 (相对于deliverables/): ").strip()
    tags_c = input("财新标签 (逗号分隔): ").strip()
    tags_w = input("公众号标签 (#分隔): ").strip()
    summary = input("摘要: ").strip()
    plan_c = input("财新计划日期 (YYYY-MM-DD): ").strip()
    plan_w = input("公众号计划日期 (YYYY-MM-DD): ").strip()

    articles.append({
        "id": new_id,
        "title": title,
        "file": file_path,
        "tags_caixin": tags_c,
        "tags_wechat": tags_w,
        "summary": summary,
        "plan_date_caixin": plan_c,
        "plan_date_wechat": plan_w,
        "platform": "both",
    })

    save_config(articles)
    print(f"✓ 文章 [{new_id}] 已添加到配置 {CONFIG_FILE}")


# ── 主入口 ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="自动发布文章到财新博客和微信公众号")
    parser.add_argument("--caixin", action="store_true", help="发布到财新博客")
    parser.add_argument("--wechat", action="store_true", help="发布到微信公众号")
    parser.add_argument("--all", action="store_true", help="发布到所有平台")
    parser.add_argument("--status", action="store_true", help="查看发布状态")
    parser.add_argument("--preview", action="store_true", help="预览文章")
    parser.add_argument("--mark", nargs=2, metavar=("ID", "PLATFORM"), help="标记文章已发布 (例: --mark 1 caixin)")
    parser.add_argument("--schedule", action="store_true", help="查看/设置发布计划的cron定时")
    parser.add_argument("--publish-plan", action="store_true", help="按发布计划执行今天应发布的文章")
    parser.add_argument("--add-article", action="store_true", help="交互式添加新文章")
    parser.add_argument("--article", type=int, nargs="*", help="指定文章ID")
    args = parser.parse_args()

    # --status
    if args.status:
        show_status()
        return

    # --mark
    if args.mark:
        aid, platform = int(args.mark[0]), args.mark[1].lower()
        if platform not in ("caixin", "wechat"):
            print("平台必须是 caixin 或 wechat")
            sys.exit(1)
        mark_published(aid, platform)
        return

    # --schedule
    if args.schedule:
        setup_cron_schedule()
        return

    # --publish-plan
    if args.publish_plan:
        publish_plan_today()
        return

    # --add-article
    if args.add_article:
        add_article_interactive()
        return

    # --preview
    if args.preview:
        articles = load_config()
        targets = [a for a in articles if args.article is None or a["id"] in args.article]
        print(f"\n预览 {len(targets)} 篇文章\n")
        for a in targets:
            body = read_article_body(a["file"])
            wc = get_word_count(body) if body else 0
            s = get_article_status(a["id"])
            print(f"  [{a['id']}] {a['title']}")
            print(f"      字数: ~{wc}  | 财新: {s.get('caixin')} | 公众号: {s.get('wechat')}")
            print(f"      财新计划: {a.get('plan_date_caixin', '-')} | 公众号计划: {a.get('plan_date_wechat', '-')}")
            print(f"      文件: {DELIVERABLES / a['file']}")
            print()

        if not targets:
            print("没有匹配的文章")
        return

    # 发布操作
    if args.caixin or args.wechat or args.all:
        if args.caixin or args.all:
            publish_caixin(args.article)
        if args.wechat or args.all:
            publish_wechat(args.article)
        return

    # 无参数：显示帮助
    print("文章自动发布管道 v2.0")
    print("=" * 50)
    print("\n常用命令:")
    print("  查看状态:    python3 scripts/publish_articles.py --status")
    print("  预览文章:    python3 scripts/publish_articles.py --preview")
    print("  查看计划:    python3 scripts/publish_articles.py --schedule")
    print("  今日发布:    python3 scripts/publish_articles.py --publish-plan")
    print("  发布财新:    python3 scripts/publish_articles.py --caixin")
    print("  发布公众号:  python3 scripts/publish_articles.py --wechat")
    print("  标记已发:    python3 scripts/publish_articles.py --mark <ID> caixin")
    print("  添加文章:    python3 scripts/publish_articles.py --add-article")
    print("\n首次使用:")
    print("  1. pip3 install playwright && playwright install chromium")
    print("  2. python3 scripts/publish_articles.py --preview  # 查看待发布内容")
    print("  3. python3 scripts/publish_articles.py --caixin   # 首次需手动登录")


if __name__ == "__main__":
    main()

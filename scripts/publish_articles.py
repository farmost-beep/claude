#!/usr/bin/env python3
"""自动发布科技金融方法论三部曲到财新博客和微信公众号

用法:
  # 首次运行（需要手动登录，登录后cookie保存在本地）
  python3 scripts/publish_articles.py --first-run

  # 后续运行（自动发布）
  python3 scripts/publish_articles.py [--caixin] [--wechat] [--all]

  # 只准备内容（不发布，打开浏览器预览）
  python3 scripts/publish_articles.py --preview

依赖: playwright (pip3 install playwright && playwright install chromium)
"""

import os, sys, json, time, argparse
from pathlib import Path

HEADLESS = False  # 首次运行时设为False以便登录

ARTICLES = [
    {
        "id": 1,
        "title": "科技金融的第三条道路：从财务信用到技术信用的银行转型框架",
        "file": "career/发表文章/公众号文章_科技金融第三条道路_20260528.md",
        "tags": "#科技金融 #银行转型 #科创金融 #信贷创新",
        "summary": "在国有大行靠规模碾压、互联网银行靠流量获客之外，科技金融是否存在第三条道路？本文提出'五层生态位'框架。",
    },
    {
        "id": 2,
        "title": "含科量：一套让银行看得懂科技企业的评分体系",
        "file": "career/发表文章/公众号文章_含科量五维评分_20260528.md",
        "tags": "#科技金融 #信用评估 #科创企业 #银行实务",
        "summary": "五维评分（研发强度、专利密度、技术壁垒、人才结构、产业位势）+ TRL技术成熟度分层，将技术评估转化为可操作的信贷决策流程。",
    },
    {
        "id": 3,
        "title": "万亿俱乐部：16家银行科技金融实力排名揭示了什么",
        "file": "career/发表文章/公众号文章_万亿俱乐部排名_20260528.md",
        "tags": "#科技金融 #银行排名 #行业分析 #数据报告",
        "summary": "规模不等于能力：真正的科技金融竞争力体现在并购贷款深度、成长期企业占比和技术评价体系老练程度上。",
    },
]

DELIVERABLES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deliverables")
COOKIE_DIR = os.path.join(os.path.dirname(__file__), ".publish_cookies")
CAIXIN_COOKIE = os.path.join(COOKIE_DIR, "caixin.json")


def ensure_dir():
    os.makedirs(COOKIE_DIR, exist_ok=True)


def read_article_body(rel_path):
    """从markdown文件读取正文（去掉YAML front matter和标题）"""
    full_path = os.path.join(DELIVERABLES, rel_path)
    if not os.path.exists(full_path):
        print(f"  ERROR: 文件不存在 {full_path}")
        return None

    with open(full_path) as f:
        lines = f.readlines()

    # 找到正文起点（跳过标题行#和元信息blockquote）
    body_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            body_start = i
            break

    # 去掉最后的"---"分隔线和文末信息
    body = lines[body_start:]
    # 去掉"---"分隔线后的内容（"编制"等）
    cleaned = []
    in_meta = False
    for line in body:
        if line.strip() == "---":
            in_meta = not in_meta
            continue
        if not in_meta:
            cleaned.append(line)

    return "".join(cleaned).strip()


def format_for_caixin(body):
    """格式化为财新博客兼容的格式

    财新博客编辑器支持基础HTML，将Markdown转为HTML样式的文本
    """
    lines = body.split("\n")
    formatted = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        # 表格 → 财新不支持复杂表格，转为纯文本列表
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                formatted.append("")
                in_table = True
            cells = [c.strip() for c in stripped.split("|") if c.strip()]
            if cells:
                formatted.append("▪ " + " | ".join(cells))
            continue
        else:
            if in_table:
                formatted.append("")
                in_table = False

        if not stripped:
            formatted.append("")
            continue

        # 标题
        if stripped.startswith("## "):
            formatted.extend(["", stripped[3:], "─" * 30, ""])
        elif stripped.startswith("### "):
            formatted.extend(["", stripped[4:], "─" * 20, ""])
        elif stripped.startswith("**") and stripped.endswith("**"):
            formatted.extend(["", stripped.strip("*"), ""])
        elif stripped.startswith("> "):
            formatted.append("📌 " + stripped[2:])
        else:
            formatted.append(stripped)

    return "\n".join(formatted)


def get_browser():
    """获取Playwright浏览器实例"""
    from playwright.sync_api import sync_playwright

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=HEADLESS, channel="chrome" if not HEADLESS else None)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 900},
        locale="zh-CN",
    )
    return p, browser, ctx


def publish_caixin(article_ids=None):
    """发布到财新博客 blog.caixin.com"""
    ensure_dir()
    from playwright.sync_api import sync_playwright

    targets = [a for a in ARTICLES if article_ids is None or a["id"] in article_ids]
    if not targets:
        print("没有选择文章")
        return

    print(f"\n准备发布 {len(targets)} 篇到财新博客:")
    for a in targets:
        print(f"  [{a['id']}] {a['title'][:30]}...")

    # 启动浏览器
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=HEADLESS, channel="chrome" if not HEADLESS else None)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 900},
        locale="zh-CN",
        storage_state=CAIXIN_COOKIE if os.path.exists(CAIXIN_COOKIE) else None,
    )
    page = ctx.new_page()

    try:
        # 打开财新博客
        page.goto("https://blog.caixin.com")
        time.sleep(2)

        # 检查是否需要登录
        if page.url.startswith("https://blog.caixin.com/login") or "登录" in page.title():
            print("\n  ⚠️ 需要登录财新博客")
            print("  请在打开的浏览器中手动登录，登录后脚本将自动继续...")
            page.goto("https://blog.caixin.com/login")
            page.wait_for_url(lambda url: "blog.caixin.com" in url and "login" not in url.lower(),
                              timeout=120000)
            print("  ✅ 登录成功，保存session...")
            ctx.storage_state(path=CAIXIN_COOKIE)
        else:
            print("  ✅ 已登录")

        for article in targets:
            print(f"\n  发布 [{article['id']}] {article['title'][:20]}...")
            body = read_article_body(article["file"])
            if not body:
                continue

            formatted = format_for_caixin(body)

            # 财新博客"写文章"页面
            page.goto("https://blog.caixin.com/write")
            time.sleep(2)

            # 填写标题
            title_input = page.locator("input[placeholder*='标题'], #title, .title-input")
            if title_input.count() > 0:
                title_input.fill(article["title"])
                print("  ✅ 标题已填写")

            # 填写正文 - 财新编辑器通常是textarea或contenteditable
            content_area = page.locator("textarea, .ql-editor, [contenteditable='true'], #content")
            if content_area.count() > 0:
                content_area.fill(formatted)
                print("  ✅ 正文已填写")

            # 填写标签
            tag_input = page.locator("input[placeholder*='标签'], .tag-input")
            if tag_input.count() > 0:
                tag_input.fill(article["tags"])

            # 填写摘要
            summary_input = page.locator("textarea[placeholder*='摘要'], input[placeholder*='摘要'], #summary")
            if summary_input.count() > 0:
                summary_input.fill(article["summary"])

            print("  ✅ 内容已填入，请在浏览器中检查并点击发布")
            print(f"  📌 发布地址: https://blog.caixin.com/write")

        print(f"\n✅ 所有内容已填入浏览器窗口，请在页面中点击发布按钮。")
        print("   关闭浏览器窗口后脚本退出。")
        page.wait_for_close(timeout=300000)

    finally:
        browser.close()
        p.stop()


def preview_articles(article_ids=None):
    """在浏览器中预览所有文章"""
    targets = [a for a in ARTICLES if article_ids is None or a["id"] in article_ids]

    print(f"\n预览 {len(targets)} 篇文章:\n")
    for a in targets:
        body = read_article_body(a["file"])
        word_count = len(body) if body else 0
        print(f"  [{a['id']}] {a['title']}")
        print(f"      字数: ~{word_count} | 标签: {a['tags']}")
        print(f"      摘要: {a['summary'][:40]}...")
        print()

    print("文件路径:")
    for a in targets:
        full = os.path.join(DELIVERABLES, a["file"])
        print(f"  [{a['id']}] {full}")


def publish_wechat(article_ids=None):
    """发布到微信公众号 (mp.weixin.qq.com)

    微信公众平台有反自动化机制，采用半自动模式：
    1. 打开浏览器到微信公众平台
    2. 用户手动登录
    3. 自动填入文章内容
    4. 用户手动调整格式后发布
    """
    ensure_dir()
    from playwright.sync_api import sync_playwright

    targets = [a for a in ARTICLES if article_ids is None or a["id"] in article_ids]

    print(f"\n准备发布 {len(targets)} 篇到微信公众号:")
    for a in targets:
        print(f"  [{a['id']}] {a['title'][:30]}...")

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False, channel="chrome")
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 900},
        locale="zh-CN",
    )
    page = ctx.new_page()

    try:
        page.goto("https://mp.weixin.qq.com")
        print("\n  ⚠️ 请手动扫码登录微信公众号")
        print("  登录后脚本将自动继续...")
        page.wait_for_url(lambda url: "mp.weixin.qq.com" in url and "token=" in url,
                          timeout=120000)
        print("  ✅ 登录成功")

        for article in targets:
            print(f"\n  发布 [{article['id']}] {article['title'][:20]}...")
            body = read_article_body(article["file"])
            if not body:
                continue

            # 进入新建图文素材
            page.goto("https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1")
            time.sleep(3)

            # 填写标题
            title_input = page.locator("#title, input[placeholder*='标题']")
            if title_input.count() > 0:
                title_input.fill(article["title"])

            # 微信编辑器是iframe，需要切换到富文本编辑区
            try:
                editor_frame = page.frame_locator("iframe").first
                editor_area = editor_frame.locator("#js_editor_rich_content, .rich_media_area_extra")
                if editor_area.count() > 0:
                    # 格式化正文为简单的HTML
                    html_body = body.replace("\n", "<br>")
                    # 处理标题
                    import re
                    html_body = re.sub(r'## (.+)', r'<h2>\1</h2>', html_body)
                    html_body = re.sub(r'### (.+)', r'<h3>\1</h3>', html_body)
                    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
                    editor_area.evaluate(f"elem => elem.innerHTML = `{html_body}`")
            except Exception as e:
                print(f"  ⚠️ 编辑器填充失败: {e}")
                print(f"  请手动粘贴内容。正文已准备好。")

            # 填写摘要
            abstract_input = page.locator("#abstract, textarea[placeholder*='摘要'], input[placeholder*='摘要']")
            if abstract_input.count() > 0:
                abstract_input.fill(article["summary"])

            print(f"  ✅ 内容已填入，请在浏览器中检查和发布")
            print(f"  📌 当前文章: {article['title']}")

        print(f"\n✅ 所有 {len(targets)} 篇内容已填入浏览器窗口。")
        print("   请在微信公众号编辑器中调整格式后保存/群发。")
        print("   关闭浏览器后脚本退出。")
        page.wait_for_close(timeout=300000)

    finally:
        browser.close()
        p.stop()


def main():
    parser = argparse.ArgumentParser(description="自动发布科技金融方法论三部曲")
    parser.add_argument("--first-run", action="store_true", help="首次运行，仅登录财新博客保存cookie")
    parser.add_argument("--caixin", action="store_true", help="发布到财新博客")
    parser.add_argument("--wechat", action="store_true", help="发布到微信公众号")
    parser.add_argument("--all", action="store_true", help="发布到所有平台")
    parser.add_argument("--preview", action="store_true", help="预览文章内容")
    parser.add_argument("--article", type=int, nargs="*", choices=[1, 2, 3],
                        help="指定文章ID（默认全部）")
    args = parser.parse_args()

    if args.preview:
        preview_articles(args.article)
        return

    if args.first_run:
        ensure_dir()
        print("首次运行：登录财新博客并保存session")
        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False, channel="chrome")
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 900}, locale="zh-CN",
        )
        page = ctx.new_page()
        print("\n请在打开的浏览器中登录 blog.caixin.com")
        print("登录后关闭浏览器，session将自动保存\n")
        page.goto("https://blog.caixin.com/login")
        try:
            page.wait_for_url(lambda url: "blog.caixin.com" in url and "login" not in url.lower(),
                              timeout=120000)
            ctx.storage_state(path=CAIXIN_COOKIE)
            print(f"✅ Session已保存到 {CAIXIN_COOKIE}")
        except:
            print("⚠️ 未检测到登录成功，请确保已登录")
        finally:
            browser.close()
            p.stop()
        return

    if args.caixin or args.wechat or args.all:
        if args.caixin or args.all:
            publish_caixin(args.article)
        if args.wechat or args.all:
            publish_wechat(args.article)
        return

    print("请指定操作：--preview / --first-run / --caixin / --wechat / --all")
    print("示例:")
    print("  首次登录: python3 scripts/publish_articles.py --first-run")
    print("  发布到财新: python3 scripts/publish_articles.py --caixin")
    print("  发布全部: python3 scripts/publish_articles.py --all")
    print("  预览: python3 scripts/publish_articles.py --preview")


if __name__ == "__main__":
    main()

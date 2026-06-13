#!/usr/bin/env python3
"""
微信通讯录自动同步脚本
用途：监控微信下载目录中的VCF/联系人导出文件，自动合并到主库
触发方式：手动运行 / 定时任务
"""

import json, os, re, quopri, sys, time
from pathlib import Path
from datetime import datetime

# 配置
MAIN_DB = Path(os.path.expanduser("~/Documents/ClaudeCode/主库/社交关系/contacts.json"))
WECHAT_FILE_DIRS = [
    Path(os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files")),
    Path(os.path.expanduser("~/Downloads")),
]
SCANNED_LOG = Path(os.path.expanduser("~/.claude/skills/social-agent/data/scanned_vcf.log"))

def get_scanned():
    """读取已扫描的VCF文件列表"""
    if SCANNED_LOG.exists():
        return set(SCANNED_LOG.read_text().strip().split('\n'))
    return set()

def mark_scanned(filepath):
    """标记VCF文件为已扫描"""
    scanned = get_scanned()
    scanned.add(str(filepath))
    SCANNED_LOG.parent.mkdir(parents=True, exist_ok=True)
    SCANNED_LOG.write_text('\n'.join(sorted(scanned)))

def parse_vcf(filepath):
    """解析VCF文件，返回联系人列表"""
    raw = filepath.read_bytes()
    try:
        text = raw.decode('utf-8')
    except:
        text = raw.decode('utf-8', errors='replace')

    blocks = text.split('END:VCARD\r\n')
    contacts = []
    for block in blocks:
        if 'BEGIN:VCARD' not in block:
            continue
        name = ''
        phone = ''
        for line in block.split('\r\n'):
            line = line.strip()
            if line.startswith('FN'):
                colon = line.find(':')
                if colon >= 0:
                    raw_val = line[colon+1:]
                    try:
                        name = quopri.decodestring(raw_val.encode()).decode('utf-8')
                    except:
                        name = raw_val
            if line.startswith('TEL'):
                digits = re.sub(r'\D', '', line)
                if digits:
                    phone = digits
        if name:
            contacts.append({'name': name, 'phone': phone})
    return contacts

def import_to_db(contacts):
    """合并联系人到主库"""
    if not MAIN_DB.exists():
        print(f"❌ 主库不存在: {MAIN_DB}")
        return 0

    existing = json.loads(MAIN_DB.read_text())
    existing_names = {c['name'] for c in existing}

    imported = 0
    skipped = 0
    for vc in contacts:
        name = vc['name']
        phone = vc['phone']

        if name in existing_names:
            # 更新手机号（如果之前没有）
            for c in existing:
                if c['name'] == name:
                    if phone and not c.get('platforms', {}).get('phone'):
                        c.setdefault('platforms', {})['phone'] = phone
                    skipped += 1
                    break
            continue

        new_id = f"vcf_auto_{int(time.time())}_{imported}"
        entry = {
            'id': new_id,
            'name': name,
            'relation': '',
            'sub_relation': '',
            'strength': 1,
            'tags': [],
            'platforms': {'phone': phone} if phone else {},
            'notes': '微信通讯录自动同步',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'source': 'wechat_auto_sync'
        }
        existing.append(entry)
        imported += 1

    MAIN_DB.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    return imported

def find_vcf_files():
    """查找所有未扫描的VCF文件"""
    found = []
    scanned = get_scanned()

    for dir_pattern in WECHAT_FILE_DIRS:
        if dir_pattern.exists():
            # Recursively search for VCF files
            for f in dir_pattern.rglob('*.vcf'):
                if str(f) not in scanned:
                    found.append(f)

    return found

def main():
    print("=" * 50)
    print(f"微信通讯录自动同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    vcf_files = find_vcf_files()
    if not vcf_files:
        print("✅ 没有新的VCF文件需要导入")
        print(f"   （已扫描 {len(get_scanned())} 个文件）")
        return

    total_imported = 0
    for vcf_file in vcf_files:
        print(f"\n📄 发现新文件: {vcf_file.name}")
        try:
            contacts = parse_vcf(vcf_file)
            n = import_to_db(contacts)
            mark_scanned(vcf_file)
            total_imported += n
            print(f"   ✅ 导入 {n} 个联系人")
        except Exception as e:
            print(f"   ❌ 解析失败: {e}")

    print(f"\n{'='*50}")
    print(f"📊 本次共导入: {total_imported} 个新联系人")

    # 统计总数
    db = json.loads(MAIN_DB.read_text())
    print(f"📊 通讯录总数: {len(db)} 人")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""华为手表健康数据读取 — BLE蓝牙直连方案

前置条件：
  1. Mac 蓝牙已开启
  2. 华为手表开启"心率广播"（设置 → 心率广播 → 开启）

用法：
  python3 scripts/huawei_health_ble.py           # 单次读取心率
  python3 scripts/huawei_health_ble.py --watch    # 持续监听（30秒间隔）
"""

import asyncio, json, os, sys, time
from datetime import datetime
from bleak import BleakScanner, BleakClient

HEART_RATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
BATTERY_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"

TRACKING_FILE = os.path.expanduser("~/claude/deliverables/health/路线图/华为手表数据.md")
WATCH_KEYWORDS = ["huawei", "watch", "gt", "band", "honor", "华为"]

found_watch = None

def hr_callback(sender, data):
    """心率数据回调"""
    hr = data[1] if len(data) > 1 else 0
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"| {ts} | {hr} | BLE直连 |\n"
    print(f"  ❤️ {hr} bpm at {ts}")
    os.makedirs(os.path.dirname(TRACKING_FILE), exist_ok=True)
    with open(TRACKING_FILE, "a") as f:
        f.write(line)

async def scan_watch():
    global found_watch
    print("🔍 扫描华为手表...")
    devices = await BleakScanner.discover(timeout=10)
    for d in devices:
        name = (d.name or "").lower()
        if any(k in name for k in WATCH_KEYWORDS):
            found_watch = d
            print(f"  ✅ 发现手表: {d.name} ({d.address})")
            return d
    print("  ❌ 未发现手表（确认手表已开启心率广播）")
    return None

async def read_once():
    device = await scan_watch()
    if not device:
        return

    hr_data = {"value": 0}

    def callback(sender, data):
        hr_data["value"] = data[1] if len(data) > 1 else 0

    async with BleakClient(device.address) as client:
        print(f"  🔗 已连接，等待心率数据...")
        # 先尝试列举服务，找心率特征
        for service in client.services:
            for char in service.characteristics:
                if "heart" in char.description.lower() or "2a37" in char.uuid:
                    print(f"  📡 找到心率特征: {char.uuid}")
                    await client.start_notify(char.uuid, callback)
                    await asyncio.sleep(5)  # 等5秒接收数据
                    await client.stop_notify(char.uuid)

        hr = hr_data["value"]
        ts = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%Y-%m-%d")
        os.makedirs(os.path.dirname(TRACKING_FILE), exist_ok=True)
        with open(TRACKING_FILE, "a") as f:
            f.write(f"| {ts} | {hr} | BLE单次 |\n")
        if hr > 0:
            print(f"\n  ✅ {date} {ts} 心率: {hr} bpm ❤️")
        else:
            print(f"\n  ⚠️ 未收到心率数据（手表可能未开启心率广播）")
        print(f"  📝 已记录到: {TRACKING_FILE}")
        await client.disconnect()

async def watch_loop():
    """持续监听模式"""
    device = await scan_watch()
    if not device:
        return
    async with BleakClient(device.address) as client:
        print(f"  🔗 已连接，开始监听心率（30秒间隔）")
        await client.start_notify(HEART_RATE_CHAR_UUID, hr_callback)
        try:
            await asyncio.sleep(300)  # 监听5分钟后退出
        finally:
            await client.stop_notify(HEART_RATE_CHAR_UUID)

if __name__ == "__main__":
    if "--watch" in sys.argv:
        asyncio.run(watch_loop())
    else:
        asyncio.run(read_once())

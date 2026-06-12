# Health Kit 申请材料清单

> 个人开发者 | 应用ID: 117974443 | 申请日期: 2026-06-09

---

## 一、应用基本信息

| 字段 | 内容 |
|:----|:-----|
| **应用名称** | 健康数据管理工具 |
| **应用类型** | 服务器应用 |
| **App ID** | 117974443 |
| **App Secret** | 6d0cc8ebe60392079b63f01a410fe9fe32cf978eb194d7341a66b03f5224ead9 |
| **回调地址** | http://localhost:8080/callback |
| **用户协议链接** | https://github.com/farmost-beep/claude/blob/main/huawei_health_agreement.html |
| **隐私政策链接** | https://github.com/farmost-beep/claude/blob/main/huawei_health_agreement.html |

---

## 二、应用描述（复制用）

> 个人健康数据管理工具，通过华为Health Kit REST API读取用户授权后的健康数据（步数、心率、睡眠、血氧等），数据仅存储于用户本地设备，不上传任何第三方服务器，不用于任何商业目的。仅限本人使用。

---

## 三、申请的数据权限范围

| 数据类型 | Scope | 说明 |
|:--------|:------|:-----|
| ☑️ 步数 | https://www.huawei.com/healthkit/steps.read | 每日步数 |
| ☑️ 心率 | https://www.huawei.com/healthkit/heartrate.read | 心率数据 |
| ☑️ 睡眠 | https://www.huawei.com/healthkit/sleep.read | 睡眠时长与质量 |
| ☑️ 血氧 | https://www.huawei.com/healthkit/bloodoxygen.read | 血氧饱和度 |
| ⬜ 身高体重 | https://www.huawei.com/healthkit/heightweight.read | 可选，暂不勾选 |
| ⬜ 运动记录 | https://www.huawei.com/healthkit/activity.read | 可选，暂不勾选 |

---

## 四、数据使用声明

### 4.1 数据用途
- ✅ 仅本地存储，用于个人健康追踪
- ✅ 仅在用户主动触发的脚本运行时读取
- ❌ 不上传至任何第三方服务器
- ❌ 不用于商业目的
- ❌ 不分享给任何第三方

### 4.2 数据存储
- 存储位置：用户本地Mac `/Users/cyingfang/claude/deliverables/health/路线图/华为手表数据.md`
- 存储格式：Markdown表格（时间、心率、来源）
- 保留期限：持续积累，用户可随时手动删除

### 4.3 用户控制
- 用户可随时在华为健康App中撤销授权
- 用户可随时删除本地存储的数据

---

## 五、申请流程操作步骤

### 线上申请（优先）
```
开发者联盟 → 管理中心 → 应用 → Health Service Kit
→ 填写表单（参考一至四节内容）
→ 提交 → 等待审核通知（短信+邮件）
```

### 邮件补充（如线上未通过）
将以下材料发送至：**hihealth@huawei.com**

**邮件标题：** Health Kit服务申请 — App ID: 117974443

**邮件正文：**
```
App ID: 117974443
应用名称：健康数据管理工具
应用类型：服务器应用

应用描述：
个人健康数据管理工具，通过华为Health Kit REST API读取用户授权后的健康数据（步数、心率、睡眠、血氧等），数据仅存储于用户本地设备，不上传任何第三方服务器，不用于任何商业目的。仅限本人使用。

申请的数据范围：
- steps.read（步数）
- heartrate.read（心率）
- sleep.read（睡眠）
- bloodoxygen.read（血氧）

用户协议：https://github.com/farmost-beep/claude/blob/main/huawei_health_agreement.html
隐私政策：https://github.com/farmost-beep/claude/blob/main/huawei_health_agreement.html
```

---

## 六、后续操作

| 步骤 | 说明 | 预计时间 |
|:----|:-----|:--------|
| ① 提交申请 | 在线填写或邮件发送 | 今天 |
| ② 等待审核 | 华为人工审核 | ~15工作日 |
| ③ 审核通过 | 获得测试权限（限100用户） | 收到短信/邮件通知 |
| ④ 运行授权 | `python3 scripts/huawei_health_cloud.py --auth` | 审批通过后 |
| ⑤ 读取数据 | `python3 scripts/huawei_health_cloud.py --fetch` | 授权成功后 |

---

## 七、相关文件索引

| 文件 | 路径 |
|:----|:-----|
| 申请材料清单 | `deliverables/health/路线图/华为Health Kit申请材料.md` |
| 用户协议/隐私政策 | `huawei_health_agreement.html` |
| Cloud API脚本 | `scripts/huawei_health_cloud.py` |
| 凭证文件 | `scripts/lib/huawei_credentials.py` |
| BLE脚本 | `scripts/huawei_health_ble.py` |
| 健康追踪文件 | `deliverables/health/路线图/华为手表数据.md` |

---

> 更新记录：2026-06-09 初版 | 脚本：`check_feishu_loop` via Claude

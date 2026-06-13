#!/usr/bin/env node
/**
 * 通过 wechat-claude-code 桥接发送消息到微信
 * 使用 Node.js fetch (ESM)，与守护进程相同的API调用方式
 *
 * 用法: node send_via_bridge.mjs <用户ID> <消息内容>
 */
import { readFileSync, readdirSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';
import crypto from 'crypto';

const accountsDir = join(homedir(), '.wechat-claude-code', 'accounts');
const files = existsSync(accountsDir)
    ? readdirSync(accountsDir).filter(f => f.endsWith('.json'))
    : [];

if (files.length === 0) {
    console.error('未找到微信桥接账号配置');
    process.exit(1);
}

const account = JSON.parse(readFileSync(join(accountsDir, files[0]), 'utf-8'));
const botToken = account.botToken;
const accountId = account.accountId;
const baseUrl = account.baseUrl || 'https://ilinkai.weixin.qq.com';

const toUserId = process.argv[2];
const text = process.argv[3];

if (!toUserId || !text) {
    console.error('用法: node send_via_bridge.mjs <用户ID> <消息内容>');
    process.exit(1);
}

async function send() {
    const url = `${baseUrl}/ilink/bot/sendmessage`;
    const clientId = `wcc-push-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
    const uin = crypto.randomBytes(4).toString('hex');

    const body = {
        msg: {
            from_user_id: accountId,
            to_user_id: toUserId,
            client_id: clientId,
            message_type: 2,
            message_state: 2,
            context_token: '',
            item_list: [{ type: 1, text_item: { text } }],
        }
    };

    const maxRetries = 3;
    let delay = 2000;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${botToken}`,
                    'AuthorizationType': 'ilink_bot_token',
                    'X-WECHAT-UIN': uin,
                },
                body: JSON.stringify(body),
                signal: AbortSignal.timeout(15000),
            });

            const result = await res.json();
            const ret = result.ret;

            if (ret === undefined || ret === 0 || result.errcode === 0) {
                console.log('微信桥接推送成功');
                return;
            }
            if (ret === -2) {
                if (attempt < maxRetries) {
                    await new Promise(r => setTimeout(r, delay));
                    delay = Math.min(delay * 2, 10000);
                    continue;
                }
                console.error('桥接API限流已达最大重试次数');
                process.exit(1);
            }
            console.error(`桥接API返回: ${JSON.stringify(result)}`);
            process.exit(1);
        } catch (err) {
            console.error(`桥接错误: ${err.message}`);
            process.exit(1);
        }
    }
}

send().catch(err => {
    console.error(`发送失败: ${err.message}`);
    process.exit(1);
});

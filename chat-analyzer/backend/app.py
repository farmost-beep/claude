"""后端API服务器 — 聊天记录分析"""
import os, json
from flask import Flask, request, jsonify
from analyzer import parse_chat, analyze

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze_api():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"code": 1, "msg": "请提供聊天文本"})

    text = data['text'].strip()
    if len(text) < 20:
        return jsonify({"code": 1, "msg": "文本太短，至少20字"})

    msgs = parse_chat(text)
    if not msgs:
        return jsonify({"code": 1, "msg": "未解析到消息，请确认格式: 日期 发言人: 内容"})

    result = analyze(msgs)
    return jsonify({"code": 0, "result": result})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

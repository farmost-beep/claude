/**
 * 群聊分析云函数 — 微信云开发
 * 调用: wx.cloud.callFunction({name:'analyze', data:{text:'...'}})
 */
const cloud = require('wx-server-sdk')
cloud.init()

exports.main = async (event) => {
  const text = (event.text || '').trim()
  if (text.length < 20) return { code: 1, msg: '文本太短' }

  // 解析聊天记录
  const msgs = []
  for (const line of text.split('\n')) {
    const m = line.match(/^(\d{4}[-/]\d{2}[-/]\d{2}[\s\d:]*)\s+([^:]+):\s*(.*)/)
    if (m) msgs.push({ time: m[1].trim(), sender: m[2].trim(), content: m[3].trim() })
  }

  if (msgs.length === 0) return { code: 1, msg: '未识别到消息，格式: 日期 发言人: 内容' }

  // 统计分析
  const senderCount = {}
  const hourCount = {}
  const dates = new Set()

  for (const m of msgs) {
    senderCount[m.sender] = (senderCount[m.sender] || 0) + 1
    dates.add(m.time.slice(0, 10))
    const h = m.time.includes(' ') ? m.time.split(' ').pop().split(':')[0] : ''
    if (h) hourCount[h] = (hourCount[h] || 0) + 1
  }

  const rankings = Object.entries(senderCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name, count]) => ({ name, count }))

  const hours = Object.entries(hourCount)
    .sort((a, b) => a[0] - b[0])
    .map(([hour, count]) => ({ hour, count }))

  const total = msgs.length
  const peakHour = hours.length > 0 ? hours.reduce((a, b) => a.count > b.count ? a : b).hour : 'N/A'

  return {
    code: 0,
    result: {
      total_msgs: total,
      total_chars: msgs.reduce((s, m) => s + m.content.length, 0),
      speakers: Object.keys(senderCount).length,
      days: dates.size,
      daily_avg: Math.round(total / Math.max(dates.size, 1) * 10) / 10,
      rankings,
      hours,
      peak_hour: peakHour + ':00',
      top_speaker: rankings[0]?.name || 'N/A'
    }
  }
}

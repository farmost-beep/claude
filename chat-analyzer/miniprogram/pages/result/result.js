Page({
  data: { stats: [], rankings: [], hours: [] },
  onLoad(options) {
    const data = JSON.parse(decodeURIComponent(options.data));
    if (data.code !== 0) return;
    const r = data.result;

    const stats = [
      { label: '总消息', value: r.total_msgs },
      { label: '发言人数', value: r.speakers },
      { label: '聊天天数', value: r.days },
      { label: '日均消息', value: r.daily_avg },
    ];

    const maxCount = r.rankings.length > 0 ? r.rankings[0].count : 1;
    const rankings = r.rankings.map(item => ({
      ...item, percent: Math.max(item.count / maxCount * 100, 5)
    }));

    const maxHour = r.hours.length > 0 ? Math.max(...r.hours.map(h => h.count)) : 1;
    const hours = r.hours.map(item => ({
      ...item, percent: Math.max(item.count / maxHour * 100, 2)
    }));

    this.setData({ stats, rankings, hours });
  },
  onShareAppMessage() {
    return { title: '📊 见面聊 - 群聊分析报告', path: '/pages/index/index' };
  }
})

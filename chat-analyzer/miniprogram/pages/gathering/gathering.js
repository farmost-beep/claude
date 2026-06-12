Page({
  data: {
    time: '周六', type: '吃饭', icon: '🍽️', note: '',
    members: [], showers: [], joined: false, passed: false, maybeDone: false
  },
  onLoad(options) {
    const data = options.data ? JSON.parse(decodeURIComponent(options.data)) : {};
    const iconMap = { '吃饭':'🍽️','咖啡':'☕','运动':'⚽','散步':'🚶','其他':'🎲' };
    const timeLabel = data.time === '今天' ? '🔥 ' : '本周';
    this.setData({
      time: data.time || '周六',
      timeLabel: timeLabel,
      type: data.type || '吃饭',
      icon: iconMap[data.type] || '🎲',
      note: data.note || '',
      members: data.members || ['组织者'],
      showers: data.showers || []
    });
  },
  join() {
    if (this.data.joined) return;
    this.setData({ joined: true, passed: false, maybeDone: false,
      members: this.data.passed ? [...this.data.members, '我'] : [...this.data.members, '我'],
      showers: [] });
    wx.showToast({ title: '✅ 报名成功！', icon: 'none' });
  },
  pass() {
    if (this.data.passed) return;
    this.setData({ passed: true, joined: false, maybeDone: false,
      showers: [...this.data.showers, '我'],
      members: this.data.joined ? this.data.members.filter(m => m !== '我') : this.data.members });
    wx.showToast({ title: '已标记，下次再约~', icon: 'none' });
  },
  recordMemory() { wx.navigateTo({ url: '/pages/memory/memory' }) },
  maybe() {
    if (this.data.maybeDone) return;
    this.setData({ maybeDone: true, joined: false, passed: false,
      members: this.data.joined ? this.data.members.filter(m => m !== '我') : this.data.members,
      showers: this.data.passed ? this.data.showers.filter(s => s !== '我') : this.data.showers });
    wx.showToast({ title: '⏳ 下次一定', icon: 'none' });
  },
  onShareAppMessage() {
    const { time, type, note, timeLabel } = this.data;
    const data = encodeURIComponent(JSON.stringify({ time, type, note }));
    const prefix = time === '今天' ? '🔥 就今天' : `📢 本周${time}`;
    return {
      title: `${prefix}一起${type}！${note ? '「' + note + '」' : ''}`,
      path: '/pages/gathering/gathering?data=' + data
    };
  }
})

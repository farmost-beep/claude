Page({
  data: { timeSel: '', typeSel: '', note: '', loading: false, canCreate: false },
  selTime(e) { this.setData({ timeSel: e.currentTarget.dataset.t }, this.checkForm) },
  selType(e) { this.setData({ typeSel: e.currentTarget.dataset.t }, this.checkForm) },
  onNote(e) { this.setData({ note: e.detail.value }) },
  checkForm() {
    this.setData({ canCreate: !!this.data.timeSel && !!this.data.typeSel });
  },
  createGathering() {
    const { timeSel, typeSel, note } = this.data;
    const data = encodeURIComponent(JSON.stringify({ time: timeSel, type: typeSel, note }));
    wx.navigateTo({ url: '/pages/gathering/gathering?data=' + data });
  },
  goMemory() { wx.navigateTo({ url: '/pages/memory/memory' }) },
  scrollToForm() { wx.pageScrollTo({ selector: '#formSection', duration: 300 }) },
  onShareAppMessage() {
    const { timeSel, typeSel, note } = this.data;
    return {
      title: `【见面聊】${timeSel}一起${typeSel}${note ? ' · ' + note : ''}`,
      path: '/pages/gathering/gathering',
      imageUrl: '/images/share_card.png'
    };
  }
})

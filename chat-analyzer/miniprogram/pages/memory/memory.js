Page({
  data: { memories: [], totalPeople: 0, uniqueMonths: 1 },
  onShow() {
    const memories = wx.getStorageSync('xiaxian_memories') || [];
    const totalPeople = memories.reduce((s, m) => s + (m.count || 0), 0);
    const uniqueMonths = new Set(memories.map(m => (m.date || '').slice(0, 7))).size || 1;
    this.setData({ memories, totalPeople, uniqueMonths: Math.max(uniqueMonths, 1) });
  },
  takePhoto() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: res => {
        const tempPath = res.tempFilePaths[0];
        wx.showModal({
          title: '📸 记录这次见面',
          content: '几个人一起的？',
          editable: true,
          placeholderText: '如：3个人',
          success: modal => {
            if (!modal.confirm) return;
            const count = parseInt(modal.content) || 2;
            const now = new Date();
            const date = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
            const time = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;

            // Save to storage
            const memories = wx.getStorageSync('xiaxian_memories') || [];
            memories.unshift({
              id: Date.now(),
              image: tempPath,
              date, time,
              count,
              type: '见面聊',
              desc: `${count}个人的聚会`
            });
            wx.setStorageSync('xiaxian_memories', memories);

            wx.showToast({ title: '✅ 见面已记录！', icon: 'none' });
            this.onShow();
          }
        });
      }
    });
  },
  onShareAppMessage() {
    return { title: '📸 见面记忆墙 - 见面聊', path: '/pages/memory/memory' };
  }
});

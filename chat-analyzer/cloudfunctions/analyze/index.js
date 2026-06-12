/**
 * 见面聊 — 云函数
 * 创建邀约: { action:'create', time, type, note }
 */
const cloud = require('wx-server-sdk')
cloud.init()

exports.main = async (event) => {
  if (event.action === 'create') {
    const card = {
      time: event.time || '周六',
      type: event.type || '吃饭',
      note: event.note || '',
      members: ['发起人'],
      showers: []
    };
    return { code: 0, card, msg: '邀约已创建，分享到群吧' };
  }
  return { code: 1, msg: '未知操作' };
};

// utils.js - 轻量级工具函数库（优化版）

/**
 * 防抖函数 - 支持立即执行和取消
 * @param {Function} fn 目标函数
 * @param {number} delay 延迟毫秒数，默认300
 * @param {Object} [options] 配置项
 * @param {boolean} [options.leading=false] 是否首次立即执行
 */
const debounce = (fn, delay = 300, { leading = false } = {}) => {
  let timer, invoked;
  const debounced = (...args) => {
    if (leading && !invoked) {
      fn(...args);
      invoked = true;
    }
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (!leading) fn(...args);
      invoked = false;
    }, delay);
  };
  debounced.cancel = () => { clearTimeout(timer); invoked = false; };
  return debounced;
};

/**
 * 节流函数 - 首次/末次可配置
 * @param {Function} fn 目标函数
 * @param {number} interval 间隔毫秒数，默认300
 */
const throttle = (fn, interval = 300) => {
  let last = 0, timer;
  return (...args) => {
    const now = Date.now(), remaining = interval - (now - last);
    if (remaining <= 0) {
      fn(...args); last = now;
    } else if (!timer) {
      timer = setTimeout(() => { fn(...args); last = Date.now(); timer = null; }, remaining);
    }
  };
};

/** 深拷贝 - 使用结构化克隆（支持 Date/RegExp/Map/Set） */
const deepClone = (obj) => structuredClone(obj);

/**
 * 对象属性挑选
 * @param {Object} obj 源对象
 * @param {string[]} keys 要提取的键数组
 * @returns {Object} 新对象
 */
const pick = (obj, keys) =>
  Object.fromEntries(keys.filter(k => k in obj).map(k => [k, obj[k]]]));

/**
 * 异步等待（可取消）
 * @param {number} ms 等待毫秒数
 * @returns {Promise<void>}
 */
const sleep = (ms) => new Promise((resolve) => {
  let timer = setTimeout(resolve, ms);
  sleep.cancel = () => { clearTimeout(timer); };
});

module.exports = { debounce, throttle, deepClone, pick, sleep };

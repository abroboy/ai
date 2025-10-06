/**
 * 全球资金流向工具函数增强模块
 */

// 格式化数字显示
function formatNumber(num, decimals = 1) {
  if (typeof num !== 'number') return '0';
  
  if (Math.abs(num) >= 1000) {
    return (num / 1000).toFixed(decimals) + 'K';
  } else if (Math.abs(num) >= 1000000) {
    return (num / 1000000).toFixed(decimals) + 'M';
  } else if (Math.abs(num) >= 1000000000) {
    return (num / 1000000000).toFixed(decimals) + 'B';
  }
  
  return num.toFixed(decimals);
}

// 格式化百分比
function formatPercentage(num, decimals = 1) {
  if (typeof num !== 'number') return '0%';
  return (num >= 0 ? '+' : '') + num.toFixed(decimals) + '%';
}

// 获取颜色基于数值
function getColorByValue(value, type = 'netFlow') {
  if (type === 'netFlow') {
    return value >= 0 ? '#28a745' : '#dc3545';
  } else if (type === 'change') {
    if (value > 5) return '#28a745';
    if (value > 0) return '#17a2b8';
    if (value > -5) return '#ffc107';
    return '#dc3545';
  }
  return '#6c757d';
}

// 数据缓存管理
const DataCache = {
  cache: new Map(),
  
  set(key, data, ttl = 300000) { // 默认5分钟过期
    this.cache.set(key, {
      data: data,
      timestamp: Date.now(),
      ttl: ttl
    });
  },
  
  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }
    
    return item.data;
  },
  
  clear() {
    this.cache.clear();
  },
  
  size() {
    return this.cache.size;
  }
};

// 防抖函数
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// 节流函数
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// 深拷贝函数
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime());
  if (obj instanceof Array) return obj.map(item => deepClone(item));
  if (typeof obj === 'object') {
    const clonedObj = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj;
  }
}

// 生成唯一ID
function generateUniqueId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// 检查数据完整性
function checkDataIntegrity(data) {
  const issues = [];
  
  if (!Array.isArray(data)) {
    issues.push('数据不是数组格式');
    return issues;
  }
  
  data.forEach((item, index) => {
    if (!item.region) {
      issues.push(`第${index + 1}项缺少地区名称`);
    }
    
    ['inflow', 'outflow', 'netFlow', 'change'].forEach(field => {
      if (typeof item[field] !== 'number') {
        issues.push(`第${index + 1}项的${field}字段不是数字`);
      }
    });
  });
  
  return issues;
}

// 数据排序工具
function sortData(data, field, order = 'desc') {
  return [...data].sort((a, b) => {
    if (order === 'desc') {
      return b[field] - a[field];
    } else {
      return a[field] - b[field];
    }
  });
}

// 数据过滤工具
function filterData(data, filters) {
  return data.filter(item => {
    for (const [field, condition] of Object.entries(filters)) {
      if (condition.min !== undefined && item[field] < condition.min) {
        return false;
      }
      if (condition.max !== undefined && item[field] > condition.max) {
        return false;
      }
      if (condition.equals !== undefined && item[field] !== condition.equals) {
        return false;
      }
      if (condition.contains && !item[field].toString().toLowerCase().includes(condition.contains.toLowerCase())) {
        return false;
      }
    }
    return true;
  });
}

// 计算统计指标
function calculateStats(data, field) {
  if (!data || data.length === 0) return null;
  
  const values = data.map(item => item[field]).filter(val => typeof val === 'number');
  
  if (values.length === 0) return null;
  
  const sum = values.reduce((acc, val) => acc + val, 0);
  const mean = sum / values.length;
  const sortedValues = [...values].sort((a, b) => a - b);
  
  return {
    count: values.length,
    sum: sum,
    mean: mean,
    median: sortedValues[Math.floor(sortedValues.length / 2)],
    min: Math.min(...values),
    max: Math.max(...values),
    range: Math.max(...values) - Math.min(...values),
    variance: values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length,
    stdDev: Math.sqrt(values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length)
  };
}

// 导出数据为CSV
function exportToCSV(data, filename = 'global_capital_flow_data.csv') {
  if (!data || data.length === 0) {
    showNotification('没有数据可导出', 'warning');
    return;
  }
  
  const headers = Object.keys(data[0]);
  const csvContent = [
    headers.join(','),
    ...data.map(row => headers.map(header => {
      const value = row[header];
      return typeof value === 'string' && value.includes(',') ? `"${value}"` : value;
    }).join(','))
  ].join('\n');
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
  
  showNotification('数据导出成功', 'success');
}

// 导出数据为Excel
function exportToExcel(data, filename = 'global_capital_flow_data.xlsx') {
  // 这里需要引入SheetJS库来实现Excel导出
  showNotification('Excel导出功能需要引入SheetJS库', 'info');
}

// 本地存储管理
const LocalStorage = {
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      console.error('本地存储失败:', e);
      return false;
    }
  },
  
  get(key) {
    try {
      const value = localStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (e) {
      console.error('本地存储读取失败:', e);
      return null;
    }
  },
  
  remove(key) {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (e) {
      console.error('本地存储删除失败:', e);
      return false;
    }
  },
  
  clear() {
    try {
      localStorage.clear();
      return true;
    } catch (e) {
      console.error('本地存储清空失败:', e);
      return false;
    }
  }
};

// 错误处理工具
function handleError(error, context = '') {
  console.error(`错误发生在 ${context}:`, error);
  
  let message = '发生未知错误';
  
  if (error.message) {
    message = error.message;
  } else if (typeof error === 'string') {
    message = error;
  }
  
  showNotification(`${context ? context + ': ' : ''}${message}`, 'danger');
}

// 加载状态管理
const LoadingManager = {
  activeLoaders: new Set(),
  
  show(id = 'default') {
    this.activeLoaders.add(id);
    this.updateUI();
  },
  
  hide(id = 'default') {
    this.activeLoaders.delete(id);
    this.updateUI();
  },
  
  hideAll() {
    this.activeLoaders.clear();
    this.updateUI();
  },
  
  updateUI() {
    const isLoading = this.activeLoaders.size > 0;
    const loadingElement = document.getElementById('global-loading');
    
    if (loadingElement) {
      loadingElement.style.display = isLoading ? 'flex' : 'none';
    }
    
    // 更新按钮状态
    document.querySelectorAll('.btn-loading').forEach(btn => {
      btn.disabled = isLoading;
    });
  }
};

// 响应式工具
const ResponsiveUtils = {
  isMobile() {
    return window.innerWidth <= 768;
  },
  
  isTablet() {
    return window.innerWidth > 768 && window.innerWidth <= 1024;
  },
  
  isDesktop() {
    return window.innerWidth > 1024;
  },
  
  onResize(callback) {
    const debouncedCallback = debounce(callback, 250);
    window.addEventListener('resize', debouncedCallback);
    return () => window.removeEventListener('resize', debouncedCallback);
  }
};

// 主题管理
const ThemeManager = {
  themes: {
    light: {
      primary: '#007bff',
      success: '#28a745',
      danger: '#dc3545',
      warning: '#ffc107',
      info: '#17a2b8',
      background: '#ffffff',
      text: '#212529'
    },
    dark: {
      primary: '#0d6efd',
      success: '#198754',
      danger: '#dc3545',
      warning: '#fd7e14',
      info: '#0dcaf0',
      background: '#212529',
      text: '#ffffff'
    }
  },
  
  current: 'light',
  
  setTheme(themeName) {
    if (!this.themes[themeName]) return;
    
    this.current = themeName;
    const theme = this.themes[themeName];
    
    // 应用主题颜色
    document.documentElement.style.setProperty('--bs-primary', theme.primary);
    document.documentElement.style.setProperty('--bs-success', theme.success);
    document.documentElement.style.setProperty('--bs-danger', theme.danger);
    document.documentElement.style.setProperty('--bs-warning', theme.warning);
    document.documentElement.style.setProperty('--bs-info', theme.info);
    
    // 保存主题设置
    LocalStorage.set('theme', themeName);
  },
  
  toggleTheme() {
    const newTheme = this.current === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
  },
  
  init() {
    const savedTheme = LocalStorage.get('theme');
    if (savedTheme && this.themes[savedTheme]) {
      this.setTheme(savedTheme);
    }
  }
};

// 初始化工具函数
function initializeUtils() {
  // 初始化主题
  ThemeManager.init();
  
  // 设置全局错误处理
  window.addEventListener('error', (event) => {
    handleError(event.error, '全局错误');
  });
  
  // 设置未处理的Promise拒绝处理
  window.addEventListener('unhandledrejection', (event) => {
    handleError(event.reason, 'Promise拒绝');
  });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initializeUtils);
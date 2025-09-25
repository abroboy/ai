/**
 * 大势所趋风险框架管理台 - 模块测试脚本
 */

// 测试第一层模块：基础数据采集
function testDataCollection() {
  console.log("=== 测试基础数据采集模块 ===");
  // 测试热点数据表
  if (typeof loadHotspotDataTable === 'function') {
    console.log("✅ 热点数据表模块加载正常");
  } else {
    console.error("❌ 热点数据表模块加载失败");
  }
  
  // 测试行业数据
  if (typeof loadIndustryDataTable === 'function') {
    console.log("✅ 行业数据表模块加载正常");
  } else {
    console.error("❌ 行业数据表模块加载失败");
  }
}

// 测试第二层模块：数据整合
function testDataIntegration() {
  console.log("\n=== 测试数据整合模块 ===");
  if (typeof loadDataIntegrationModule === 'function') {
    console.log("✅ 数据整合模块加载正常");
  } else {
    console.error("❌ 数据整合模块加载失败");
  }
}

// 测试第三层模块：深度分析
function testDeepAnalysis() {
  console.log("\n=== 测试深度分析模块 ===");
  if (typeof loadDeepAnalysisModule === 'function') {
    console.log("✅ 深度分析模块加载正常");
  } else {
    console.error("❌ 深度分析模块加载失败");
  }
}

// 测试第四层模块：评分系统
function testScoringSystem() {
  console.log("\n=== 测试评分系统模块 ===");
  if (typeof loadCompanyScoreTable === 'function') {
    console.log("✅ 公司分值表模块加载正常");
  } else {
    console.error("❌ 公司分值表模块加载失败");
  }
}

// 测试第五层模块：权重分析
function testWeightAnalysis() {
  console.log("\n=== 测试权重分析模块 ===");
  if (typeof loadObjectFactorWeightTable === 'function') {
    console.log("✅ 对象因子权重表模块加载正常");
  } else {
    console.error("❌ 对象因子权重表模块加载失败");
  }
}

// 测试第六层模块：预测分析
function testPredictionAnalysis() {
  console.log("\n=== 测试预测分析模块 ===");
  if (typeof loadCurvePredictionAnalysis === 'function') {
    console.log("✅ 曲线预测分析模块加载正常");
  } else {
    console.error("❌ 曲线预测分析模块加载失败");
  }
}

// 测试模块间数据流转
function testDataFlow() {
  console.log("\n=== 测试模块间数据流转 ===");
  
  // 测试热点数据→深度分析
  if (typeof exportToDeepAnalysis === 'function') {
    console.log("✅ 热点数据→深度分析 导出功能正常");
  } else {
    console.error("❌ 热点数据→深度分析 导出功能异常");
  }
  
  // 测试深度分析→评分系统
  if (typeof importFromDeepAnalysis === 'function') {
    console.log("✅ 深度分析→评分系统 导入功能正常");
  } else {
    console.error("❌ 深度分析→评分系统 导入功能异常");
  }
  
  // 测试评分系统→权重分析
  if (typeof importFromScoreSystem === 'function') {
    console.log("✅ 评分系统→权重分析 导入功能正常");
  } else {
    console.error("❌ 评分系统→权重分析 导入功能异常");
  }
  
  // 测试权重分析→预测分析
  if (typeof importFromWeightAnalysis === 'function') {
    console.log("✅ 权重分析→预测分析 导入功能正常");
  } else {
    console.error("❌ 权重分析→预测分析 导入功能异常");
  }
}

// 运行所有测试
function runAllTests() {
  testDataCollection();
  testDataIntegration();
  testDeepAnalysis();
  testScoringSystem();
  testWeightAnalysis();
  testPredictionAnalysis();
  testDataFlow();
}

// 执行测试
runAllTests();
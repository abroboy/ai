package com.windindustry.service;

import com.windindustry.model.ListedCompanyInfo;
import com.windindustry.repository.ListedCompanyInfoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

/**
 * 上市公司信息服务层
 * 提供上市公司基本信息的查询、统计和管理功能
 */
@Service
public class ListedCompanyInfoService {
    
    @Autowired
    private ListedCompanyInfoRepository listedCompanyRepository;
    
    /**
     * 获取上市公司信息统计数据
     */
    public Map<String, Object> getCompanyStatistics() {
        Map<String, Object> stats = new HashMap<>();
        
        // 基础统计
        long totalCompanies = listedCompanyRepository.count();
        long activeCompanies = listedCompanyRepository.findByIsActiveTrue().size();
        long suspendedCompanies = listedCompanyRepository.findSuspendedStocks().size();
        long stCompanies = listedCompanyRepository.findStStocks().size();
        
        stats.put("total_companies", totalCompanies);
        stats.put("active_companies", activeCompanies);
        stats.put("suspended_companies", suspendedCompanies);
        stats.put("st_companies", stCompanies);
        
        // 市场分布统计
        List<Object[]> marketStats = listedCompanyRepository.getMarketTypeStatistics();
        List<Map<String, Object>> marketDistribution = new ArrayList<>();
        for (Object[] stat : marketStats) {
            Map<String, Object> market = new HashMap<>();
            market.put("market_type", stat[0]);
            market.put("count", stat[1]);
            marketDistribution.add(market);
        }
        stats.put("market_distribution", marketDistribution);
        
        // 行业分布统计
        List<Object[]> industryStats = listedCompanyRepository.getIndustryStatistics();
        List<Map<String, Object>> industryDistribution = new ArrayList<>();
        for (Object[] stat : industryStats) {
            Map<String, Object> industry = new HashMap<>();
            industry.put("industry_code", stat[0]);
            industry.put("industry_name", stat[1]);
            industry.put("count", stat[2]);
            industryDistribution.add(industry);
        }
        stats.put("industry_distribution", industryDistribution);
        
        return stats;
    }
    
    /**
     * 分页查询上市公司信息
     */
    public Page<ListedCompanyInfo> getCompanies(int page, int size, String sortBy, String sortDir,
                                                 String stockCode, String stockName, String companyName,
                                                 String marketType, String industryCode, Boolean isActive) {
        
        Sort sort = sortDir.equalsIgnoreCase("desc") ? 
                   Sort.by(sortBy).descending() : Sort.by(sortBy).ascending();
        Pageable pageable = PageRequest.of(page, size, sort);
        
        return listedCompanyRepository.findByMultipleFilters(
                stockCode, stockName, companyName, marketType, industryCode, isActive, pageable);
    }
    
    /**
     * 根据股票代码获取公司信息
     */
    public Optional<ListedCompanyInfo> getCompanyByStockCode(String stockCode) {
        return listedCompanyRepository.findByStockCode(stockCode);
    }
    
    /**
     * 获取市值排行榜
     */
    public List<ListedCompanyInfo> getMarketValueRanking(int limit) {
        Pageable pageable = PageRequest.of(0, limit);
        return listedCompanyRepository.findTopByMarketValue(pageable);
    }
    
    /**
     * 根据市值范围查询公司
     */
    public List<ListedCompanyInfo> getCompaniesByMarketValueRange(BigDecimal minValue, BigDecimal maxValue) {
        return listedCompanyRepository.findByMarketValueRange(minValue, maxValue);
    }
    
    /**
     * 获取高ROE公司
     */
    public List<ListedCompanyInfo> getHighRoeCompanies(BigDecimal minRoe) {
        return listedCompanyRepository.findByRoeGreaterThan(minRoe);
    }
    
    /**
     * 获取低PE公司
     */
    public List<ListedCompanyInfo> getLowPeCompanies(BigDecimal maxPe) {
        return listedCompanyRepository.findByPeRatioRange(BigDecimal.ZERO, maxPe);
    }
    
    /**
     * 保存或更新公司信息
     */
    public ListedCompanyInfo saveCompanyInfo(ListedCompanyInfo companyInfo) {
        return listedCompanyRepository.save(companyInfo);
    }
    
    /**
     * 批量保存公司信息
     */
    public List<ListedCompanyInfo> saveAllCompanyInfo(List<ListedCompanyInfo> companies) {
        return listedCompanyRepository.saveAll(companies);
    }
    
    /**
     * 刷新上市公司数据
     */
    public void refreshCompanyData() {
        System.out.println("开始刷新上市公司数据...");
        
        try {
            // 获取所有活跃公司
            List<ListedCompanyInfo> companies = listedCompanyRepository.findByIsActiveTrue();
            
            // 更新数据
            for (ListedCompanyInfo company : companies) {
                updateCompanyData(company);
            }
            
            // 批量保存
            listedCompanyRepository.saveAll(companies);
            
            System.out.println("上市公司数据刷新完成，共更新 " + companies.size() + " 家公司");
            
        } catch (Exception e) {
            System.err.println("刷新上市公司数据失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * 更新单个公司的模拟数据
     */
    private void updateCompanyData(ListedCompanyInfo company) {
        Random random = ThreadLocalRandom.current();
        
        // 更新股价 (基于现有价格±10%波动)
        if (company.getLatestPrice() != null) {
            double currentPrice = company.getLatestPrice().doubleValue();
            double newPrice = currentPrice * (0.9 + random.nextDouble() * 0.2);
            company.setLatestPrice(BigDecimal.valueOf(Math.round(newPrice * 100.0) / 100.0));
            
            // 基于新股价更新市值
            if (company.getTotalShareCapital() != null) {
                BigDecimal newMarketValue = company.getLatestPrice()
                        .multiply(company.getTotalShareCapital());
                company.setTotalMarketValue(newMarketValue);
            }
        }
        
        // 更新PE比率 (5-50之间)
        double newPe = 5 + random.nextDouble() * 45;
        company.setPeRatio(BigDecimal.valueOf(Math.round(newPe * 100.0) / 100.0));
        
        // 更新PB比率 (0.5-10之间)
        double newPb = 0.5 + random.nextDouble() * 9.5;
        company.setPbRatio(BigDecimal.valueOf(Math.round(newPb * 100.0) / 100.0));
        
        // 更新ROE (0-30%之间)
        double newRoe = random.nextDouble() * 0.3;
        company.setRoe(BigDecimal.valueOf(Math.round(newRoe * 10000.0) / 10000.0));
        
        // 更新股息率 (0-8%之间)
        double newDividendYield = random.nextDouble() * 0.08;
        company.setDividendYield(BigDecimal.valueOf(Math.round(newDividendYield * 10000.0) / 10000.0));
    }
    
    /**
     * 初始化上市公司测试数据
     */
    public void initializeCompanyData() {
        System.out.println("初始化上市公司数据...");
        
        // 检查是否已有数据
        if (listedCompanyRepository.count() > 0) {
            System.out.println("上市公司数据已存在，跳过初始化");
            return;
        }
        
        List<ListedCompanyInfo> companies = generateCompanyTestData();
        listedCompanyRepository.saveAll(companies);
        
        System.out.println("成功初始化 " + companies.size() + " 家上市公司数据");
    }
    
    /**
     * 生成上市公司测试数据
     */
    private List<ListedCompanyInfo> generateCompanyTestData() {
        List<ListedCompanyInfo> companies = new ArrayList<>();
        Random random = ThreadLocalRandom.current();
        
        // A股主要公司数据
        Object[][] companyData = {
            // {股票代码, 公司名称, 股票名称, 市场类型, 交易所, 行业代码, 行业名称}
            {"000001", "平安银行股份有限公司", "平安银行", "A股", "SZ", "480100", "银行"},
            {"000002", "万科企业股份有限公司", "万科A", "A股", "SZ", "430100", "房地产开发"},
            {"600000", "浦发银行股份有限公司", "浦发银行", "A股", "SH", "480100", "银行"},
            {"600036", "招商银行股份有限公司", "招商银行", "A股", "SH", "480100", "银行"},
            {"600519", "贵州茅台酒股份有限公司", "贵州茅台", "A股", "SH", "610300", "白酒"},
            {"000858", "五粮液股份有限公司", "五粮液", "A股", "SZ", "610300", "白酒"},
            {"000725", "京东方科技集团股份有限公司", "京东方A", "A股", "SZ", "360100", "半导体"},
            {"002415", "海康威视数字技术股份有限公司", "海康威视", "A股", "SZ", "360100", "半导体"},
            {"002594", "比亚迪股份有限公司", "比亚迪", "A股", "SZ", "420000", "交通运输"},
            {"600104", "上海汽车集团股份有限公司", "上汽集团", "A股", "SH", "420000", "交通运输"},
            {"300015", "爱尔眼科医院集团股份有限公司", "爱尔眼科", "创业板", "SZ", "710000", "社服"},
            {"688981", "中芯国际集成电路制造有限公司", "中芯国际", "科创板", "SH", "360100", "半导体"},
            {"688036", "传音控股股份有限公司", "传音控股", "科创板", "SH", "360000", "电子"},
            {"300760", "迈瑞医疗股份有限公司", "迈瑞医疗", "创业板", "SZ", "710000", "社服"},
            {"000661", "长春高新技术产业(集团)股份有限公司", "长春高新", "A股", "SZ", "710000", "社服"}
        };
        
        for (Object[] data : companyData) {
            ListedCompanyInfo company = new ListedCompanyInfo();
            company.setStockCode((String) data[0]);
            company.setCompanyName((String) data[1]);
            company.setStockName((String) data[2]);
            company.setMarketType((String) data[3]);
            company.setExchangeCode((String) data[4]);
            company.setIndustryCode((String) data[5]);
            company.setIndustryName((String) data[6]);
            
            // 随机生成财务数据
            company.setListingDate(LocalDate.of(1990 + random.nextInt(30), 
                                               1 + random.nextInt(12), 
                                               1 + random.nextInt(28)));
            
            // 总股本(1-500亿股)
            BigDecimal totalShares = BigDecimal.valueOf(10000 + random.nextDouble() * 4990000);
            company.setTotalShareCapital(totalShares);
            
            // 流通股本(总股本的60-100%)
            BigDecimal circulatingShares = totalShares.multiply(
                    BigDecimal.valueOf(0.6 + random.nextDouble() * 0.4));
            company.setCirculatingShareCapital(circulatingShares);
            
            // 股价(1-500元)
            BigDecimal price = BigDecimal.valueOf(1 + random.nextDouble() * 499);
            company.setLatestPrice(price);
            
            // 市值
            company.setTotalMarketValue(totalShares.multiply(price));
            company.setCirculatingMarketValue(circulatingShares.multiply(price));
            
            // 财务指标
            company.setPeRatio(BigDecimal.valueOf(5 + random.nextDouble() * 45));
            company.setPbRatio(BigDecimal.valueOf(0.5 + random.nextDouble() * 9.5));
            company.setEps(BigDecimal.valueOf(0.1 + random.nextDouble() * 5));
            company.setBps(BigDecimal.valueOf(price.doubleValue() / company.getPbRatio().doubleValue()));
            company.setRoe(BigDecimal.valueOf(random.nextDouble() * 0.3));
            company.setRoa(BigDecimal.valueOf(random.nextDouble() * 0.15));
            company.setDividendYield(BigDecimal.valueOf(random.nextDouble() * 0.08));
            
            // 其他信息
            company.setIsSt(random.nextDouble() < 0.05); // 5%概率为ST
            company.setIsSuspended(random.nextDouble() < 0.02); // 2%概率停牌
            company.setIsActive(true);
            company.setRegisteredCapital(totalShares.multiply(BigDecimal.valueOf(1 + random.nextDouble())));
            company.setEmployeeCount(1000 + random.nextInt(50000));
            
            companies.add(company);
        }
        
        return companies;
    }
}
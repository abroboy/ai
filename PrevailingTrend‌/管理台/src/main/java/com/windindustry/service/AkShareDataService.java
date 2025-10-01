package com.windindustry.service;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * AKShare数据服务类
 * 用于从AKShare API获取上市公司数据
 */
@Service
public class AkShareDataService {
    
    // AKShare API 基础URL
    private static final String AKSHARE_BASE_URL = "http://127.0.0.1:8000";
    
    /**
     * 获取所有A股上市公司数据（精简映射，用于行业聚合）
     * @return 上市公司数据列表
     */
    public List<Map<String, Object>> getAllListedCompanies() {
        List<Map<String, Object>> companies = new ArrayList<>();
        
        try {
            CloseableHttpClient httpClient = HttpClients.createDefault();
            
            // 调用AKShare的股票代码接口获取所有A股
            String url = AKSHARE_BASE_URL + "/api/stock_zh_a_spot";
            HttpGet request = new HttpGet(url);
            CloseableHttpResponse response = httpClient.execute(request);
            
            if (response.getStatusLine().getStatusCode() == 200) {
                String jsonResponse = EntityUtils.toString(response.getEntity());
                JSONObject result = JSON.parseObject(jsonResponse);
                
                if (result.getBoolean("success")) {
                    JSONArray data = result.getJSONArray("data");
                    
                    for (int i = 0; i < data.size(); i++) {
                        JSONObject companyJson = data.getJSONObject(i);
                        Map<String, Object> company = new HashMap<>();
                        
                        // 处理股票代码，去除前缀
                        String stockCode = companyJson.getString("代码");
                        if (stockCode != null && stockCode.length() > 2) {
                            // 去除前缀（如sh、sz、bj）
                            stockCode = stockCode.substring(2);
                        }
                        
                        company.put("stockCode", stockCode);
                        company.put("stockName", companyJson.getString("名称"));
                        
                        // 将价格数据转换为BigDecimal
                        try {
                            if (companyJson.containsKey("最新价")) {
                                company.put("latestPrice", new BigDecimal(companyJson.getString("最新价")));
                            }
                            if (companyJson.containsKey("成交额")) {
                                company.put("turnover", new BigDecimal(companyJson.getString("成交额")));
                            }
                            if (companyJson.containsKey("成交量")) {
                                company.put("volume", new BigDecimal(companyJson.getString("成交量")));
                            }
                            if (companyJson.containsKey("涨跌幅")) {
                                company.put("priceChangeRate", new BigDecimal(companyJson.getString("涨跌幅")));
                            }
                            if (companyJson.containsKey("市盈率-动态")) {
                                company.put("peRatio", new BigDecimal(companyJson.getString("市盈率-动态")));
                            }
                        } catch (NumberFormatException e) {
                            // 处理数字格式异常
                            System.err.println("数据格式异常: " + e.getMessage());
                        }
                        
                        companies.add(company);
                    }
                }
            }
            
            response.close();
            httpClient.close();
            
        } catch (IOException e) {
            System.err.println("获取AKShare数据失败: " + e.getMessage());
            e.printStackTrace();
        }
        
        return companies;
    }
    
    /**
     * 获取所有A股上市公司数据（原始全字段，保持AKShare字段名）
     */
    public List<Map<String, Object>> getAllListedCompaniesRaw() {
        List<Map<String, Object>> companies = new ArrayList<>();
        try {
            CloseableHttpClient httpClient = HttpClients.createDefault();
            String url = AKSHARE_BASE_URL + "/api/stock_zh_a_spot";
            HttpGet request = new HttpGet(url);
            CloseableHttpResponse response = httpClient.execute(request);
            if (response.getStatusLine().getStatusCode() == 200) {
                String jsonResponse = EntityUtils.toString(response.getEntity());
                JSONObject result = JSON.parseObject(jsonResponse);
                if (result.getBoolean("success")) {
                    JSONArray data = result.getJSONArray("data");
                    for (int i = 0; i < data.size(); i++) {
                        JSONObject row = data.getJSONObject(i);
                        // 直接转成 Map，保留中文键
                        Map<String, Object> map = JSON.parseObject(row.toJSONString(), Map.class);
                        companies.add(map);
                    }
                }
            }
            response.close();
            httpClient.close();
        } catch (IOException e) {
            System.err.println("获取AKShare全量数据失败: " + e.getMessage());
            e.printStackTrace();
        }
        return companies;
    }
    
    /**
     * 获取公司详细信息
     * @param stockCode 股票代码
     * @return 公司详细信息
     */
    public Map<String, Object> getCompanyDetail(String stockCode) {
        Map<String, Object> companyDetail = new HashMap<>();
        
        try {
            CloseableHttpClient httpClient = HttpClients.createDefault();
            
            // 获取公司基本信息
            String url = AKSHARE_BASE_URL + "/api/stock_company_info";
            url += "?symbol=" + stockCode;
            
            HttpGet request = new HttpGet(url);
            CloseableHttpResponse response = httpClient.execute(request);
            
            if (response.getStatusLine().getStatusCode() == 200) {
                String jsonResponse = EntityUtils.toString(response.getEntity());
                JSONObject result = JSON.parseObject(jsonResponse);
                
                if (result.getBoolean("success")) {
                    JSONObject data = result.getJSONObject("data");
                    companyDetail.putAll(JSON.parseObject(data.toJSONString(), Map.class));
                }
            }
            
            response.close();
            httpClient.close();
            
        } catch (IOException e) {
            System.err.println("获取公司详细信息失败: " + e.getMessage());
            e.printStackTrace();
        }
        
        return companyDetail;
    }
    
    /**
     * 检查AKShare服务是否可用
     * @return 是否可用
     */
    public boolean isAkShareAvailable() {
        try {
            CloseableHttpClient httpClient = HttpClients.createDefault();
            HttpGet request = new HttpGet(AKSHARE_BASE_URL + "/api/ping");
            CloseableHttpResponse response = httpClient.execute(request);
            
            boolean available = response.getStatusLine().getStatusCode() == 200;
            
            response.close();
            httpClient.close();
            
            return available;
        } catch (Exception e) {
            return false;
        }
    }
}
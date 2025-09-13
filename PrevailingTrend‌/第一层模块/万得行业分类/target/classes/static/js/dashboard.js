document.addEventListener("DOMContentLoaded", function() {
    const sidebarToggle = document.getElementById("sidebar-toggle");
    const sidebar = document.querySelector(".sidebar");
    const mainContent = document.querySelector(".main-content");
    const pageTitle = document.getElementById("page-title");

    // Sidebar toggle functionality
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function() {
            sidebar.classList.toggle("collapsed");
            mainContent.classList.toggle("expanded");
        });
    }

    // Section switching
    window.showSection = function(sectionId) {
        // Hide all sections
        document.querySelectorAll(".content-section").forEach(section => {
            section.classList.remove("active");
        });
        
        // Show selected section
        const targetSection = document.getElementById(sectionId + "-section");
        if (targetSection) {
            targetSection.classList.add("active");
        }
        
        // Update page title
        const linkElement = document.querySelector(`[onclick="showSection('${sectionId}')"] span`);
        if (linkElement) {
            pageTitle.textContent = linkElement.textContent;
        }
        
        // Load data based on section
        if (sectionId === "dashboard") {
            fetchStats();
            renderCharts();
        } else if (sectionId === "industries") {
            fetchIndustries(1);
        } else if (sectionId === "stocks") {
            fetchStocks(1);
        }
    };

    // Initial load
    showSection("dashboard");

    // Fetch statistics data
    async function fetchStats() {
        try {
            const response = await fetch("/api/stats");
            const data = await response.json();
            
            if (data.success) {
                document.getElementById("total-industries").textContent = data.data.total_industries;
                document.getElementById("total-stocks").textContent = data.data.total_stocks;
                document.getElementById("level-1-count").textContent = data.data.level_1_count;
                document.getElementById("level-2-count").textContent = data.data.level_2_count;
            } else {
                console.error("Error fetching stats:", data.error);
            }
        } catch (error) {
            console.error("Error fetching stats:", error);
        }
    }

    // Fetch industries data
    async function fetchIndustries(page = 1) {
        try {
            const response = await fetch("/api/industries");
            const data = await response.json();
            
            if (data.success) {
                renderIndustriesTable(data.data);
            } else {
                console.error("Error fetching industries:", data.error);
            }
        } catch (error) {
            console.error("Error fetching industries:", error);
        }
    }

    // Fetch stocks data
    async function fetchStocks(page = 1) {
        try {
            const sortBy = document.getElementById("sort-field")?.value || "stock_code";
            const sortOrder = document.getElementById("sort-order")?.value || "asc";
            
            const response = await fetch(`/api/stocks?page=${page}&sort_by=${sortBy}&sort_order=${sortOrder}`);
            const data = await response.json();
            
            if (data.success) {
                renderStocksTable(data.data.stocks);
                renderPagination("stocks-pagination", page, Math.ceil(data.data.total / data.data.page_size), fetchStocks);
            } else {
                console.error("Error fetching stocks:", data.error);
            }
        } catch (error) {
            console.error("Error fetching stocks:", error);
        }
    }

    // Render industries table
    function renderIndustriesTable(industries) {
        const tbody = document.getElementById("industries-table-body");
        if (!tbody) return;
        
        tbody.innerHTML = "";
        
        industries.forEach(industry => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${industry.industry_code}</td>
                <td>${industry.industry_name}</td>
                <td><span class="badge bg-${industry.level === 1 ? 
primary : secondary}">${industry.level === 1 ? 一级 : 二级}</span></td>
                <td>${industry.stock_count}</td>
                <td><span class="badge bg-success">活跃</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewIndustry('${industry.industry_code}')">查看</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    // Render stocks table
    function renderStocksTable(stocks) {
        const tbody = document.getElementById("stocks-table-body");
        if (!tbody) return;
        
        tbody.innerHTML = "";
        
        stocks.forEach(stock => {
            const row = document.createElement("tr");
            const predictionScore = stock.prediction_score || 0;
            const scoreClass = predictionScore > 0.7 ? success : predictionScore > 0.4 ? warning : danger;
            
            row.innerHTML = `
                <td>${stock.stock_code}</td>
                <td>${stock.stock_name}</td>
                <td>${stock.industry_name}</td>
                <td><span class="badge bg-${scoreClass}">${(predictionScore * 100).toFixed(1)}%</span></td>
                <td>${formatNumber(stock.avg_net_flow)}</td>
                <td>${(stock.confidence * 100).toFixed(1)}%</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewStock('${stock.stock_code}')">详情</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    // Render pagination
    function renderPagination(containerId, currentPage, totalPages, fetchFunction) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = "";
        
        if (totalPages <= 1) return;
        
        const pagination = document.createElement("nav");
        pagination.innerHTML = `
            <ul class="pagination">
                <li class="page-item ${currentPage === 1 ? disabled : '}">
                    <a class="page-link" href="#" onclick="fetchFunction(${currentPage - 1}); return false;">上一页</a>
                </li>
                ${Array.from({length: Math.min(5, totalPages)}, (_, i) => {
                    const page = i + 1;
                    return `<li class="page-item ${page === currentPage ? active : '}">
                        <a class="page-link" href="#" onclick="fetchFunction(${page}); return false;">${page}</a>
                    </li>`;
                }).join(')}
                <li class="page-item ${currentPage === totalPages ? disabled : '}">
                    <a class="page-link" href="#" onclick="fetchFunction(${currentPage + 1}); return false;">下一页</a>
                </li>
            </ul>
        `;
        
        container.appendChild(pagination);
    }

    // Render charts
    function renderCharts() {
        renderTrendChart();
        renderPieChart();
    }

    // Render trend chart
    function renderTrendChart() {
        const ctx = document.getElementById("trendChart");
        if (!ctx) return;
        
        new Chart(ctx, {
            type: line,
            data: {
                labels: [周一, 周二, 周三, 周四, 周五, 周六, 周日],
                datasets: [{
                    label: 股票数量,
                    data: [120, 135, 142, 138, 145, 150, 148],
                    borderColor: #3b82f6,
                    backgroundColor: rgba
59
130
246
0.1
,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Render pie chart
    function renderPieChart() {
        const ctx = document.getElementById("pieChart");
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 
doughnut,
            data: {
                labels: [银行, 科技, 医药, 新能源, 其他],
                datasets: [{
                    data: [25, 20, 15, 18, 22],
                    backgroundColor: [
                        #3b82f6,
                        #10b981,
                        #f59e0b,
                        #ef4444,
                        #8b5cf6
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: bottom
                    }
                }
            }
        });
    }

    // Utility functions
    function formatNumber(num) {
        if (num >= 100000000) {
            return (num / 100000000).toFixed(1) + 亿;
        } else if (num >= 10000) {
            return (num / 10000).toFixed(1) + 万;
        } else {
            return num.toFixed(2);
        }
    }

    // Global functions
    window.viewIndustry = function(industryCode) {
        alert(查看行业:
 + industryCode);
    };

    window.viewStock = function(stockCode) {
        alert(
查看股票:
 + stockCode);
    };

    window.clearCache = function() {
        alert(
缓存已清除);
    };

    window.refreshData = async function() {
        try {
            const response = await fetch("/api/refresh", {
                method: POST,
                headers: {
                    Content-Type: application/json
                }
            });
            const data = await response.json();
            
            if (data.success) {
                alert(数据刷新成功);
                // Refresh current section
                const activeSection = document.querySelector(".content-section.active");
                if (activeSection) {
                    const sectionId = activeSection.id.replace(-section, ');
                    showSection(sectionId);
                }
            } else {
                alert(数据刷新失败:
 + data.error);
            }
        } catch (error) {
            alert(
数据刷新失败:
 + error.message);
        }
    };

    // Event listeners for sorting
    document.getElementById("sort-field")?.addEventListener("change", () => fetchStocks(1));
    document.getElementById("sort-order")?.addEventListener("change", () => fetchStocks(1));
});

/**
 * 数据库管理页面脚本
 * 用于管理和查询数据库中的表和数据
 */

// 全局变量
let currentTable = '';
let currentPage = 1;
let pageSize = 50;
let totalRows = 0;
let tables = [];

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 加载数据库表列表
    loadTables();

    // 绑定事件处理程序
    document.getElementById('refreshBtn').addEventListener('click', loadTables);
    document.getElementById('runQueryBtn').addEventListener('click', runQuery);
    document.getElementById('clearQueryBtn').addEventListener('click', clearQuery);
    document.getElementById('prevPageBtn').addEventListener('click', () => changePage(-1));
    document.getElementById('nextPageBtn').addEventListener('click', () => changePage(1));

    // 绑定查询模板点击事件
    document.querySelectorAll('.query-template').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('sqlQuery').value = this.getAttribute('data-query');
        });
    });
});

/**
 * 加载数据库表列表
 */
function loadTables() {
    fetch('/api/db/tables')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                tables = data.data;
                renderTablesList(tables);
            } else {
                showError('加载表列表失败: ' + data.message);
            }
        })
        .catch(error => {
            showError('加载表列表失败: ' + error);
        });
}

/**
 * 渲染表列表
 * @param {Array} tables 表列表数据
 */
function renderTablesList(tables) {
    const tablesList = document.getElementById('tablesList');
    tablesList.innerHTML = '';

    if (tables.length === 0) {
        tablesList.innerHTML = '<div class="list-group-item">没有找到表</div>';
        return;
    }

    tables.forEach(table => {
        const item = document.createElement('a');
        item.href = '#';
        item.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
        if (table.name === currentTable) {
            item.classList.add('active');
        }
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = table.name;
        
        const badge = document.createElement('span');
        badge.className = 'badge-table-count';
        badge.textContent = `${table.columns.length} 列`;
        
        item.appendChild(nameSpan);
        item.appendChild(badge);
        
        item.addEventListener('click', function(e) {
            e.preventDefault();
            selectTable(table.name);
        });
        
        tablesList.appendChild(item);
    });
}

/**
 * 选择表
 * @param {string} tableName 表名
 */
function selectTable(tableName) {
    currentTable = tableName;
    currentPage = 1;
    
    // 更新UI
    document.getElementById('currentTableName').textContent = tableName;
    document.getElementById('structureTableName').textContent = tableName + ' 表结构';
    
    // 高亮选中的表
    document.querySelectorAll('#tablesList a').forEach(item => {
        item.classList.remove('active');
        if (item.querySelector('span').textContent === tableName) {
            item.classList.add('active');
        }
    });
    
    // 加载表数据
    loadTableData();
    
    // 加载表结构
    loadTableStructure();
}

/**
 * 加载表数据
 */
function loadTableData() {
    if (!currentTable) return;
    
    const offset = (currentPage - 1) * pageSize;
    const query = `SELECT * FROM ${currentTable} LIMIT ${pageSize} OFFSET ${offset}`;
    
    // 显示加载中
    document.getElementById('dataTable').innerHTML = `
        <thead>
            <tr>
                <th colspan="100%" class="text-center">
                    <div class="loading d-inline-block"></div>
                    <span class="ms-2">加载中...</span>
                </th>
            </tr>
        </thead>
    `;
    
    fetch(`/api/db/query?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderTableData(data.data, data.columns);
                
                // 获取总行数
                fetch(`/api/db/query?query=${encodeURIComponent(`SELECT COUNT(*) as count FROM ${currentTable}`)}`)
                    .then(response => response.json())
                    .then(countData => {
                        if (countData.success && countData.data.length > 0) {
                            totalRows = countData.data[0].count;
                            document.getElementById('rowCount').textContent = `共 ${totalRows} 行`;
                            
                            // 更新分页按钮状态
                            document.getElementById('prevPageBtn').disabled = currentPage <= 1;
                            document.getElementById('nextPageBtn').disabled = (currentPage * pageSize) >= totalRows;
                        }
                    });
            } else {
                showError('加载表数据失败: ' + data.message);
            }
        })
        .catch(error => {
            showError('加载表数据失败: ' + error);
        });
}

/**
 * 渲染表数据
 * @param {Array} data 表数据
 * @param {Array} columns 列名
 */
function renderTableData(data, columns) {
    const table = document.getElementById('dataTable');
    
    if (!data || data.length === 0) {
        table.innerHTML = `
            <thead>
                <tr>
                    <th>暂无数据</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>该表没有数据</td>
                </tr>
            </tbody>
        `;
        return;
    }
    
    // 创建表头
    let thead = '<thead><tr>';
    columns.forEach(column => {
        thead += `<th>${column}</th>`;
    });
    thead += '</tr></thead>';
    
    // 创建表体
    let tbody = '<tbody>';
    data.forEach(row => {
        tbody += '<tr>';
        columns.forEach(column => {
            tbody += `<td>${row[column] !== null ? row[column] : '<span class="text-muted">NULL</span>'}</td>`;
        });
        tbody += '</tr>';
    });
    tbody += '</tbody>';
    
    table.innerHTML = thead + tbody;
}

/**
 * 加载表结构
 */
function loadTableStructure() {
    if (!currentTable) return;
    
    const selectedTable = tables.find(t => t.name === currentTable);
    if (!selectedTable) return;
    
    const structureTable = document.getElementById('structureTable');
    const columns = selectedTable.columns;
    
    if (!columns || columns.length === 0) {
        structureTable.innerHTML = `
            <thead>
                <tr>
                    <th>列名</th>
                    <th>类型</th>
                    <th>非空</th>
                    <th>默认值</th>
                    <th>主键</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="5">没有列信息</td>
                </tr>
            </tbody>
        `;
        return;
    }
    
    // 创建表头
    let thead = `
        <thead>
            <tr>
                <th>列名</th>
                <th>类型</th>
                <th>非空</th>
                <th>默认值</th>
                <th>主键</th>
            </tr>
        </thead>
    `;
    
    // 创建表体
    let tbody = '<tbody>';
    columns.forEach(column => {
        tbody += `
            <tr>
                <td>${column.name}</td>
                <td>${column.type}</td>
                <td>${column.notnull ? '是' : '否'}</td>
                <td>${column.dflt_value !== null ? column.dflt_value : '<span class="text-muted">NULL</span>'}</td>
                <td>${column.pk ? '是' : '否'}</td>
            </tr>
        `;
    });
    tbody += '</tbody>';
    
    structureTable.innerHTML = thead + tbody;
}

/**
 * 执行SQL查询
 */
function runQuery() {
    const query = document.getElementById('sqlQuery').value.trim();
    if (!query) {
        showError('请输入SQL查询语句');
        return;
    }
    
    // 显示加载中
    document.getElementById('queryResultTable').innerHTML = `
        <thead>
            <tr>
                <th colspan="100%" class="text-center">
                    <div class="loading d-inline-block"></div>
                    <span class="ms-2">执行查询中...</span>
                </th>
            </tr>
        </thead>
    `;
    
    fetch(`/api/db/query?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.data) {
                    renderQueryResult(data.data, data.columns);
                    document.getElementById('queryResultCount').textContent = `${data.data.length} 行`;
                } else {
                    // 非SELECT查询
                    document.getElementById('queryResultTable').innerHTML = `
                        <thead>
                            <tr>
                                <th>执行结果</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>${data.message}</td>
                            </tr>
                        </tbody>
                    `;
                    document.getElementById('queryResultCount').textContent = '';
                    
                    // 如果是修改数据的操作，刷新表数据
                    if (query.toLowerCase().includes('insert') || 
                        query.toLowerCase().includes('update') || 
                        query.toLowerCase().includes('delete')) {
                        loadTableData();
                    }
                }
            } else {
                showError('执行查询失败: ' + data.message);
            }
        })
        .catch(error => {
            showError('执行查询失败: ' + error);
        });
}

/**
 * 渲染查询结果
 * @param {Array} data 查询结果数据
 * @param {Array} columns 列名
 */
function renderQueryResult(data, columns) {
    const table = document.getElementById('queryResultTable');
    
    if (!data || data.length === 0) {
        table.innerHTML = `
            <thead>
                <tr>
                    <th>查询结果</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>查询没有返回数据</td>
                </tr>
            </tbody>
        `;
        return;
    }
    
    // 创建表头
    let thead = '<thead><tr>';
    columns.forEach(column => {
        thead += `<th>${column}</th>`;
    });
    thead += '</tr></thead>';
    
    // 创建表体
    let tbody = '<tbody>';
    data.forEach(row => {
        tbody += '<tr>';
        columns.forEach(column => {
            tbody += `<td>${row[column] !== null ? row[column] : '<span class="text-muted">NULL</span>'}</td>`;
        });
        tbody += '</tr>';
    });
    tbody += '</tbody>';
    
    table.innerHTML = thead + tbody;
}

/**
 * 清空查询
 */
function clearQuery() {
    document.getElementById('sqlQuery').value = '';
    document.getElementById('queryResultTable').innerHTML = `
        <thead>
            <tr>
                <th>执行查询后显示结果</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>暂无数据</td>
            </tr>
        </tbody>
    `;
    document.getElementById('queryResultCount').textContent = '';
}

/**
 * 切换页面
 * @param {number} direction 方向，1表示下一页，-1表示上一页
 */
function changePage(direction) {
    const newPage = currentPage + direction;
    if (newPage < 1 || (newPage - 1) * pageSize >= totalRows) return;
    
    currentPage = newPage;
    loadTableData();
}

/**
 * 显示错误信息
 * @param {string} message 错误信息
 */
function showError(message) {
    console.error(message);
    alert('错误: ' + message);
}
// 表格相关JavaScript - 简化版本
console.log('表格JavaScript加载成功');

// 表格相关的辅助函数
function formatNumber(num) {
    return num ? num.toLocaleString() : '0';
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('zh-CN');
}

function showTableError(message) {
    const tableBody = document.getElementById('industriesTableBody');
    if (tableBody) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-danger">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </td>
            </tr>
        `;
    }
}

function showTableLoading() {
    const tableBody = document.getElementById('industriesTableBody');
    if (tableBody) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    <div class="loading-spinner">
                        <i class="fas fa-spinner fa-spin"></i>
                        <span>加载中...</span>
                    </div>
                </td>
            </tr>
        `;
    }
}

console.log('表格JavaScript功能就绪');

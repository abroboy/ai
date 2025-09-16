// 主JavaScript文件
document.addEventListener('DOMContentLoaded', function() {
    console.log('管理台初始化完成');
    
    // 侧边栏菜单点击事件
    const menuItems = document.querySelectorAll('.sidebar-menu li');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // 其他交互逻辑将根据设计图逐步添加
});
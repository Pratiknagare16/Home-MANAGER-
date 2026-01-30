document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Active State
    const currentPath = window.location.pathname;
    const mobileLinks = document.querySelectorAll('.mobile-nav-item');
    
    mobileLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Sidebar Toggle (Mobile)
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('appSidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent immediate closing
            sidebar.classList.toggle('show');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth < 992 && 
                sidebar.classList.contains('show') && 
                !sidebar.contains(e.target) && 
                e.target !== sidebarToggle) {
                sidebar.classList.remove('show');
            }
        });
    }

    // Initialize Tooltips (Bootstrap)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Quick Add Modal Tab Handling
    const quickAddTabs = document.querySelectorAll('#quickAddTabs button');
    quickAddTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (event) {
            // Focus on first input of active tab
            const targetId = event.target.getAttribute('data-bs-target');
            const targetPane = document.querySelector(targetId);
            const firstInput = targetPane.querySelector('input, select, textarea');
            if (firstInput) firstInput.focus();
        });
    });

    // Flash Messages Auto-dismiss
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

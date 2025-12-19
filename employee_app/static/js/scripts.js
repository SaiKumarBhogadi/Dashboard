
// ============================================================
// SIDEBAR TOGGLE FUNCTIONALITY
// ============================================================

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const windowWidth = window.innerWidth;

    // For desktop (> 768px) - collapse/expand sidebar
    if (windowWidth > 768) {
        sidebar.classList.toggle('collapsed');
    } 
    // For mobile/tablet (<= 768px) - show/hide sidebar
    else {
        sidebar.classList.toggle('mobile-visible');
        toggleOverlay();
    }
}

function toggleOverlay() {
    // Create overlay if it doesn't exist
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);
    }

    overlay.classList.toggle('active');

    // Close sidebar when overlay is clicked
    overlay.addEventListener('click', function() {
        document.querySelector('.sidebar').classList.remove('mobile-visible');
        this.classList.remove('active');
    });
}

// Close sidebar when clicking on a menu item
document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const sidebar = document.querySelector('.sidebar');
            const windowWidth = window.innerWidth;

            // Close sidebar on mobile/tablet after clicking menu
            if (windowWidth <= 768 && sidebar.classList.contains('mobile-visible')) {
                sidebar.classList.remove('mobile-visible');
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay) overlay.classList.remove('active');
            }
        });
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        const sidebar = document.querySelector('.sidebar');
        const windowWidth = window.innerWidth;

        if (windowWidth > 768) {
            // Reset mobile states for desktop
            sidebar.classList.remove('mobile-visible', 'mobile-hidden');
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) overlay.classList.remove('active');
        }
    });
});
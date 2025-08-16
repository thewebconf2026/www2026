document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                e.preventDefault();
                
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Add active class to current page in navigation
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.main-nav a');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        // Handle cases where linkPage might be a full path or just a file name
        const linkFileName = linkPage.split('/').pop();

        // Check if the current page matches the link's file name
        if (linkFileName === currentPage || (currentPage === '' && linkFileName === 'index.html')) {
            link.classList.add('active');
        } else if (link.classList.contains('has-dropdown')) {
            // For dropdowns, check if any of its sub-items match the current page
            const dropdownContent = link.nextElementSibling;
            if (dropdownContent && dropdownContent.classList.contains('dropdown')) {
                const subLinks = dropdownContent.querySelectorAll('a');
                subLinks.forEach(subLink => {
                    const subLinkFileName = subLink.getAttribute('href').split('/').pop();
                    if (subLinkFileName === currentPage) {
                        link.classList.add('active');
                    }
                });
            }
        }
    });
});

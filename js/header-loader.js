/**
 * Header Loader - Modular Header Component System
 * Loads shared header component into all pages
 */

class HeaderLoader {
    constructor() {
        this.currentPage = this.getCurrentPage();
        this.basePath = this.getBasePath();
    }

    /**
     * Get the current page name from URL
     */
    getCurrentPage() {
        const path = window.location.pathname;
        const page = path.split('/').pop() || 'index.html';
        return page.replace('.html', '');
    }

    /**
     * Calculate the base path for relative URLs based on current location
     */
    getBasePath() {
        const path = window.location.pathname;
        const depth = (path.match(/\//g) || []).length - 1;
        
        if (depth <= 1) {
            return './'; // Root level
        } else {
            return '../'.repeat(depth - 1); // Subdirectory
        }
    }

    /**
     * Load header component from components/header.html
     */
    async loadHeader() {
        try {
            const headerPath = this.basePath + 'components/header.html';
            const response = await fetch(headerPath);
            
            if (!response.ok) {
                throw new Error(`Failed to load header: ${response.status}`);
            }
            
            const headerHTML = await response.text();
            
            // Insert header into placeholder
            const placeholder = document.getElementById('header-placeholder');
            if (placeholder) {
                placeholder.innerHTML = headerHTML;
                
                // Update navigation to show active page
                this.setActiveNavigation();
                
                // Initialize mobile menu functionality
                this.initializeMobileMenu();
                
                // Fix relative paths in header based on current location
                this.fixRelativePaths();
                
                console.log('✅ Header loaded successfully');
            } else {
                console.error('❌ Header placeholder not found');
            }
            
        } catch (error) {
            console.error('❌ Error loading header:', error);
            // Fallback: show a basic header message
            const placeholder = document.getElementById('header-placeholder');
            if (placeholder) {
                placeholder.innerHTML = '<div style="padding: 20px; background: #f8f9fa; text-align: center;">Header loading...</div>';
            }
        }
    }

    /**
     * Set active navigation item based on current page
     */
    setActiveNavigation() {
        // Remove all active classes
        const navLinks = document.querySelectorAll('.tab-menu a');
        navLinks.forEach(link => link.classList.remove('active'));

        // Add active class to current page
        const currentPageClass = `tab-${this.currentPage}`;
        const activeLink = document.querySelector(`.${currentPageClass}`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        // Special cases for subdirectory pages
        if (this.currentPage.includes('research-tracks') || 
            this.currentPage.includes('industry') || 
            this.currentPage.includes('tutorials')) {
            const callsLink = document.querySelector('.tab-calls');
            if (callsLink) callsLink.classList.add('active');
        }
    }

    /**
     * Fix relative paths in header based on current page location
     */
    fixRelativePaths() {
        const header = document.querySelector('header');
        if (!header) return;

        // Fix logo link
        const logoLink = header.querySelector('.logo a');
        if (logoLink) {
            logoLink.href = this.basePath + 'index.html';
        }

        // Fix logo image src
        const logoImg = header.querySelector('.logo img');
        if (logoImg) {
            logoImg.src = this.basePath + 'images/tentative logo 2.png';
        }

        // Fix all navigation links
        const navLinks = header.querySelectorAll('a[href]');
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('http') && !href.startsWith('#')) {
                // Only fix relative paths, not absolute URLs or anchors
                if (!href.startsWith('./') && !href.startsWith('../')) {
                    link.href = this.basePath + href;
                }
            }
        });
    }

    /**
     * Initialize mobile menu functionality
     */
    initializeMobileMenu() {
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const navContainer = document.querySelector('.main-nav-container');
        
        if (mobileToggle && navContainer) {
            mobileToggle.addEventListener('click', () => {
                navContainer.classList.toggle('active');
            });
        }
    }
}

// Auto-load header when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const headerLoader = new HeaderLoader();
    headerLoader.loadHeader();
});

// Export for manual usage if needed
window.HeaderLoader = HeaderLoader;


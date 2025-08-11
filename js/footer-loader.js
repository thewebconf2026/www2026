// Footer loader script for modular footer system
document.addEventListener('DOMContentLoaded', function() {
    const footerPlaceholder = document.getElementById('footer-placeholder');
    
    if (footerPlaceholder) {
        // Calculate relative path to components directory
        const currentPath = window.location.pathname;
        const pathDepth = (currentPath.match(/\//g) || []).length - 1;
        
        let relativePath = '';
        if (pathDepth === 0) {
            // Root level (no subdirectories)
            relativePath = 'components/footer.html';
        } else {
            // Any subdirectory level - always one level up
            relativePath = '../components/footer.html';
        }
        
        // Load footer content
        fetch(relativePath)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                footerPlaceholder.innerHTML = html;
                
                // Fix relative links in footer based on current page depth
                if (pathDepth > 1) {
                    const links = footerPlaceholder.querySelectorAll('a[href]');
                    links.forEach(link => {
                        const href = link.getAttribute('href');
                        // Only fix relative links (not external links starting with http)
                        if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('../')) {
                            link.setAttribute('href', '../' + href);
                        }
                    });
                }
                
                console.log('✅ Footer loaded successfully');
            })
            .catch(error => {
                console.error('❌ Error loading footer:', error);
                // Fallback: show basic footer
                footerPlaceholder.innerHTML = `
                    <footer>
                        <div class="footer-container">
                            <div class="footer-column">
                                <h3>TheWebConf 2026</h3>
                                <p>April 13-17, 2026</p>
                                <p>Dubai, United Arab Emirates</p>
                            </div>
                        </div>
                    </footer>
                `;
            });
    }
});


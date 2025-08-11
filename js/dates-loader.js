// Important Dates loader script for modular dates system
class DatesLoader {
    constructor() {
        this.datesData = null;
        this.loadDates();
    }

    async loadDates() {
        try {
            // Calculate relative path to data directory
            const currentPath = window.location.pathname;
            const pathDepth = (currentPath.match(/\//g) || []).length - 1;
            
            let relativePath = '';
            if (pathDepth === 0) {
                // Root level (no subdirectories)
                relativePath = 'data/important-dates.json';
            } else {
                // Any subdirectory level - always one level up
                relativePath = '../data/important-dates.json';
            }

            const response = await fetch(relativePath);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.datesData = await response.json();
            console.log('✅ Important dates loaded successfully');
            
            // Auto-populate any date placeholders on the page
            this.populateDatePlaceholders();
            
        } catch (error) {
            console.error('❌ Error loading important dates:', error);
        }
    }

    // Get specific date by category and key
    getDate(category, key) {
        if (!this.datesData || !this.datesData[category] || !this.datesData[category][key]) {
            return null;
        }
        return this.datesData[category][key];
    }

    // Get formatted date string
    getDateString(category, key) {
        const dateInfo = this.getDate(category, key);
        return dateInfo ? dateInfo.date : 'TBD';
    }

    // Get date description
    getDateDescription(category, key) {
        const dateInfo = this.getDate(category, key);
        return dateInfo ? dateInfo.description : '';
    }

    // Generate research track dates list (for homepage and calls page)
    generateResearchTrackDates() {
        if (!this.datesData) return '';
        
        const research = this.datesData.research_track;
        return `
            <li><strong>Abstract deadline:</strong> ${research.abstract_deadline.date}</li>
            <li><strong>Full paper deadline:</strong> ${research.full_paper_deadline.date}</li>
            <li><strong>Rebuttal period:</strong> ${research.rebuttal_period.date}</li>
            <li><strong>Notification of acceptance:</strong> ${research.notification.date}</li>
            <li><strong>Camera ready:</strong> ${research.camera_ready.date}</li>
            <li><strong>Conference:</strong> ${this.datesData.conference.start.date} – ${this.datesData.conference.end.date.split(', ')[1]}</li>
        `;
    }

    // Generate tutorial dates (for tutorial page)
    generateTutorialDates() {
        if (!this.datesData) return '';
        
        const tutorials = this.datesData.tutorials;
        return `
            <li><strong>Proposal submission deadline:</strong> ${tutorials.submission_deadline.date}</li>
            <li><strong>Notification:</strong> ${tutorials.notification.date}</li>
            <li><strong>Materials due:</strong> ${tutorials.materials_due.date}</li>
        `;
    }

    // Auto-populate date placeholders on the page
    populateDatePlaceholders() {
        // Research track dates
        const researchDatesContainer = document.getElementById('research-track-dates');
        if (researchDatesContainer) {
            researchDatesContainer.innerHTML = this.generateResearchTrackDates();
        }

        // Tutorial dates
        const tutorialDatesContainer = document.getElementById('tutorial-dates');
        if (tutorialDatesContainer) {
            tutorialDatesContainer.innerHTML = this.generateTutorialDates();
        }

        // Individual date placeholders (format: data-date="category.key")
        const datePlaceholders = document.querySelectorAll('[data-date]');
        datePlaceholders.forEach(element => {
            const [category, key] = element.getAttribute('data-date').split('.');
            const dateString = this.getDateString(category, key);
            if (dateString !== 'TBD') {
                element.textContent = dateString;
            }
        });
    }
}

// Initialize dates loader when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.datesLoader = new DatesLoader();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DatesLoader;
}


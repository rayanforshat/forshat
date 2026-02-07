// Services Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearch');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const sortSelect = document.getElementById('sortSelect');
    const servicesGrid = document.getElementById('servicesGrid');
    const resultsCount = document.getElementById('resultsCount');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Current filters state
    let currentFilters = {
        search: searchInput ? searchInput.value : '',
        category: getActiveCategory(),
        sort: sortSelect ? sortSelect.value : 'default'
    };

    // Initialize
    init();

    function init() {
        // Search input event
        if (searchInput) {
            searchInput.addEventListener('input', debounce(handleSearch, 300));
        }

        // Clear search button
        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', clearSearch);
        }

        // Category buttons
        categoryBtns.forEach(btn => {
            btn.addEventListener('click', handleCategoryChange);
        });

        // Sort select
        if (sortSelect) {
            sortSelect.addEventListener('change', handleSortChange);
        }

        // Update results count on load
        updateResultsCount();
    }

    // Handle search input
    function handleSearch(e) {
        currentFilters.search = e.target.value.trim();
        
        // Show/hide clear button
        if (clearSearchBtn) {
            clearSearchBtn.style.display = currentFilters.search ? 'flex' : 'none';
        }
        
        applyFilters();
    }

    // Clear search
    function clearSearch() {
        if (searchInput) {
            searchInput.value = '';
            currentFilters.search = '';
            if (clearSearchBtn) {
                clearSearchBtn.style.display = 'none';
            }
            applyFilters();
            searchInput.focus();
        }
    }

    // Handle category change
    function handleCategoryChange(e) {
        const btn = e.currentTarget;
        const category = btn.dataset.category;

        // Update active state
        categoryBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update filter
        currentFilters.category = category;
        applyFilters();
    }

    // Handle sort change
    function handleSortChange(e) {
        currentFilters.sort = e.target.value;
        applyFilters();
    }

    // Apply all filters
    function applyFilters() {
        const rows = servicesGrid.querySelectorAll('.service-row');
        let visibleCount = 0;

        rows.forEach(row => {
            const serviceName = row.querySelector('.service-name')?.textContent.toLowerCase() || '';
            const serviceDesc = row.querySelector('.service-desc')?.textContent.toLowerCase() || '';
            const category = row.dataset.category || '';

            // Search filter
            const searchMatch = !currentFilters.search || 
                serviceName.includes(currentFilters.search.toLowerCase()) ||
                serviceDesc.includes(currentFilters.search.toLowerCase());

            // Category filter
            const categoryMatch = currentFilters.category === 'all' || 
                category === currentFilters.category;

            // Show/hide row
            if (searchMatch && categoryMatch) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        // Sort rows
        sortRows();

        // Update results count
        updateResultsCount(visibleCount);

        // Show/hide no results message
        toggleNoResults(visibleCount === 0);

        // Update URL without reload
        updateURL();
    }

    // Sort rows
    function sortRows() {
        const tbody = servicesGrid.querySelector('tbody');
        if (!tbody) return;
        
        const rows = Array.from(tbody.querySelectorAll('.service-row'));
        const sortedRows = [...rows].sort((a, b) => {
            switch (currentFilters.sort) {
                case 'price_low':
                    return getPrice(a) - getPrice(b);
                case 'price_high':
                    return getPrice(b) - getPrice(a);
                case 'newest':
                    return getTimestamp(b) - getTimestamp(a);
                case 'popular':
                    return getFeatured(b) - getFeatured(a);
                default:
                    return 0;
            }
        });

        // Re-append in sorted order
        sortedRows.forEach(row => {
            if (row.style.display !== 'none') {
                tbody.appendChild(row);
            }
        });
    }

    // Helper: Get price from row
    function getPrice(row) {
        const priceElement = row.querySelector('.price-value');
        
        if (priceElement) {
            const priceText = priceElement.textContent.replace(/[^\d.]/g, '');
            return parseFloat(priceText) || 0;
        }
        return 0;
    }

    // Helper: Get timestamp (for sorting by newest)
    function getTimestamp(row) {
        const tbody = row.closest('tbody');
        if (!tbody) return 0;
        return Array.from(tbody.children).indexOf(row);
    }

    // Helper: Check if featured
    function getFeatured(row) {
        return row.querySelector('.badge-featured') ? 1 : 0;
    }

    // Update results count
    function updateResultsCount(count) {
        if (resultsCount) {
            if (count !== undefined) {
                resultsCount.textContent = count;
            } else {
                const visibleRows = servicesGrid.querySelectorAll('.service-row:not([style*="display: none"])');
                resultsCount.textContent = visibleRows.length;
            }
        }
    }

    // Toggle no results message
    function toggleNoResults(show) {
        let noResults = document.getElementById('noResults');
        const table = servicesGrid.querySelector('table');
        
        if (show) {
            if (table) table.style.display = 'none';
            if (noResults) noResults.style.display = 'block';
        } else {
            if (table) table.style.display = 'table';
            if (noResults) noResults.style.display = 'none';
        }
    }

    // Get active category
    function getActiveCategory() {
        const activeBtn = document.querySelector('.category-btn.active');
        return activeBtn ? activeBtn.dataset.category : 'all';
    }

    // Update URL without reload
    function updateURL() {
        const params = new URLSearchParams();
        
        if (currentFilters.search) {
            params.set('search', currentFilters.search);
        }
        
        if (currentFilters.category && currentFilters.category !== 'all') {
            params.set('category', currentFilters.category);
        }
        
        if (currentFilters.sort && currentFilters.sort !== 'default') {
            params.set('sort', currentFilters.sort);
        }

        const newURL = params.toString() 
            ? `${window.location.pathname}?${params.toString()}`
            : window.location.pathname;
        
        window.history.replaceState({}, '', newURL);
    }

    // Debounce function for search input
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});

// Reset all filters (called from button)
function resetFilters() {
    // Reset search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = '';
        const clearBtn = document.getElementById('clearSearch');
        if (clearBtn) {
            clearBtn.style.display = 'none';
        }
    }

    // Reset category to "all"
    const categoryBtns = document.querySelectorAll('.category-btn');
    categoryBtns.forEach(btn => {
        if (btn.dataset.category === 'all') {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Reset sort
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.value = 'default';
    }

    // Show all rows
    const rows = document.querySelectorAll('.service-row');
    rows.forEach(row => {
        row.style.display = '';
    });

    // Show table, hide no results
    const table = document.querySelector('.services-table');
    const noResults = document.getElementById('noResults');
    if (table) table.style.display = 'table';
    if (noResults) noResults.style.display = 'none';

    // Update results count
    const resultsCount = document.getElementById('resultsCount');
    if (resultsCount) {
        resultsCount.textContent = rows.length;
    }

    // Clear URL params
    window.history.replaceState({}, '', window.location.pathname);

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Book service function
function bookService(serviceName) {
    const message = encodeURIComponent(`مرحباً، أود حجز موعد لـ: ${serviceName}`);
    const whatsappURL = `https://wa.me/966547199970?text=${message}`;
    window.open(whatsappURL, '_blank');
}

// Smooth scroll for categories on mobile
const categoriesWrapper = document.querySelector('.categories-wrapper');
if (categoriesWrapper) {
    let isDown = false;
    let startX;
    let scrollLeft;

    categoriesWrapper.addEventListener('mousedown', (e) => {
        isDown = true;
        categoriesWrapper.style.cursor = 'grabbing';
        startX = e.pageX - categoriesWrapper.offsetLeft;
        scrollLeft = categoriesWrapper.scrollLeft;
    });

    categoriesWrapper.addEventListener('mouseleave', () => {
        isDown = false;
        categoriesWrapper.style.cursor = 'grab';
    });

    categoriesWrapper.addEventListener('mouseup', () => {
        isDown = false;
        categoriesWrapper.style.cursor = 'grab';
    });

    categoriesWrapper.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - categoriesWrapper.offsetLeft;
        const walk = (x - startX) * 2;
        categoriesWrapper.scrollLeft = scrollLeft - walk;
    });
}
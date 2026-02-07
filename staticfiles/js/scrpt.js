// Doctors Carousel Functionality
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('doctorsCarousel');
    const scrollLeftBtn = document.getElementById('scrollLeft');
    const scrollRightBtn = document.getElementById('scrollRight');
    
    if (carousel && scrollLeftBtn && scrollRightBtn) {
        // Calculate scroll amount based on card width
        const card = document.querySelector('.doctor-card');
        const cardWidth = card ? card.offsetWidth + 25 : 245; // card width + gap
        
        // For RTL layout, we need to handle scrolling differently
        scrollRightBtn.addEventListener('click', () => {
            // In RTL, scrolling RIGHT moves content to the RIGHT (negative scroll)
            carousel.scrollBy({
                left: -cardWidth * 3, // Scroll 3 cards to the right
                behavior: 'smooth'
            });
        });

        scrollLeftBtn.addEventListener('click', () => {
            // In RTL, scrolling LEFT moves content to the LEFT (positive scroll)
            carousel.scrollBy({
                left: cardWidth * 3, // Scroll 3 cards to the left
                behavior: 'smooth'
            });
        });

        // Update button states based on scroll position
        function updateButtonStates() {
            const scrollWidth = carousel.scrollWidth;
            const clientWidth = carousel.clientWidth;
            const scrollLeft = Math.abs(carousel.scrollLeft); // Use absolute value for RTL
            
            // Enable/disable buttons based on scroll position
            scrollLeftBtn.disabled = scrollLeft <= 10;
            scrollRightBtn.disabled = scrollLeft + clientWidth >= scrollWidth - 10;
            
            // Add/remove disabled styling
            if (scrollLeftBtn.disabled) {
                scrollLeftBtn.classList.add('disabled');
            } else {
                scrollLeftBtn.classList.remove('disabled');
            }
            
            if (scrollRightBtn.disabled) {
                scrollRightBtn.classList.add('disabled');
            } else {
                scrollRightBtn.classList.remove('disabled');
            }
        }

        // Initialize button states
        updateButtonStates();
        
        // Update button states on scroll
        carousel.addEventListener('scroll', updateButtonStates);
        
        // Reset scroll position to start for RTL
        setTimeout(() => {
            // For RTL, start at the rightmost position
            carousel.scrollLeft = carousel.scrollWidth - carousel.clientWidth;
            updateButtonStates();
        }, 100);

        // Add keyboard navigation support
        document.addEventListener('keydown', (e) => {
            if (!carousel.contains(document.activeElement)) return;
            
            if (e.key === 'ArrowRight' || e.key === 'Right') {
                e.preventDefault();
                scrollRightBtn.click();
            } else if (e.key === 'ArrowLeft' || e.key === 'Left') {
                e.preventDefault();
                scrollLeftBtn.click();
            }
        });

        // Add mousewheel/trackpad horizontal scrolling
        carousel.addEventListener('wheel', (e) => {
            e.preventDefault();
            carousel.scrollBy({
                left: e.deltaY < 0 ? -100 : 100,
                behavior: 'smooth'
            });
        });

        // Touch/swipe support for mobile
        let touchStartX = 0;
        let touchStartScrollLeft = 0;
        let isDragging = false;

        carousel.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].pageX;
            touchStartScrollLeft = carousel.scrollLeft;
            isDragging = true;
            carousel.style.scrollBehavior = 'auto';
        });

        carousel.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            
            const touchX = e.touches[0].pageX;
            const distance = touchX - touchStartX;
            carousel.scrollLeft = touchStartScrollLeft - distance;
        });

        carousel.addEventListener('touchend', () => {
            isDragging = false;
            carousel.style.scrollBehavior = 'smooth';
        });
    }

    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenuToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Scroll to top button
    const scrollTopBtn = document.getElementById('scrollTop');
    
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                scrollTopBtn.style.display = 'flex';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        });

        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// Show working message for incomplete pages
function showWorkingMessage(event) {
    event.preventDefault();
    alert('هذه الصفحة قيد الإنشاء. سيتم إطلاقها قريباً!');
}





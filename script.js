// 100K SHAKES - MAIN JAVASCRIPT

// ════════════════════════════════════════════════
//  LOADING SCREEN
// ════════════════════════════════════════════════

const loadingScreen = document.getElementById('loadingScreen');
const loadingBar = document.getElementById('loadingBar');
const loadingPercent = document.getElementById('loadingPercent');

if (loadingScreen) {
    let progress = 0;
    
    // Simulate loading progress
    const updateProgress = () => {
        progress += Math.random() * 15;
        if (progress > 100) progress = 100;
        
        loadingBar.style.width = progress + '%';
        loadingPercent.textContent = Math.floor(progress) + '%';
        
        if (progress < 100) {
            setTimeout(updateProgress, 100 + Math.random() * 200);
        } else {
            // Wait for actual page load
            if (document.readyState === 'complete') {
                setTimeout(() => {
                    loadingScreen.classList.add('hidden');
                    setTimeout(() => loadingScreen.remove(), 500);
                }, 300);
            } else {
                window.addEventListener('load', () => {
                    setTimeout(() => {
                        loadingScreen.classList.add('hidden');
                        setTimeout(() => loadingScreen.remove(), 500);
                    }, 300);
                });
            }
        }
    };
    
    // Start loading animation
    updateProgress();
}

// Mobile Menu Toggle
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navMenu = document.getElementById('navMenu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// Navbar scroll effect
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    if (scrollY > 80) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
        // Back in hero zone — go transparent
        if (navbar) {
            navbar.style.background = 'transparent';
            navbar.style.backdropFilter = 'none';
        }
    }
}, { passive: true });

// Carousel functionality
const carouselTrack = document.getElementById('carouselTrack');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

if (carouselTrack && prevBtn && nextBtn) {
    let currentIndex = 0;
    const slides = carouselTrack.querySelectorAll('.carousel-slide');
    const totalSlides = slides.length;
    const slideWidth = slides[0]?.offsetWidth || 280;
    const gap = 32; // 2rem gap
    const moveDistance = slideWidth + gap;

    function updateCarousel() {
        carouselTrack.style.transform = `translateX(-${currentIndex * moveDistance}px)`;
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateCarousel();
    }

    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);

    // Auto-play carousel
    setInterval(nextSlide, 5000);

    // Touch/swipe support for mobile
    let startX = 0;
    let isDragging = false;

    carouselTrack.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
    });

    carouselTrack.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
    });

    carouselTrack.addEventListener('touchend', (e) => {
        if (!isDragging) return;
        const endX = e.changedTouches[0].clientX;
        const diff = startX - endX;

        if (Math.abs(diff) > 50) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
        isDragging = false;
    });
}

// Newsletter form submission
const newsletterForm = document.getElementById('newsletterForm');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input[type="email"]').value;
        
        // Simulate form submission
        alert(`Thank you for subscribing! We'll send updates to ${email}`);
        newsletterForm.reset();
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offsetTop = target.offsetTop - 70; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Menu filter functionality (for menu page)
const filterButtons = document.querySelectorAll('.filter-btn');
const menuItems = document.querySelectorAll('.menu-item');

if (filterButtons.length > 0 && menuItems.length > 0) {
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const filter = button.getAttribute('data-filter');

            menuItems.forEach(item => {
                if (filter === 'all' || item.classList.contains(filter)) {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                    }, 10);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
}

// Initialize menu items with transition styles
if (menuItems.length > 0) {
    menuItems.forEach(item => {
        item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    });
}

// Form validation and submission (for contact page)
const contactForm = document.querySelector('.contact-form form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);
        
        // Simulate form submission
        alert('Thank you for your message! We\'ll get back to you soon.');
        contactForm.reset();
    });
}

// Lazy loading for images (if implemented)
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Add active class to current page in navigation
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
const navLinksAll = document.querySelectorAll('.nav-menu a');

navLinksAll.forEach(link => {
    const linkPage = link.getAttribute('href');
    if (linkPage === currentPage || (currentPage === '' && linkPage === 'index.html')) {
        link.classList.add('active');
    }
});

// ════════════════════════════════════════════════
//  HERO VIDEO SCROLL-SCRUB + TITLE FADE-OUT
// ════════════════════════════════════════════════

const heroVideo = document.getElementById('heroVideo');
const heroTitleOverlay = document.getElementById('heroTitleOverlay');

if (heroVideo) {
    // Wait for video metadata to load so we know the duration
    heroVideo.addEventListener('loadedmetadata', () => {
        heroVideo.currentTime = 0;
    });
    // Force load
    heroVideo.load();

    // Scroll-scrub: map scroll position to video timeline
    const heroScrollSpacer = document.querySelector('.hero-scroll-spacer');
    
    window.addEventListener('scroll', () => {
        const scrollY = window.pageYOffset;
        const spacerHeight = heroScrollSpacer ? heroScrollSpacer.offsetHeight : window.innerHeight * 2;
        
        // Map scroll to video time — START AT 50% (halfway through video)
        // Scroll 0 → spacerHeight maps to video 50% → 100%
        if (heroVideo.duration && isFinite(heroVideo.duration)) {
            const maxScroll = spacerHeight;
            const scrollFraction = Math.min(Math.max(scrollY / maxScroll, 0), 1);
            // Start at 50% of video, end at 100%
            const videoStartTime = heroVideo.duration * 0.5;
            const videoEndTime = heroVideo.duration;
            heroVideo.currentTime = videoStartTime + (scrollFraction * (videoEndTime - videoStartTime));
        }
        
        // Hero title fades out ONLY at the very end of scroll spacer (last 10%)
        if (heroTitleOverlay) {
            const fadeStart = spacerHeight * 0.9; // Last 10% of spacer
            const fadeEnd = spacerHeight;
            if (scrollY >= fadeStart) {
                const progress = Math.min((scrollY - fadeStart) / (fadeEnd - fadeStart), 1);
                heroTitleOverlay.style.opacity = 1 - progress;
            } else {
                heroTitleOverlay.style.opacity = 1; // Fully visible until fadeStart
            }
        }
    }, { passive: true });
}

// ════════════════════════════════════════════════
//  INNER PAGE HERO VIDEO SCRUB
// ════════════════════════════════════════════════

const innerHeroVideo = document.getElementById('innerHeroVideo');
if (innerHeroVideo) {
    innerHeroVideo.load();

    window.addEventListener('scroll', () => {
        const scrollY = window.pageYOffset;
        const pageHeader = document.querySelector('.page-header');
        const maxScroll  = pageHeader ? pageHeader.offsetHeight : window.innerHeight;

        // Scrub video with scroll
        if (innerHeroVideo.duration && isFinite(innerHeroVideo.duration)) {
            const fraction = Math.min(Math.max(scrollY / maxScroll, 0), 1);
            innerHeroVideo.currentTime = fraction * innerHeroVideo.duration;
        }

        // Fade page header title out as content curtain approaches
        const innerTitle = document.querySelector('.page-header-content');
        if (innerTitle) {
            const fadeEnd   = maxScroll * 0.6;
            const fadeStart = maxScroll * 0.1;
            const progress  = Math.min(Math.max((scrollY - fadeStart) / (fadeEnd - fadeStart), 0), 1);
            innerTitle.style.opacity = 1 - progress;
        }
    }, { passive: true });
}

// ════════════════════════════════════════════════
//  SCROLL-BLEND SHAKE SECTIONS
// ════════════════════════════════════════════════

const scrollBlendContainer = document.getElementById('scrollBlendContainer');
const scrollBlendSections = document.getElementById('scrollBlendSections');
const mainContentCurtain = document.getElementById('mainContentCurtain');

if (scrollBlendContainer && scrollBlendSections) {
    // Featured shakes data — backgrounds chosen by vision analysis for maximum contrast/pop
    const featuredShakes = [
        {
            name: "Oreo Delight",
            tag: "Popular",
            image: "images/oreo-delight-nobg.webp",
            desc: "Classic cookie perfection in every sip. Creamy cookies-and-cream blended with premium vanilla ice cream.",
            bg: "#00205B",      // Oreo brand dark navy blue
            navAccent: "#003087", // Oreo blue accent
            category: "StraightShake"
        },
        {
            name: "Strawberry Dream",
            tag: "Fresh",
            image: "images/strawberry-dream-nobg.webp",
            desc: "Fresh strawberries blended to perfection. Vibrant pink milkshake with real fruit flavor.",
            bg: "#5C0020",      // Deep strawberry crimson
            navAccent: "#9B1040", // Raspberry accent
            category: "StraightShake"
        },
        {
            name: "Milo Magic",
            tag: "Signature",
            image: "images/milo-magic-nobg.webp",
            desc: "Rich chocolate malt indulgence. Deep malty chocolate meets premium ice cream.",
            bg: "#004D1A",      // Milo brand deep green
            navAccent: "#006E25", // Milo green accent
            category: "StraightShake"
        },
        {
            name: "Jäger Shake",
            tag: "Premium · 18+",
            image: "images/jager-shake-nobg.webp",
            desc: "Premium alcohol-infused luxury. Jägermeister meets rich chocolate and vanilla.",
            bg: "#2A1000",      // Deep amber/brown — Jäger orange-brown theme
            navAccent: "#7A3500", // Burnt orange-brown Jäger accent
            category: "ShotShake"
        },
        {
            name: "Amarula Bliss",
            tag: "Luxury · 18+",
            image: "images/amarula-bliss-nobg.webp",
            desc: "Creamy liqueur meets milkshake perfection. Smooth, luxurious, and irresistibly indulgent.",
            bg: "#2D3D1A",      // Dark pistachio/sage green — Amarula feel
            navAccent: "#4A6828", // Pistachio accent
            category: "ShotShake"
        },
        {
            name: "Strawberry Kiss",
            tag: "Sweet · 18+",
            image: "images/strawberry-kiss-nobg.webp",
            desc: "Strawberry liqueur infused shake with white chocolate sprinkles. Sweet, fruity, and irresistibly indulgent.",
            bg: "#4A0020",      // Deep rose — Strawberry Lips brand pink
            navAccent: "#8B1045", // Rose-red accent
            category: "ShotShake"
        }
    ];

    // Color interpolation utilities
    function hexToRgb(hex) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return [r, g, b];
    }

    function rgbToHex(r, g, b) {
        return '#' + [r, g, b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
    }

    function lerpColor(colorA, colorB, t) {
        const a = hexToRgb(colorA);
        const b = hexToRgb(colorB);
        return rgbToHex(
            a[0] + (b[0] - a[0]) * t,
            a[1] + (b[1] - a[1]) * t,
            a[2] + (b[2] - a[2]) * t
        );
    }

    // Floating ingredient images — 3 BIG elements per shake, spread left / center / right
    const floatingImages = {
        "Oreo Delight": [
            { src: "images/floating/oreo-delight-float-1.webp", top: "55%", left: "2%", width: "280px" },
            { src: "images/floating/oreo-delight-float-2.webp", top: "8%", left: "35%", width: "250px" },
            { src: "images/floating/oreo-delight-float-3.webp", top: "20%", right: "2%", width: "300px" }
        ],
        "Strawberry Dream": [
            { src: "images/floating/strawberry-dream-float-1.webp", top: "15%", left: "3%", width: "300px" },
            { src: "images/floating/strawberry-dream-float-2.webp", top: "50%", left: "30%", width: "260px" },
            { src: "images/floating/strawberry-dream-float-3.webp", top: "10%", right: "3%", width: "280px" }
        ],
        "Milo Magic": [
            { src: "images/floating/milo-magic-float-1.webp", top: "50%", left: "2%", width: "320px" },
            { src: "images/floating/milo-magic-float-2.webp", top: "10%", left: "32%", width: "240px" },
            { src: "images/floating/milo-magic-float-3.webp", top: "25%", right: "3%", width: "260px" }
        ],
        "Jäger Shake": [
            { src: "images/floating/jager-shake-float-1.webp", top: "12%", left: "3%", width: "280px" },
            { src: "images/floating/jager-shake-float-2.webp", top: "55%", left: "28%", width: "260px" },
            { src: "images/floating/jager-shake-float-3.webp", top: "18%", right: "2%", width: "300px" }
        ],
        "Amarula Bliss": [
            { src: "images/floating/amarula-bliss-float-1.webp", top: "18%", left: "2%", width: "300px" },
            { src: "images/floating/amarula-bliss-float-2.webp", top: "8%", left: "33%", width: "250px" },
            { src: "images/floating/amarula-bliss-float-3.webp", top: "50%", right: "3%", width: "280px" }
        ],
        "Strawberry Kiss": [
            { src: "images/floating/strawberry-kiss-float-1.webp", top: "50%", left: "3%", width: "280px" },
            { src: "images/floating/strawberry-kiss-float-2.webp", top: "10%", left: "30%", width: "260px" },
            { src: "images/floating/strawberry-kiss-float-3.webp", top: "15%", right: "2%", width: "300px" }
        ]
    };

    // Generate sections
    featuredShakes.forEach((shake, i) => {
        const section = document.createElement('div');
        section.className = `scroll-blend-section${i % 2 === 1 ? ' flip' : ''}`;
        section.dataset.index = i;
        section.id = `shake-${i}`;

        // Build floating elements HTML
        const floats = floatingImages[shake.name] || [];
        let floatingHTML = '<div class="floating-elements">';
        floats.forEach((f) => {
            let style = `width: ${f.width};`;
            if (f.top) style += ` top: ${f.top};`;
            if (f.bottom) style += ` bottom: ${f.bottom};`;
            if (f.left) style += ` left: ${f.left};`;
            if (f.right) style += ` right: ${f.right};`;
            floatingHTML += `<img src="${f.src}" class="floating-ingredient" style="${style}" alt="" loading="lazy" />`;
        });
        floatingHTML += '</div>';

        section.innerHTML = `
            ${floatingHTML}
            <div class="scroll-blend-content">
                <div class="scroll-blend-visual">
                    <img src="${shake.image}" alt="${shake.name}" class="scroll-blend-image" />
                </div>
                <div class="scroll-blend-info">
                    <span class="scroll-blend-tag">${shake.tag}</span>
                    <h2 class="scroll-blend-name">${shake.name}</h2>
                    <p class="scroll-blend-desc">${shake.desc}</p>
                    <a href="menu.html" class="scroll-blend-cta">View Menu</a>
                </div>
            </div>
        `;

        scrollBlendSections.appendChild(section);
    });

    // ── Set initial curtain background ──
    if (mainContentCurtain) {
        mainContentCurtain.style.backgroundColor = featuredShakes[0].bg;
    }

    // Helper: hex → rgba string
    function hexToRgba(hex, alpha) {
        const [r, g, b] = hexToRgb(hex);
        return `rgba(${r},${g},${b},${alpha})`;
    }

    // ── Smooth scroll-based color blending (no instant snaps) ──
    const sections = document.querySelectorAll('.scroll-blend-section');
    const bgColors = featuredShakes.map(s => s.bg);
    const accentColors = featuredShakes.map(s => s.navAccent);

    function updateColorsOnScroll() {
        if (!mainContentCurtain) return;

        const scrollY = window.pageYOffset;
        const curtainTop = mainContentCurtain.offsetTop;
        const relativeScroll = scrollY - curtainTop;

        if (relativeScroll < 0) {
            // Before curtain — use first color
            mainContentCurtain.style.backgroundColor = bgColors[0];
            if (navbar) {
                navbar.style.background = hexToRgba(accentColors[0], 0.88);
                navbar.style.backdropFilter = 'blur(14px)';
            }
            return;
        }

        const sectionHeight = window.innerHeight;
        const sectionIndex = Math.floor(relativeScroll / sectionHeight);
        const sectionProgress = (relativeScroll % sectionHeight) / sectionHeight;

        // Smooth lerp between current and next section
        if (sectionIndex < bgColors.length - 1) {
            const currentBg = bgColors[sectionIndex];
            const nextBg = bgColors[sectionIndex + 1];
            const blendedBg = lerpColor(currentBg, nextBg, sectionProgress);
            mainContentCurtain.style.backgroundColor = blendedBg;

            const currentAccent = accentColors[sectionIndex];
            const nextAccent = accentColors[sectionIndex + 1];
            const blendedAccent = lerpColor(currentAccent, nextAccent, sectionProgress);
            if (navbar) {
                navbar.style.background = hexToRgba(blendedAccent, 0.88);
                navbar.style.backdropFilter = 'blur(14px)';
            }
        } else {
            // Last section — use final color
            mainContentCurtain.style.backgroundColor = bgColors[bgColors.length - 1];
            if (navbar) {
                navbar.style.background = hexToRgba(accentColors[accentColors.length - 1], 0.88);
                navbar.style.backdropFilter = 'blur(14px)';
            }
        }

        // Show/hide sections based on scroll (for animations)
        sections.forEach((section, idx) => {
            const sectionTop = curtainTop + (idx * sectionHeight);
            const sectionBottom = sectionTop + sectionHeight;
            const isVisible = scrollY >= sectionTop - sectionHeight * 0.3 && scrollY < sectionBottom + sectionHeight * 0.3;
            if (isVisible) {
                section.classList.add('visible');
            } else {
                section.classList.remove('visible');
            }
        });
    }

    // Throttled scroll handler for smooth color blending
    let scrollTicking = false;
    window.addEventListener('scroll', () => {
        if (!scrollTicking) {
            requestAnimationFrame(() => {
                updateColorsOnScroll();
                scrollTicking = false;
            });
            scrollTicking = true;
        }
    }, { passive: true });

    // Initial update
    updateColorsOnScroll();
}




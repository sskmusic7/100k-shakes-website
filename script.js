// 100K SHAKES - MAIN JAVASCRIPT

// ════════════════════════════════════════════════
//  LOADING SCREEN — REAL ASSET PRELOADER
//  Buffers all videos + images behind the loading mask
//  so animations and scrolling run smooth from frame 1
// ════════════════════════════════════════════════

const loadingScreen = document.getElementById('loadingScreen');
const loadingBar    = document.getElementById('loadingBar');
const loadingPercent = document.getElementById('loadingPercent');

// Lock scroll while loading
if (loadingScreen) {
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
}

function dismissLoader() {
    if (!loadingScreen) return;
    // Unlock scroll
    document.body.classList.remove('is-loading');
    document.body.style.overflow = '';
    document.documentElement.style.overflow = '';
    // Reset scroll to top so hero starts fresh
    window.scrollTo(0, 0);
    // Animate out
    loadingScreen.classList.add('hidden');
    setTimeout(() => loadingScreen.remove(), 600);
}

function setLoaderProgress(pct) {
    if (loadingBar)     loadingBar.style.width = pct + '%';
    if (loadingPercent) loadingPercent.textContent = Math.round(pct) + '%';
}

if (loadingScreen) {
    // ── Collect every heavy asset on the page ──
    const assetPromises = [];
    let loaded = 0;
    let totalAssets = 0;

    // Helper: create a promise that resolves when an image is loaded
    function preloadImage(src) {
        return new Promise(resolve => {
            const img = new Image();
            img.onload  = resolve;
            img.onerror = resolve; // don't block on broken images
            img.src = src;
        });
    }

    // Helper: create a promise that resolves when a video is buffered enough
    function preloadVideo(videoEl) {
        return new Promise(resolve => {
            if (!videoEl) { resolve(); return; }

            // Force the video to start loading/buffering
            videoEl.load();

            const checkReady = () => {
                // Consider ready if we have enough data buffered
                // HAVE_CURRENT_DATA (2) = can render current frame
                // HAVE_FUTURE_DATA (3) = can play next frame
                // HAVE_ENOUGH_DATA (4) = can play without buffering
                if (videoEl.readyState >= 3) {
                    videoEl.removeEventListener('canplay', checkReady);
                    videoEl.removeEventListener('loadeddata', checkReady);
                    resolve();
                }
            };

            // Try multiple events to catch when video is ready
            videoEl.addEventListener('canplay', checkReady, { once: true });
            videoEl.addEventListener('loadeddata', checkReady, { once: true });

            // Also check immediately in case already loaded
            if (videoEl.readyState >= 3) {
                resolve();
                return;
            }

            // Timeout fallback — give it time to buffer (max 10s per video)
            setTimeout(resolve, 10000);
        });
    }

    // 1) VIDEOS — the heaviest assets
    const heroVideo    = document.getElementById('heroVideo');
    if (heroVideo)    assetPromises.push(preloadVideo(heroVideo));

    // 2) IMAGES already in the DOM (carousel, social, elevated text, etc.)
    document.querySelectorAll('img[src]').forEach(img => {
        // Always preload images, even if they appear complete
        // This ensures they're fully decoded and ready
        assetPromises.push(preloadImage(img.src));
    });

    // 3) Background images in inline styles (carousel shake-image divs)
    document.querySelectorAll('[style*="background-image"]').forEach(el => {
        const match = el.style.backgroundImage.match(/url\(['"]?(.+?)['"]?\)/);
        if (match && match[1]) {
            assetPromises.push(preloadImage(match[1]));
        }
    });

    // 4) Key images that will be injected by JS later (scroll-blend shakes + floating)
    const criticalImages = [
        'images/elevated-text-nobg.png?v=1',  // Elevated text image
        'images/oreo-delight-nobg.webp',
        'images/strawberry-dream-nobg.webp',
        'images/milo-magic-nobg.webp',
        'images/jager-shake-nobg.webp',
        'images/amarula-bliss-nobg.webp',
        'images/strawberry-kiss-nobg.webp'
    ];
    criticalImages.forEach(src => assetPromises.push(preloadImage(src)));

    // 5) Floating ingredient images (preload so they don't pop-in later)
    const floatShakes = ['oreo-delight','strawberry-dream','milo-magic','jager-shake','amarula-bliss','strawberry-kiss'];
    floatShakes.forEach(name => {
        for (let i = 1; i <= 3; i++) {
            assetPromises.push(preloadImage(`images/floating/${name}-float-${i}.webp`));
        }
    });

    totalAssets = assetPromises.length;

    // ── Track progress as each asset finishes ──
    let smoothProgress = 0;
    let targetProgress = 0;

    // Smooth progress animation (don't jump, glide)
    const progressInterval = setInterval(() => {
        if (smoothProgress < targetProgress) {
            smoothProgress += (targetProgress - smoothProgress) * 0.15; // ease toward target
            if (targetProgress - smoothProgress < 0.5) smoothProgress = targetProgress;
            setLoaderProgress(smoothProgress);
        }
    }, 30);

    assetPromises.forEach(p => {
        p.then(() => {
            loaded++;
            targetProgress = Math.min((loaded / totalAssets) * 100, 100);
        });
    });

    // ── All done → dismiss ──
    Promise.all(assetPromises).then(() => {
        targetProgress = 100;
        // Let the bar animate to 100% before dismissing
        setTimeout(() => {
            clearInterval(progressInterval);
            setLoaderProgress(100);
            setTimeout(dismissLoader, 400);
        }, 300);
    });

    // ── Safety net: dismiss after 25s no matter what ──
    setTimeout(() => {
        clearInterval(progressInterval);
        setLoaderProgress(100);
        dismissLoader();
    }, 25000);
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

if (carouselTrack) {
    const slides = carouselTrack.querySelectorAll('.carousel-slide');
    const totalSlides = slides.length;

    // Detect mobile: buttons are hidden via CSS on ≤768px
    const isMobile = () => window.innerWidth <= 768;

    // ── Desktop: JS-driven transform carousel ──
    let currentIndex = 0;
    let autoPlayTimer = null;

    function getSlideMetrics() {
        const slide = slides[0];
        if (!slide) return { slideWidth: 280, gap: 32 };
        const slideWidth = slide.offsetWidth;
        const gap = parseInt(getComputedStyle(carouselTrack).gap) || 32;
        return { slideWidth, gap };
    }

    function updateCarousel() {
        if (isMobile()) {
            // On mobile, remove transform so CSS scroll-snap works
            carouselTrack.style.transform = '';
            return;
        }
        const { slideWidth, gap } = getSlideMetrics();
        carouselTrack.style.transform = `translateX(-${currentIndex * (slideWidth + gap)}px)`;
    }

    function nextSlide() {
        if (isMobile()) return; // Let CSS handle mobile
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
    }

    function prevSlide() {
        if (isMobile()) return;
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateCarousel();
    }

    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);

    // Auto-play only on desktop
    function startAutoPlay() {
        if (autoPlayTimer) clearInterval(autoPlayTimer);
        if (!isMobile()) {
            autoPlayTimer = setInterval(nextSlide, 5000);
        }
    }
    startAutoPlay();

    // On resize: re-check mobile vs desktop
    window.addEventListener('resize', () => {
        updateCarousel();
        startAutoPlay();
    });

    // Initial state: clear transform on mobile
    if (isMobile()) {
        carouselTrack.style.transform = '';
    }
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
const elevatedImage = document.getElementById('elevatedImage');
const heroTitleMain = document.querySelector('.hero-title-main');

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

        // ── Hero title + Elevated image fade out at the very end of spacer (last 15%) ──
        if (heroTitleOverlay) {
            const fadeStart = spacerHeight * 0.85;
            const fadeEnd = spacerHeight;
            if (scrollY >= fadeStart) {
                const progress = Math.min((scrollY - fadeStart) / (fadeEnd - fadeStart), 1);
                heroTitleOverlay.style.opacity = 1 - progress;
            } else {
                heroTitleOverlay.style.opacity = 1;
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
            rotateVideo: "images/rotating-shakes/oreo-delight-rotate.webm",
            desc: "Classic cookie perfection in every sip. Creamy cookies-and-cream blended with premium vanilla ice cream.",
            bg: "#00205B",      // Oreo brand dark navy blue
            navAccent: "#003087", // Oreo blue accent
            category: "StraightShake"
        },
        {
            name: "Strawberry Dream",
            tag: "Fresh",
            image: "images/strawberry-dream-nobg.webp",
            rotateVideo: "images/rotating-shakes/strawberry-dream-rotate.webm",
            desc: "Fresh strawberries blended to perfection. Vibrant pink milkshake with real fruit flavor.",
            bg: "#5C0020",      // Deep strawberry crimson
            navAccent: "#9B1040", // Raspberry accent
            category: "StraightShake"
        },
        {
            name: "Milo Magic",
            tag: "Signature",
            image: "images/milo-magic-nobg.webp",
            rotateVideo: "images/rotating-shakes/milo-magic-rotate.webm",
            desc: "Rich chocolate malt indulgence. Deep malty chocolate meets premium ice cream.",
            bg: "#004D1A",      // Milo brand deep green
            navAccent: "#006E25", // Milo green accent
            category: "StraightShake"
        },
        {
            name: "Jäger Shake",
            tag: "Premium · 18+",
            image: "images/jager-shake-nobg.webp",
            rotateVideo: "images/rotating-shakes/jager-shake-rotate.webm",
            desc: "Premium alcohol-infused luxury. Jägermeister meets rich chocolate and vanilla.",
            bg: "#2A1000",      // Deep amber/brown — Jäger orange-brown theme
            navAccent: "#7A3500", // Burnt orange-brown Jäger accent
            category: "ShotShake"
        },
        {
            name: "Amarula Bliss",
            tag: "Luxury · 18+",
            image: "images/amarula-bliss-nobg.webp",
            rotateVideo: "images/rotating-shakes/amarula-bliss-rotate.webm",
            desc: "Creamy liqueur meets milkshake perfection. Smooth, luxurious, and irresistibly indulgent.",
            bg: "#2D3D1A",      // Dark pistachio/sage green — Amarula feel
            navAccent: "#4A6828", // Pistachio accent
            category: "ShotShake"
        },
        {
            name: "Strawberry Kiss",
            tag: "Sweet · 18+",
            image: "images/strawberry-kiss-nobg.webp",
            rotateVideo: "images/rotating-shakes/strawberry-kiss-rotate.webm",
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
                    <img src="${shake.image}" alt="${shake.name}" class="scroll-blend-image" data-shake="${shake.name}" />
                    <div class="scroll-blend-video-wrapper">
                        <video class="scroll-blend-rotate-video" muted playsinline preload="none" loop>
                            <source src="${shake.rotateVideo}" type="video/webm">
                        </video>
                    </div>
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

    // ── HOVER ROTATING VIDEOS WITH SCROLL SCRUB ──
    // Wait for DOM to update after sections are created
    setTimeout(() => {
        const rotateVideos = document.querySelectorAll('.scroll-blend-rotate-video');
        const scrollBlendImages = document.querySelectorAll('.scroll-blend-image');
        
        rotateVideos.forEach((video, index) => {
            const img = scrollBlendImages[index];
            const visual = img ? img.closest('.scroll-blend-visual') : null;
            
            if (!visual || !img) return;
            
            let isHovering = false;
            let videoLoaded = false;
            
            // Sync video size to match image exactly
            const syncVideoSize = () => {
                const imgRect = img.getBoundingClientRect();
                const imgStyle = window.getComputedStyle(img);
                video.style.width = imgStyle.width;
                video.style.maxWidth = imgStyle.maxWidth;
                video.style.height = imgStyle.height;
            };
            
            // Load video on first hover
            const loadVideo = () => {
                if (!videoLoaded) {
                    video.load();
                    videoLoaded = true;
                    // Wait for video metadata, then sync size
                    video.addEventListener('loadedmetadata', syncVideoSize, { once: true });
                }
            };
            
            // Hover/touch enter: show video, hide image, start playing
            const startVideo = () => {
                isHovering = true;
                loadVideo();
                syncVideoSize();
                video.currentTime = 0;
                video.play().catch(() => {});
            };
            
            const stopVideo = () => {
                isHovering = false;
                video.pause();
                video.currentTime = 0;
            };
            
            // Desktop hover
            visual.addEventListener('mouseenter', startVideo);
            visual.addEventListener('mouseleave', stopVideo);
            
            // Mobile touch
            visual.addEventListener('touchstart', (e) => {
                e.preventDefault();
                startVideo();
            });
            
            visual.addEventListener('touchend', (e) => {
                e.preventDefault();
                // Delay stop to allow scrolling
                setTimeout(() => {
                    if (!visual.matches(':hover')) {
                        stopVideo();
                    }
                }, 100);
            });
            
            // Scroll scrub: sync video playback with scroll position while hovering
            const handleScroll = () => {
                if (!isHovering || !videoLoaded || !video.duration) return;
                
                const section = visual.closest('.scroll-blend-section');
                if (!section) return;
                
                const sectionRect = section.getBoundingClientRect();
                const sectionTop = sectionRect.top + window.pageYOffset;
                const sectionHeight = sectionRect.height;
                const scrollY = window.pageYOffset;
                const relativeScroll = scrollY - sectionTop;
                
                // Only scrub when section is in viewport
                if (sectionRect.top < window.innerHeight && sectionRect.bottom > 0) {
                    // Map scroll position within section to video timeline (0 to duration)
                    const scrollProgress = Math.max(0, Math.min(1, relativeScroll / sectionHeight));
                    video.currentTime = scrollProgress * video.duration;
                }
            };
            
            window.addEventListener('scroll', handleScroll, { passive: true });
            window.addEventListener('resize', syncVideoSize);
        });
    }, 100);

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
            // Before curtain — still in hero zone
            mainContentCurtain.style.backgroundColor = bgColors[0];
            // DON'T touch navbar here — the hero scroll handler keeps it transparent
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




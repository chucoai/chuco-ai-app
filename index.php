
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chuco AI | AI Consulting for Small & Mid-Sized Businesses</title>
    <meta name="description" content="El Paso-based AI consulting agency helping SMBs streamline operations, boost revenue, and future-proof processes through practical AI solutions.">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Header */
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            background: linear-gradient(45deg, #fff, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }

        .nav-links a:hover {
            color: #e0e7ff;
            transform: translateY(-2px);
        }

        .cta-btn {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white !important;
            padding: 0.8rem 1.5rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        }

        .cta-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 150px 0 100px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }

        .hero-content {
            position: relative;
            z-index: 2;
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #fff, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: fadeInUp 1s ease;
        }

        .hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            opacity: 0.9;
            animation: fadeInUp 1s ease 0.2s both;
        }

        .hero-cta {
            display: inline-flex;
            gap: 1rem;
            animation: fadeInUp 1s ease 0.4s both;
        }

        .btn-primary {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        }

        .btn-secondary {
            background: transparent;
            color: white;
            padding: 1rem 2rem;
            border: 2px solid white;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }

        .btn-secondary:hover {
            background: white;
            color: #667eea;
            transform: translateY(-3px);
        }

        /* Services Section */
        .services {
            padding: 100px 0;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
            color: #2d3748;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            border-radius: 2px;
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 4rem;
        }

        .service-card {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .service-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(45deg, #667eea, #764ba2);
        }

        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .service-icon {
            font-size: 3rem;
            color: #667eea;
            margin-bottom: 1rem;
        }

        .service-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #2d3748;
        }

        .service-card p {
            color: #718096;
            margin-bottom: 1.5rem;
        }

        .service-price {
            font-weight: bold;
            color: #667eea;
            font-size: 1.2rem;
        }

        /* About Section */
        .about {
            padding: 100px 0;
            background: white;
        }

        .about-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }

        .about-text h2 {
            font-size: 2.5rem;
            margin-bottom: 2rem;
            color: #2d3748;
        }

        .about-text p {
            font-size: 1.1rem;
            color: #718096;
            margin-bottom: 1.5rem;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
            margin-top: 2rem;
        }

        .stat {
            text-align: center;
            padding: 1.5rem;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 15px;
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            display: block;
        }

        .stat-label {
            color: #718096;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Contact Section */
        .contact {
            padding: 100px 0;
            background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
            color: white;
        }

        .contact-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }

        .contact-form {
            background: rgba(255,255,255,0.1);
            padding: 2rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #e2e8f0;
        }

        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .form-group input::placeholder,
        .form-group textarea::placeholder {
            color: rgba(255,255,255,0.6);
        }

        .contact-info h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #e2e8f0;
        }

        .contact-info p {
            margin-bottom: 1rem;
            color: #cbd5e0;
        }

        .contact-item {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }

        .contact-item i {
            margin-right: 1rem;
            font-size: 1.2rem;
            color: #feca57;
        }

        /* Footer */
        footer {
            background: #1a202c;
            color: white;
            text-align: center;
            padding: 2rem 0;
        }

        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }

            .hero h1 {
                font-size: 2.5rem;
            }

            .hero p {
                font-size: 1.1rem;
            }

            .hero-cta {
                flex-direction: column;
                align-items: center;
            }

            .about-content,
            .contact-content {
                grid-template-columns: 1fr;
                gap: 2rem;
            }

            .stats {
                grid-template-columns: 1fr;
            }
        }

        /* Floating Elements */
        .floating-element {
            position: absolute;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <nav class="container">
            <div class="logo">Chuco AI</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
            <a href="#contact" class="cta-btn">Get Started</a>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="home">
        <div class="container">
            <div class="hero-content">
                <h1>AI That Actually Works for Your Business</h1>
                <p>El Paso-based AI consulting helping small and mid-sized businesses streamline operations, boost revenue, and future-proof their processes through practical AI solutions.</p>
                <div class="hero-cta">
                    <a href="#contact" class="btn-primary">Start Your AI Journey</a>
                    <a href="#services" class="btn-secondary">View Services</a>
                </div>
            </div>
        </div>
        
        <!-- Floating Elements -->
        <div class="floating-element" style="top: 20%; left: 10%; font-size: 2rem;">
            <i class="fas fa-robot"></i>
        </div>
        <div class="floating-element" style="top: 60%; right: 15%; font-size: 1.5rem;">
            <i class="fas fa-chart-line"></i>
        </div>
        <div class="floating-element" style="top: 40%; right: 8%; font-size: 2.5rem;">
            <i class="fas fa-cogs"></i>
        </div>
    </section>

    <!-- Services Section -->
    <section class="services" id="services">
        <div class="container">
            <h2 class="section-title">Our AI Solutions</h2>
            
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <h3>AI Opportunity Audits</h3>
                    <p>Comprehensive analysis of your workflows and data readiness to identify the best AI implementation opportunities.</p>
                    <div class="service-price">$3K - $5K</div>
                </div>

                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>Custom LLM Integrations</h3>
                    <p>Domain-tuned AI assistants, support bots, and lead generation systems tailored to your business needs.</p>
                    <div class="service-price">$15K - $100K</div>
                </div>

                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <h3>Data Strategy & Architecture</h3>
                    <p>Design and implement data pipelines, warehousing solutions, and governance frameworks for AI readiness.</p>
                    <div class="service-price">$20K - $80K</div>
                </div>

                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-cogs"></i>
                    </div>
                    <h3>AI-Driven Automation</h3>
                    <p>RPA, API orchestration, and low-code workflow automation to eliminate repetitive tasks and boost efficiency.</p>
                    <div class="service-price">$10K - $50K</div>
                </div>

                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <h3>Training & Change Management</h3>
                    <p>Hands-on staff training and change management strategies to ensure successful AI adoption across your team.</p>
                    <div class="service-price">$5K - $25K</div>
                </div>

                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-headset"></i>
                    </div>
                    <h3>Managed AI Services</h3>
                    <p>Ongoing support, monitoring, and optimization of your AI systems to ensure continued performance and ROI.</p>
                    <div class="service-price">$1K - $10K/month</div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section class="about" id="about">
        <div class="container">
            <div class="about-content">
                <div class="about-text">
                    <h2>15+ Years of Proven Results</h2>
                    <p>Founded by David Negrete, Chuco AI builds on over a decade of experience in web design, marketing, and automation through ventures like 915 Web Design, American Water Softeners, and Garcia Water Care.</p>
                    <p>We're not just AI consultants – we're business operators who understand what it takes to drive real ROI. Our bilingual team serves both local El Paso businesses and national clients with the same commitment to practical, results-driven solutions.</p>
                    <p>Our mission is simple: make AI accessible, practical, and profitable for small and mid-sized businesses ready to compete in the modern marketplace.</p>
                </div>
                
                <div class="stats">
                    <div class="stat">
                        <span class="stat-number">15+</span>
                        <span class="stat-label">Years Experience</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">100+</span>
                        <span class="stat-label">Projects Completed</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">55%</span>
                        <span class="stat-label">Average ROI Increase</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">24/7</span>
                        <span class="stat-label">Support Available</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="contact" id="contact">
        <div class="container">
            <h2 class="section-title" style="color: white;">Ready to Transform Your Business?</h2>
            
            <div class="contact-content">
                <div class="contact-info">
                    <h3>Let's Discuss Your AI Opportunities</h3>
                    <p>Schedule a free consultation to explore how AI can streamline your operations and boost your bottom line.</p>
                    
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>El Paso, Texas</span>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <span>(915) 555-0123</span>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <span>hello@chuco.ai</span>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-clock"></i>
                        <span>Mon-Fri: 9AM-6PM MST</span>
                    </div>
                    
                    <p style="margin-top: 2rem; color: #cbd5e0;">
                        <strong>Bilingual Services Available</strong><br>
                        Servicios disponibles en español
                    </p>
                </div>

                <form class="contact-form">
                    <div class="form-group">
                        <label for="name">Full Name</label>
                        <input type="text" id="name" name="name" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email" placeholder="your@email.com" required>
                    </div>
                    <div class="form-group">
                        <label for="company">Company</label>
                        <input type="text" id="company" name="company" placeholder="Your Company">
                    </div>
                    <div class="form-group">
                        <label for="message">Tell us about your AI needs</label>
                        <textarea id="message" name="message" rows="4" placeholder="Describe your current challenges and what you'd like to achieve with AI..." required></textarea>
                    </div>
                    <button type="submit" class="btn-primary" style="width: 100%;">Schedule Free Consultation</button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2025 Chuco AI. All rights reserved. | Helping businesses thrive with practical AI solutions.</p>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Form submission handler
        document.querySelector('.contact-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Simple validation
            if (!data.name || !data.email || !data.message) {
                alert('Please fill in all required fields.');
                return;
            }
            
            // Simulate form submission
            alert('Thank you for your interest! We\'ll contact you within 24 hours to schedule your free consultation.');
            this.reset();
        });

        // Add scroll effect to header
        window.addEventListener('scroll', function() {
            const header = document.querySelector('header');
            if (window.scrollY > 100) {
                header.style.background = 'rgba(102, 126, 234, 0.95)';
            } else {
                header.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }
        });

        // Animate service cards on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.service-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease';
            observer.observe(card);
        });
    </script>
</body>
</html>

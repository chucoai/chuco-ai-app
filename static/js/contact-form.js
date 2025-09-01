/**
 * Contact Form Handler for Chuco AI
 * Add this to your static/js/ directory
 */

class ContactFormHandler {
    constructor() {
        this.formId = 'contact-form';
        this.apiEndpoint = '/api/contact';
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupForm());
        } else {
            this.setupForm();
        }
    }

    setupForm() {
        // Create and inject the form if it doesn't exist
        const existingForm = document.getElementById(this.formId);
        if (!existingForm) {
            this.injectForm();
        }

        // Attach event listener
        const form = document.getElementById(this.formId);
        if (form) {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        // Setup field validation
        this.setupFieldValidation();
    }

    injectForm() {
        // Find the contact section or create one
        let contactSection = document.getElementById('contact');
        if (!contactSection) {
            contactSection = document.querySelector('.cta-section');
        }

        if (contactSection) {
            const formHTML = `
                <div class="contact-form-container" style="max-width: 800px; margin: 40px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                    <h3 style="color: #333; margin-bottom: 30px; text-align: center;">Get Your Free AI Consultation</h3>
                    
                    <form id="${this.formId}" class="contact-form">
                        <!-- Success/Error Messages -->
                        <div id="form-message" style="display: none; padding: 15px; margin-bottom: 20px; border-radius: 8px;"></div>
                        
                        <!-- Personal Information -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div class="form-group">
                                <label for="first_name" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">First Name *</label>
                                <input type="text" id="first_name" name="first_name" required 
                                       style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;">
                            </div>
                            <div class="form-group">
                                <label for="last_name" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Last Name *</label>
                                <input type="text" id="last_name" name="last_name" required 
                                       style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;">
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div class="form-group">
                                <label for="email" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Email *</label>
                                <input type="email" id="email" name="email" required 
                                       style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;">
                            </div>
                            <div class="form-group">
                                <label for="phone" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Phone</label>
                                <input type="tel" id="phone" name="phone" 
                                       placeholder="(555) 123-4567"
                                       style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;">
                            </div>
                        </div>

                        <!-- Company Information -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div class="form-group">
                                <label for="company_name" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Company Name</label>
                                <input type="text" id="company_name" name="company_name" 
                                       style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;">
                            </div>
                            <div class="form-group">
                                <label for="company_website" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Company Website</label>
                                <input type="url" id="company_website" name="company_website" 
                                       placeholder="www.example.com"
                                       style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;">
                            </div>
                        </div>

                        <!-- Business Details -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div class="form-group">
                                <label for="company_size" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Company Size</label>
                                <select id="company_size" name="company_size" 
                                        style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; background: white;">
                                    <option value="">Select size...</option>
                                    <option value="1-5">1-5 employees</option>
                                    <option value="5-10">5-10 employees</option>
                                    <option value="10-50">10-50 employees</option>
                                    <option value="50-100">50-100 employees</option>
                                    <option value="100+">100+ employees</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="industry" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Industry</label>
                                <input type="text" id="industry" name="industry" 
                                       placeholder="e.g., E-commerce, Healthcare, Construction"
                                       style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;">
                            </div>
                        </div>

                        <!-- Project Information -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div class="form-group">
                                <label for="service_interested" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Service Interested In</label>
                                <select id="service_interested" name="service_interested" 
                                        style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; background: white;">
                                    <option value="other">Select a service...</option>
                                    <option value="ai_audit">AI Opportunity Audit</option>
                                    <option value="chatbot_llm">Custom AI Chatbots & LLM</option>
                                    <option value="data_strategy">Data Strategy & Architecture</option>
                                    <option value="process_automation">Process Automation</option>
                                    <option value="ai_training">AI Training & Change Management</option>
                                    <option value="ongoing_support">Ongoing AI Support</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="project_timeline" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Project Timeline</label>
                                <select id="project_timeline" name="project_timeline" 
                                        style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; background: white;">
                                    <option value="">Select timeline...</option>
                                    <option value="Immediate">Immediate (ASAP)</option>
                                    <option value="1-3 months">1-3 months</option>
                                    <option value="3-6 months">3-6 months</option>
                                    <option value="6-12 months">6-12 months</option>
                                    <option value="Planning stage">Just planning</option>
                                </select>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div class="form-group">
                                <label for="budget_range" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Budget Range</label>
                                <select id="budget_range" name="budget_range" 
                                        style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; background: white;">
                                    <option value="">Select budget...</option>
                                    <option value="Under $5k">Under $5,000</option>
                                    <option value="$5k-$10k">$5,000 - $10,000</option>
                                    <option value="$10k-$25k">$10,000 - $25,000</option>
                                    <option value="$25k-$50k">$25,000 - $50,000</option>
                                    <option value="$50k-$100k">$50,000 - $100,000</option>
                                    <option value="$100k+">$100,000+</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="preferred_contact_method" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">Preferred Contact Method</label>
                                <select id="preferred_contact_method" name="preferred_contact_method" 
                                        style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; background: white;">
                                    <option value="email">Email</option>
                                    <option value="phone">Phone</option>
                                    <option value="text">Text Message</option>
                                </select>
                            </div>
                        </div>

                        <!-- Message -->
                        <div class="form-group" style="margin-bottom: 20px;">
                            <label for="message" style="display: block; margin-bottom: 5px; color: #555; font-weight: 600;">How can we help you? *</label>
                            <textarea id="message" name="message" required rows="5" 
                                      placeholder="Tell us about your business challenges and what you'd like to achieve with AI..."
                                      style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; resize: vertical;"></textarea>
                        </div>

                        <!-- Hidden fields for tracking -->
                        <input type="hidden" id="lead_source" name="lead_source" value="website">
                        <input type="hidden" id="utm_source" name="utm_source" value="">
                        <input type="hidden" id="utm_medium" name="utm_medium" value="">
                        <input type="hidden" id="utm_campaign" name="utm_campaign" value="">

                        <!-- Submit Button -->
                        <div style="text-align: center;">
                            <button type="submit" id="submit-btn" 
                                    style="background: linear-gradient(45deg, #8B5CF6, #A855F7); color: white; padding: 15px 40px; border: none; border-radius: 50px; font-size: 18px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                                Get Your Free Consultation
                            </button>
                        </div>
                    </form>
                </div>
            `;

            // Insert the form into the contact section
            const container = document.createElement('div');
            container.innerHTML = formHTML;
            contactSection.appendChild(container.firstElementChild);
        }
    }

    setupFieldValidation() {
        // Phone number formatting
        const phoneInput = document.getElementById('phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 0) {
                    if (value.length <= 3) {
                        value = `(${value}`;
                    } else if (value.length <= 6) {
                        value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
                    } else {
                        value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
                    }
                }
                e.target.value = value;
            });
        }

        // Website URL formatting
        const websiteInput = document.getElementById('company_website');
        if (websiteInput) {
            websiteInput.addEventListener('blur', (e) => {
                let value = e.target.value.trim();
                if (value && !value.startsWith('http://') && !value.startsWith('https://')) {
                    e.target.value = 'https://' + value;
                }
            });
        }

        // Email validation
        const emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.addEventListener('blur', (e) => {
                const email = e.target.value;
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (email && !emailRegex.test(email)) {
                    e.target.setCustomValidity('Please enter a valid email address');
                } else {
                    e.target.setCustomValidity('');
                }
            });
        }
    }

    async handleSubmit(e) {
        e.preventDefault();

        const form = e.target;
        const submitBtn = document.getElementById('submit-btn');
        const messageDiv = document.getElementById('form-message');

        // Disable submit button and show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
        submitBtn.style.opacity = '0.7';

        // Get form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            if (value) data[key] = value;
        });

        // Add UTM parameters from URL if present
        const urlParams = new URLSearchParams(window.location.search);
        data.utm_source = urlParams.get('utm_source') || data.utm_source || '';
        data.utm_medium = urlParams.get('utm_medium') || data.utm_medium || '';
        data.utm_campaign = urlParams.get('utm_campaign') || data.utm_campaign || '';

        try {
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // Show success message
                this.showMessage('success', result.message || 'Thank you! We\'ll be in touch within 24 hours.');

                // Reset form
                form.reset();

                // Track conversion if analytics is available
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'form_submit', {
                        'event_category': 'Contact',
                        'event_label': 'Contact Form',
                        'value': result.data?.lead_score || 0
                    });
                }

                // Scroll to message
                messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

            } else {
                // Show error message
                this.showMessage('error', result.message || 'Something went wrong. Please try again.');
            }

        } catch (error) {
            console.error('Form submission error:', error);
            this.showMessage('error', 'Network error. Please check your connection and try again.');
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Get Your Free Consultation';
            submitBtn.style.opacity = '1';
        }
    }

    showMessage(type, message) {
        const messageDiv = document.getElementById('form-message');
        if (!messageDiv) return;

        messageDiv.style.display = 'block';
        messageDiv.textContent = message;

        if (type === 'success') {
            messageDiv.style.background = '#10b981';
            messageDiv.style.color = 'white';
        } else {
            messageDiv.style.background = '#ef4444';
            messageDiv.style.color = 'white';
        }

        // Auto-hide message after 10 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 10000);
    }
}

// Initialize the contact form handler when the script loads
const contactFormHandler = new ContactFormHandler();

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ContactFormHandler;
}
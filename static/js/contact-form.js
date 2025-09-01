document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Get reCAPTCHA token
            const recaptchaToken = typeof grecaptcha !== 'undefined' ? grecaptcha.getResponse() : '';

            const formData = new FormData(contactForm);
            const data = {
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                company_name: formData.get('company_name') || '',
                company_website: formData.get('company_website') || '',
                service_interested: formData.get('service_interested'),
                project_timeline: formData.get('project_timeline'),
                message: formData.get('message') || '',
                recaptcha_token: recaptchaToken
            };

            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message || 'Thank you for your inquiry!');
                    contactForm.reset();
                    if (typeof grecaptcha !== 'undefined') {
                        grecaptcha.reset();
                    }
                } else {
                    alert(result.detail || 'Something went wrong. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Something went wrong. Please try again.');
            }
        });
    }
});